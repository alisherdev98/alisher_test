import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from employee.models import Employee
from employee.serializers import EmployeeSerializer, CreateEmployeeSerializer


class EmployeeAPITestCase(APITestCase):
    def setUp(self) -> None:
        user = Employee.objects.create_user(
            username='Test_user',
            email='test@test.com',
            password='12345678',
            is_staff=True
        )

        self.token = user.token
        self.user_token_id = user.id

    def test_get(self):
        url = reverse('employee_retrieve', args=[self.user_token_id])
        token = self.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_obj = Employee.objects.get(pk=self.user_token_id)
        self.assertEqual(response.data.get('employee', None), EmployeeSerializer(test_obj).data)


    def test_create_token(self):
        id_from_token = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256']).get('id', None)
        self.assertEqual(self.user_token_id, id_from_token)

    def test_post_create(self):
        url = reverse('employee_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, {
            "username": "Test",
            "email": "test1@test.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)