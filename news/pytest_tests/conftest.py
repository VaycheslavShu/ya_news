from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

COMMENT_TXT = (
    'Текст новости',
    'просто текст',
)

FORM_DATA = {'text': COMMENT_TXT[1]}

@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client



@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TXT[0],
    )


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Заголовок новости {index}',
            text=f'Текст {index}',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments_list(author, news):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Коментарий {index}',
        )
        comment.created = now - timedelta(days=index)
        comment.save()


# conftest.py
@pytest.fixture
def home_url():
    return reverse('news:home')

@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))

@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))

@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))

@pytest.fixture
def singup_url():
    return reverse('users:signup')

@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


