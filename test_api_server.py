import pytest
from fastapi.testclient import TestClient
from api_server import app


@pytest.fixture(name="client")
def client_fixture():
    # Does not work with lifespan
    # client = TestClient(app)
    # yield client
    # Below works with lifespan
    with TestClient(app) as client:
        print("\nSetting up client")
        yield client
        print("\nClosing client")

# Works with lifespan
def test_read_root():
    with TestClient(app) as local_client:
        response = local_client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "WITH lifespan"}

# Works with lifespan
# Note how the client is formed in the fixture
def test_read_root_fixture(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "WITH lifespan"}

# Does not work with lifespan when on its own, but works when run with other tests
def test_read_root_fail(request):
    # Note: This is a hack to check if the test is being run on its own
    if request.node.name not in request.config.args[0]:
        return

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "with NO lifespan"}


def test_read_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "WITH lifespan"}

