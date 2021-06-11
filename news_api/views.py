from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.settings import NEWSAPI_KEY
from newsapi import NewsApiClient


@api_view(["GET"])
def news_search(request):
    search_string = request.query_params.get("q", "")
    output = list()

    if not search_string:
        return Response(
            dict(details="Please provide a search string to proceed"),
            status=400,
        )

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    all_articles = newsapi.get_everything(
        q=search_string,
        language="en",
        sort_by="relevancy",
        page_size=100,
    )

    for news in all_articles["articles"]:
        output.append(
            dict(
                source_name=news["source"]["name"],
                heading=news["title"],
                description=news["description"],
                imageURL=news["urlToImage"],
                publishedAt=news["publishedAt"],
                articleLink=news["url"],
            )
        )
    return Response(dict(details=output), status=200)


@api_view(["GET"])
def get_trending_news(request):
    output = []
    category = request.data.get("category", "")

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    if category:
        top_headlines = newsapi.get_top_headlines(
            language="en",
            page_size=100,
            category=category,
        )
    else:
        top_headlines = newsapi.get_top_headlines(
            language="en",
            page_size=100,
        )

    for news in top_headlines["articles"]:
        output.append(
            dict(
                source_name=news["source"]["name"],
                heading=news["title"],
                description=news["description"],
                imageURL=news["urlToImage"],
                publishedAt=news["publishedAt"],
                articleLink=news["url"],
            )
        )

    return Response(dict(details=output), status=200)
