from django.contrib import admin
from .models import Author, Tag, Quotes

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Quotes)
