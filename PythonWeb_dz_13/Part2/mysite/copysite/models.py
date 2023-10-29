from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False)
    born = models.CharField(max_length=30)
    location = models.CharField(max_length=150, null=True)
    bio = models.TextField()
    
    def __str__(self):
        return f'{self.fullname}'

class Tag(models.Model):
    name = models.CharField(max_length=55, null=False, unique=True)

    def __str__(self):
        return self.name

class Quotes(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.text}'
