from fastapi.testclient import TestClient

# Test Data
test_recipe = {
    'title': 'Test Recipe',
    'ingredients': [1, 2, 3, 4, 5],
	'instructions': 'test instructions'
}

def test_get_recipes(client: TestClient):
    response = client.get('/recipes/')
    assert response.status_code == 200
    assert 'items' in response.json()

def test_create_recipe(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/recipes/', json=test_recipe, headers=headers)
    assert response.status_code == 201
    assert response.json()['title'] == test_recipe['title']

def test_get_recipe(client: TestClient):
    response = client.get('/recipes/1')
    assert response.status_code == 200
    assert response.json()['title'] == test_recipe['title']

def test_update_recipe(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    updated_data = {'title': 'Updated Recipe', 'instructions': 'Updated instrutions'}
    response = client.put('/recipes/1', json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['title'] == updated_data['title']

def test_update_image(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    with open('app/static/test_image.jpg', 'rb') as image_file:
        response = client.patch('/recipes/1/image', files={'image_file': image_file}, headers=headers)
    assert response.status_code == 201
    assert 'image_name' in response.json()

def test_delete_recipe(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete('/recipes/1', headers=headers)
    assert response.status_code == 204

def test_search_by_preferences(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/recipes/search-by-preferences', headers=headers)
    assert response.status_code == 200
    assert 'items' in response.json()