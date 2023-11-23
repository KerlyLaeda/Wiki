from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from random import choice

from . import util


# Convert markdown to html
def md_to_html(title):
    page = util.get_entry(title)
    markdowner = Markdown()
    if page is None:
        return None
    else:
        return markdowner.convert(page)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display content of an entry
def entry(request, title):
    # Convert md to html
    converted_page = md_to_html(title)

    # If no such page found, display an error
    if converted_page is None:
        return render(request, "encyclopedia/errors.html", {
            "error": "Page not found :("
        })

    # If page exists, render it
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": converted_page
        })


# Search for an entry
def search():
    pass
    # if total match:
        # redirect to entry
    # sub in query:
        # list all with sub


# Create new entry
def add(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        # Check if an entry already exists with the provided title
        existing = util.get_entry(title)
        if existing:

            # Throw an error if it does
            return render(request, "encyclopedia/errors.html", {
                "error": "This page already exists!"
            })

        # Otherwise, save and redirect to newly created page
        else:
            converted_page = md_to_html(title)
            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": converted_page
            })

    return render(request, "encyclopedia/add.html")


# Edit entry
def edit(request, title):
    if request.method == "POST":
        #title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def random_page(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    converted_page = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": converted_page
    })
