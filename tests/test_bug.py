from starlette.testclient import TestClient

from starlette_testclient_bug import app


# get works
def test_get():
    with TestClient(app) as client:
        data = client.get("/hello").raise_for_status().json()
        assert data == {"hello": "world"}


# post works
def test_post():
    with TestClient(app) as client:
        data = client.post("/hello").raise_for_status().json()
        assert data == {"hello": "world"}


# websockets work
def test_ws():
    with TestClient(app) as client:
        with client.websocket_connect("/ws/hello") as ws:
            assert ws.receive_text() == "Hello, world!"


# helper method
def _do_post_ws_test():
    with TestClient(app) as client:
        with client.websocket_connect("/ws/register") as ws:
            _ = client.post("/ping").raise_for_status()
            assert ws.receive_text() == "pong"


# this is fine
def test_post_with_ws_1():
    _do_post_ws_test()


# this breaks!
def test_post_with_ws_2():
    _do_post_ws_test()
