import pytest
from django.urls import reverse

def test_api_parse_succeeds(client):
    address_string = '123 main st chicago il'
    url = reverse('address-parse') + f'?address={address_string}'
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert 'input_string' in data
    assert data['input_string'] == address_string
    assert 'address_components' in data
    assert 'address_type' in data
    assert isinstance(data['address_components'], dict)
    assert isinstance(data['address_type'], str)


def test_api_parse_raises_error(client):
    address_string = '123 main st chicago il 123 main st'
    url = reverse('address-parse') + f'?address={address_string}'
    response = client.get(url)
    assert response.status_code == 400

    data = response.json()
    assert 'error' in data
    assert isinstance(data['error'], str)