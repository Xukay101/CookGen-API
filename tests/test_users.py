from fastapi.testclient import TestClient

# Test Data
test_preference = {
    'ingredient_id': 1,
    'preference_type': 'like'
}

test_saved_recipe = {
    'recipe_id': 1 
}

def test_get_me(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/users/me', headers=headers)
    assert response.status_code == 200
    assert 'id' in response.json()

def test_get_preferences(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/users/me/preferences', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_set_user_preference(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/users/me/preferences', json=test_preference, headers=headers)
    assert response.status_code == 201
    assert response.json()['message'] == 'Preferences updated successfully'

def test_get_saved_recipes(client: TestClient, token: str):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/users/me/saved-recipes', headers=headers)
    assert response.status_code == 200
    assert 'items' in response.json()