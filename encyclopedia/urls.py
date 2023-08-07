from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("search/", views.search_article, name="search"),
    path("new_article/", views.new_article, name="new_article"),
]


