from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes

from core.settings import NEWSAPI_KEY
from newsapi import NewsApiClient


@api_view(["GET"])
def news_search(request):
    search_string = request.query_params.get("q", "")
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 5)

    if not search_string:
        return Response(
            dict(details="Please provide a search string to proceed"),
            status=400,
        )

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        page_size = int(page_size)
        if page_size not in [5, 10]:
            raise ValueError
    except ValueError:
        page_size = 10

    if page > 100 / page_size:
        page = int(100 / page_size)

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    all_articles = newsapi.get_everything(
        q=search_string,
        language="en",
        sort_by="relevancy",
        page=page,
        page_size=page_size,
    )
    return Response(dict(details=all_articles), status=200)


@api_view(["GET"])
def get_trending_news(request):
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 5)
    country = request.query_params.get("country", "in")

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        page_size = int(page_size)
        if page_size not in [5, 10]:
            raise ValueError
    except ValueError:
        page_size = 5

    if page > 100 / page_size:
        page = int(100 / page_size)

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    top_headlines = newsapi.get_top_headlines(
        language="en",
        country=country,
        page=page,
        page_size=page_size,
    )

    return Response(dict(details=top_headlines), status=200)
