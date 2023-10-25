from fastapi.testclient import TestClient

# Test Data
test_ingredient = {
    'name': 'Test Ingredient',
    'description': 'This is a test ingredient'
}

def test_get_ingredients(client: TestClient):
    response = client.get('/ingredients/')
    assert response.status_code == 200
    assert 'items' in response.json()

def test_create_ingredient(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/ingredients/', json=test_ingredient, headers=headers)
    assert response.status_code == 201
    assert response.json()['name'] == test_ingredient['name']

def test_get_ingredient(client: TestClient):
    response = client.get('/ingredients/21')
    assert response.status_code == 200
    assert response.json()['name'] == test_ingredient['name']

def test_update_ingredient(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    updated_data = {'name': 'Updated Ingredient', 'description': 'Updated description'}
    response = client.put('/ingredients/21', json=updated_data, headers=headers)
    assert response.status_code == 200