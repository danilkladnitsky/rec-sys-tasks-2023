from http import HTTPStatus

from starlette.testclient import TestClient

API_KEY_HEADER = "default_api_key"


def test_invalid_api_key(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health", headers={"Api-Key": "validJWTiPromise"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_valid_api_key(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health", headers={"Api-Key": API_KEY_HEADER})
    assert response.status_code == HTTPStatus.OK
