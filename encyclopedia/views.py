from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from django import forms

from . import util


def helper(request, list_entries):    
    return render(request, "encyclopedia/index.html", {
            "entries": list_entries
        })


def index(request):
    return helper(request, util.list_entries())


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


def search_article(request):
    if request.method == "POST":
        article_name = request.POST['article_search']
        articles = []
        
        for entry in util.list_entries():
            if article_name == entry:
                return HttpResponseRedirect(reverse("article", args=(article_name, )))
            elif article_name in entry:
                articles.append(entry)
            

        if len(articles) == 0:
            return HttpResponseRedirect(reverse("article", args=(article_name, )))
        return helper(request, articles)
    
    

    


