from django.urls import path

from . import views

app_name = 'copysite'

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('detailauthor/<int:author_id>', views.detailauthor, name='detailauthor'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
 ]