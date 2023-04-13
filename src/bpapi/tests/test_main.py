from fastapi.testclient import TestClient

import bpapi.app as app

client = TestClient(app.app)


def test_no_token_sections():
    response = client.get('/api/v1/sections/')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authentificated',}
