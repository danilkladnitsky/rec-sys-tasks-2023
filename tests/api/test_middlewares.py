from http import HTTPStatus

from starlette.testclient import TestClient

API_KEY_HEADER = "default_api_key"


def test_public_url(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_invalid_api_key(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/reco/sample_model/1", headers={"Api-Key": "validJWTiPromise"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_valid_api_key(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/reco/sample_model/1", headers={"Api-Key": API_KEY_HEADER})
    assert response.status_code == HTTPStatus.OK
