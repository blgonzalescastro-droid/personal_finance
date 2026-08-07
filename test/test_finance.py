from datetime import date, timedelta

import pytest
from faker import Faker
from rest_framework.test import APIClient
from rest_framework import status

faker = Faker()

API_PREFIX = '/api'


@pytest.fixture
def client_with_auth():
    client = APIClient()

    register_payload = {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": faker.password(length=10),
    }
    register_response = client.post(f'{API_PREFIX}/auth/register/', register_payload, format='json')
    assert register_response.status_code == status.HTTP_201_CREATED

    login_payload = {
        'username': register_payload['username'],
        'password': register_payload['password'],
    }
    login_response = client.post(f'{API_PREFIX}/auth/login/', login_payload, format='json')
    assert login_response.status_code == status.HTTP_200_OK

    access_token = login_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.mark.django_db
def test_unauthenticated_access_denied():
    client = APIClient()
    response = client.get(f'{API_PREFIX}/cards/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_card(client_with_auth):
    payload = {
        'card_number': str(faker.random_number(digits=16, fix_len=True)),
        'card_holder': faker.name(),
        'expire_date': '12/28',
        'balance': '100.00',
        'weekly_limit': '500.00',
        'is_active': True,
    }
    response = client_with_auth.post(f'{API_PREFIX}/cards/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.data['id'], int)
    assert response.data['card_number'] == payload['card_number']


@pytest.mark.django_db
def test_create_card_invalid_number(client_with_auth):
    payload = {
        'card_number': '123',
        'card_holder': faker.name(),
        'expire_date': '12/28',
        'balance': '0',
        'weekly_limit': '500.00',
    }
    response = client_with_auth.post(f'{API_PREFIX}/cards/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'card_number' in response.data


@pytest.mark.django_db
def test_create_transaction(client_with_auth):
    payload = {
        'receiver': faker.company(),
        'category': 'Food',
        'amount': '25.50',
    }
    response = client_with_auth.post(f'{API_PREFIX}/transactions/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['amount'] == '25.50'


@pytest.mark.django_db
def test_create_transaction_invalid_amount(client_with_auth):
    payload = {
        'receiver': faker.company(),
        'category': 'Food',
        'amount': '-10',
    }
    response = client_with_auth.post(f'{API_PREFIX}/transactions/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'amount' in response.data


@pytest.mark.django_db
def test_create_goal(client_with_auth):
    payload = {
        'title': faker.sentence(nb_words=3),
        'target_amount': '1000.00',
        'target_date': str(date.today() + timedelta(days=30)),
    }
    response = client_with_auth.post(f'{API_PREFIX}/goals/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.data['id'], int)


@pytest.mark.django_db
def test_create_goal_past_date_rejected(client_with_auth):
    payload = {
        'title': faker.sentence(nb_words=3),
        'target_amount': '1000.00',
        'target_date': str(date.today() - timedelta(days=1)),
    }
    response = client_with_auth.post(f'{API_PREFIX}/goals/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'target_date' in response.data
