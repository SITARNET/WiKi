from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    article = util.get_entry(title)
    if article == None:
        return render(request, "encyclopedia/article_not_found.html", {
            "title": title
    })

    return render(request, "encyclopedia/article.html", {
        "article": markdown(article),
        "title": title
    })

