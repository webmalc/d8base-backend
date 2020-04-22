"""The views tests module."""
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse

from conftest import OBJECTS_TO_CREATE
from d8b.lang import select_locale
from users.models import User

pytestmark = pytest.mark.django_db


def test_category_list(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    response = client.get(reverse('categories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == categories.count()


def test_category_display(client: Client, categories: QuerySet):
    """Should return a list of categories."""
    cat = categories.first()
    response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['name'] == cat.name_en


def test_category_display_de(client: Client, categories: QuerySet):
    """Should return a list of categories [de]."""
    cat = categories.first()
    with select_locale('de'):
        response = client.get(reverse('categories-detail', args=[cat.pk]))

    assert response.json()['name'] == cat.name_de
    assert response.json()['description'] == cat.description_de


def test_subcategory_list(client: Client, subcategories: QuerySet):
    """Should return a list of subcategories."""
    subcat = subcategories.first()
    response = client.get(reverse('subcategories-list'))

    assert response.status_code == 200
    assert response.accepted_media_type == 'application/json'
    assert response.json()['count'] == subcategories.count()
    assert response.json()['results'][0]['name'] == 'category 0: subcategory 0'
    assert response.json()['results'][0]['category'] == subcat.category.pk


def test_user_professionals_list(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a professionals list."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.get(reverse('user-professionals-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 2
    assert data['results'][0]['name'] == obj.name


def test_user_professionals_detail(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should return a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-professionals-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['level'] == obj.level


def test_user_professionals_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.patch(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professionals_create(
    user: User,
    client_with_token: Client,
    subcategories: QuerySet,
):
    """Should be able to create a user professional object."""
    response = client_with_token.post(
        reverse('user-professionals-list'),
        {
            'name': 'test professional',
            'description': 'test professional description',
            'subcategory': subcategories.first().pk
        },
    )
    assert response.status_code == 201
    assert user.professionals.first().name == 'test professional'


def test_user_professionals_update(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to update a user professional."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.patch(
        reverse('user-professionals-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.user == user
    assert obj.modified_by == user


def test_user_professionals_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.post(
        reverse('user-professionals-detail', args=[obj.pk]), {'name': 'xxx'})
    assert response.status_code == 405


def test_user_professionals_delete(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to delete a user professionals."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.delete(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professionals.filter(pk=obj.pk).count() == 0


def test_user_professionals_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professionals.filter(user=admin).first()
    response = client_with_token.delete(
        reverse('user-professionals-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_list(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a professional tags list."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.get(reverse('user-professional-tags-list'))
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == OBJECTS_TO_CREATE * 2
    assert data['results'][0]['name'] == obj.name


def test_user_professional_tags_detail(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should return a user professional tag."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == obj.name


def test_user_professional_tags_detail_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_tags_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional tag object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse('user-professional-tags-list'),
        {
            'name': 'test professional tag',
            'professional': obj.pk,
        },
    )
    assert response.status_code == 201
    assert obj.tags.first().name == 'test professional tag'


def test_user_professional_tags_update(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to update a user professional."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.patch(
        reverse('user-professional-tags-detail', args=[obj.pk]),
        {
            'name': 'new name',
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.name == 'new name'
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_tags_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse('user-professional-tags-detail', args=[obj.pk]), {'name': 'x'})
    assert response.status_code == 405


def test_user_professional_tags_delete(
    user: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should be able to delete a user professionals."""
    obj = professional_tags.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 204
    assert professional_tags.filter(pk=obj.pk).count() == 0


def test_user_professional_tags_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_tags: QuerySet,
):
    """Should deny access to someone else's record."""
    obj = professional_tags.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse('user-professional-tags-detail', args=[obj.pk]))
    assert response.status_code == 404
