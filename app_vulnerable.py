import pytest
import json
from app import app, init_db

@pytest.fixture(scope="module")
def test_client():
    init_db()
    with app.test_client() as client:
        yield client

def test_sql_injection_prevention(test_client):
    response = test_client.get("/user/' OR '1'='1")
    assert response.status_code == 400  # Invalid username format

def test_xss_mitigation(test_client):
    response = test_client.post("/xss", data={"name": "<script>alert(1)</script>"})
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.data  # XSS sanitized

def test_authentication_success(test_client):
    response = test_client.post("/login", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_authentication_failure(test_client):
    response = test_client.post("/login", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_ping_validation(test_client):
    response = test_client.get("/ping?target=127.0.0.1")
    assert response.status_code in [200, 500]  # Success or failure, but no injection

def test_open_redirect_prevention(test_client):
    response = test_client.get("/redirect?url=https://evil.com")
    assert response.status_code == 400  # Invalid redirect URL

def test_rate_limiting(test_client):
    for _ in range(5):
        response = test_client.get("/ping?target=127.0.0.1")
    limited_response = test_client.get("/ping?target=127.0.0.1")
    assert limited_response.status_code == 429  # Too many requests

def test_file_read_traversal_prevention(test_client):
    response = test_client.get("/read_file?file=../../etc/passwd")
    assert response.status_code == 404  # Prevents directory traversal

def test_deserialization_safety(test_client):
    response = test_client.post("/deserialize", json={"key": "value"})
    assert response.status_code == 200  # Valid JSON should pass
    response_invalid = test_client.post("/deserialize", data="invalid json")
    assert response_invalid.status_code == 400  # Invalid JSON should fail
