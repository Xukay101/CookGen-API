from fastapi.testclient import TestClient

# Access Token 
access_token = None

# Test Data
test_user = {
    'username': 'testuser',
    'password': 'testpassword',
    'full_name': 'test user',
    'email': 'test@example.com'
}

def test_register_new_user(client: TestClient):
    response = client.post('/auth/register', json=test_user)
    assert response.status_code == 201
    assert 'id' in response.json()

def test_login_existing_user(client: TestClient):
    response = client.post('/auth/login', data=test_user)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_login_existing_user(client: TestClient):
    global access_token
    response = client.post('/auth/login', data=test_user)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    access_token = response.json()['access_token']

def test_verify_token(client: TestClient):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/auth/verify', headers=headers)
    assert response.status_code == 200
    assert response.json() == {'status': 'Token is valid', 'user_id': 2}

def test_logout(client: TestClient):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/auth/logout', headers=headers)
    assert response.status_code == 200
    assert response.json() == {'detail': 'Token has been revoked'}