import pytest

from create_slack_bday_chat import app

VERSION_PREFIX = app.config.get("APP_VERSION", "/v0/")


@pytest.fixture()
def client():
    with app.test_client() as test_client:
        yield test_client


def test_ping(client):
    resp = client.get(f"{VERSION_PREFIX}ping")

    assert resp.status_code == 200
    assert resp.data.decode() == "pong"
