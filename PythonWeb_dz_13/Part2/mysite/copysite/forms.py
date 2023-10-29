from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Tag, Quotes, Author


class TagForm(ModelForm):

    name = CharField(min_length=1, max_length=55, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']

class QuoteForm(ModelForm):

    text = CharField(min_length=5, max_length=300, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all(), widget=TextInput())
    
    class Meta:
        model = Quotes
        fields = ['text', 'author']
        exclude = ['tags']

class AuthorForm(ModelForm):

    fullname = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    born = CharField(min_length=5, max_length=30, required=True, widget=TextInput())
    location = CharField(min_length=5, max_length=150, required=True, widget=TextInput())
    bio = CharField(min_length=10, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname','born','location', 'bio']