from random import choice

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_name_course(api_client, factory_course):
    '''  Получение 1го курса  '''

    url = reverse('courses-detail', args='1')
    course = factory_course(_quantity=1)

    response = api_client.get(url)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_len_course(api_client, factory_course):
    '''  Получение списка курсов  '''

    url = reverse('courses-list')
    factory_course(_quantity=10)

    response = api_client.get(url)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == 10


@pytest.mark.django_db
def test_filte_id_course(api_client, factory_course):
    '''  Фильтрация по id  '''

    course = factory_course(_quantity=10)
    random_course = choice(course)
    url = reverse('courses-list')
    filter_course = {'id': str(random_course.id)}

    response = api_client.get(url, filter_course)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['id'] == random_course.id


@pytest.mark.django_db
def test_filte_name_course(api_client, factory_course):
    '''  Фильтрацция по name  '''

    course = factory_course(_quantity=10)
    random_course = choice(course)
    url = reverse('courses-list')
    filter_course = {'name': str(random_course.name)}

    response = api_client.get(url, filter_course)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['name'] == random_course.name


@pytest.mark.django_db
def test_create_course(api_client):
    '''  Cоздание курса  '''

    url = reverse('courses-list')
    create_data = {'name': 'test_name'}

    response = api_client.post(url, create_data)
    response2 = api_client.get(url)
    data = response2.json()

    assert response.status_code == HTTP_201_CREATED
    assert data[0]['name'] == 'test_name'


@pytest.mark.django_db
def test_update_course(api_client, factory_course):
    '''  Обновление курса  '''

    course = factory_course(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])
    create_data = {'name': 'new_name'}

    response = api_client.patch(url, data=create_data)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert data['name'] == 'new_name'


@pytest.mark.django_db
def test_delete_course(api_client, factory_course):
    '''  Удаление курса  '''

    course = factory_course(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])

    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert response.content_type is None


@pytest.mark.parametrize(["max_value", "expected_status"], ((0, HTTP_400_BAD_REQUEST), (5, HTTP_201_CREATED)))
@pytest.mark.django_db
def test_max_student_per_course(api_client, factory_student, factory_course, max_value, expected_status, settings):
    '''  Проверка количества студентов на курсе  '''

    settings.MAX_STUDENTS_PER_COURSE = max_value
    course = factory_course()
    students = factory_student(_quantity=3)
    url = reverse('courses-list')

    for student in students:
        data = {'name': course.name, 'students': [student.id]}
        response = api_client.post(url, data=data)
        assert response.status_code == expected_status

