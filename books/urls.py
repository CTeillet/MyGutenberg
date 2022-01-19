from django.urls import path

from .views import BooksView, SearchBook

urlpatterns = [
    path('', BooksView.as_view(), name='books'),
    path('search', SearchBook.as_view(), name='search'),
]
