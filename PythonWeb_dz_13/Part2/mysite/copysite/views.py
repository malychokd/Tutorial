from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Author, Quotes, Tag


def index(request, page=1):
    quotes = Quotes.objects.all()
    return render(request, 'copysite/index.html', {"quotes": quotes})

def detail(request, quote_id):
    quote = get_object_or_404(Quotes, pk=quote_id)
    return render(request, "copysite/detail.html", {"quote": quote})

def detailauthor(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "copysite/detailauthor.html", {"author": author})

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='copysite:index')
        else:
            return render(request, 'copysite/tag.html', {'form': form})

    return render(request, 'copysite/tag.html', {'form': TagForm()})

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='copysite:index')
        else:
            return render(request, 'copysite/author.html', {'form': form})
    return render(request, 'copysite/author.html', {'form': AuthorForm()})

def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    print(authors)

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.save()
            return redirect(to='copysite:index')
        else:
            return render(request, 'copysite/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'copysite/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})

def delete_quote(request, quote_id):
    Quotes.objects.get(pk=quote_id).delete()
    return redirect(to='copysite:index')

