from django.urls import path
from news_api.views import news_search, get_trending_news

urlpatterns = [
    path(
        "newsapi/search",
        news_search,
    ),
    path(
        "newsapi/trending",
        get_trending_news,
    ),
]
