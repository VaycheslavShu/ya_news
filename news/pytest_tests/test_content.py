import pytest
from django.conf import settings
from pytest_lazyfixture import lazy_fixture 

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('news_list')
def test_news_count(client, home_url):
    response = client.get(home_url)
    assert (
        response.context['object_list'].count()
        == settings.NEWS_COUNT_ON_HOME_PAGE
    )


@pytest.mark.usefixtures('news_list')
def test_news_order(client, home_url):
    response = client.get(home_url)
    news_dates = [news.date for news in response.context['object_list']]
    ordered_dates = sorted(news_dates, reverse=True)
    assert news_dates == ordered_dates


@pytest.mark.usefixtures('comments_list')
def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    all_comments = response.context['news'].comment_set.all()
    assert list(all_comments) == list(all_comments.order_by('created'))


@pytest.mark.parametrize(
    'test_client_instance, access_form',
    (
        (lazy_fixture('author_client'), True),
        (lazy_fixture('client'), False),
    )
)
def test_form_shown_to_correct_user(
    test_client_instance,
    access_form,
    detail_url,
):
    response = test_client_instance.get(detail_url)
    assert ('form' in response.context) == access_form
    if access_form:
        assert isinstance(response.context['form'], CommentForm)