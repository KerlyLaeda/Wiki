from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from random import choice

from . import util


class EntryForm(forms.Form):
    title = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Title"}))

    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Content"}))


# Convert Markdown to HTML
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
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # If the entry exists with the provided title
            if util.get_entry(title):
                return render(request, "encyclopedia/errors.html", {
                    "error": "This page already exists!"
                })

            util.save_entry(title, content)

            # Redirect to the same page
            return redirect("entry", title)

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": EntryForm
    })


# Edit entry
# def edit(request, title):
#     if request.method == "POST":
#         #title = request.POST['title']
#         content = util.get_entry(title)
#         return render(request, "encyclopedia/edit.html", {
#             "title": title,
#             "content": content
#         })


def random_page(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    converted_page = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": converted_page
    })
