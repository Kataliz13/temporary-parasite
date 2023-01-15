from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.core.handlers.wsgi import WSGIRequest

NUM_POST: int = 10


def paginator(posts: QuerySet, request: WSGIRequest) -> Paginator:
    """Данная функция реализует
    постраничный вывод постов для view-функций
    index, group_posts, profile.
    """
    paginator = Paginator(posts, NUM_POST)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
