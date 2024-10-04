from http import HTTPStatus

import pytest
from pytest import lazy_fixture 
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lazy_fixture('home_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('detail_url'), lazy_fixture('client'), HTTPStatus.OK), # type: ignore
        (lazy_fixture('edit_url'), lazy_fixture('author_client'), HTTPStatus.OK),
        (lazy_fixture('delete_url'), lazy_fixture('author_client'), HTTPStatus.OK),
        (lazy_fixture('edit_url'), lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('delete_url'), lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('singup_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('login_url'), lazy_fixture('client'), HTTPStatus.OK),
        (lazy_fixture('logout_url'), lazy_fixture('client'), HTTPStatus.OK),
    )
)
@pytest.mark.django_db
def test_home_availability_for_anonymous_user(
    reverse_url, parametrized_client, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'variable_url',
    (
        (lazy_fixture('edit_url')),
        (lazy_fixture('delete_url')),
    )
)

def test_access_edit_delete_comment(
    client,
    variable_url,
    login_url,
):
    response = client.get(variable_url)
    expected_url = f'{login_url}?next={variable_url}'
    assertRedirects(response, expected_url)