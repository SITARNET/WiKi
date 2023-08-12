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


class FormArticle(forms.Form):
    title = forms.CharField(label="Title", max_length=30, widget=forms.TextInput(attrs={'class': 'form-article'}))
    article = forms.CharField(label="Article", widget=forms.Textarea(attrs={'class': 'form-textarea'}))

    
def new_article(request):
    if request.method == "POST":
        form = FormArticle(request.POST)

        if form.is_valid():
            article_title = form.cleaned_data["title"]
            article_content = form.cleaned_data["article"]

            for entry in util.list_entries():
                if entry == article_title:
                    return render(request, "encyclopedia/new_article.html", {
                        "title": article_title,
                        "message": f"Name {article_title} of file is alredy exists!",
                        "form": form
                    })
                else:
                    util.save_entry(article_title, article_content)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/new_article.html", {
                "form": form
            })

    return render(request, "encyclopedia/new_article.html", {
        "form": FormArticle()
    })


    


