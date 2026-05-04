import pytest
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

def test_registration_endpoint():
    url = reverse('https://optiweb.lankapanel.net/register')  # Adjust to your URL name
    data = {
        "email": "chameerah@lankacom.net",
        "password": "20251228@Sri",
        "server_ip": "203.143.13.30"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
