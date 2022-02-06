from django.urls import path

from .views import BooksView, SearchBook, AdvancedSearchBook, SearchBookByLanguage, AddBookClick, SearchByTitle, \
    LanguageView, ShowBook

urlpatterns = [
    path('', BooksView.as_view(), name='books'),
    path('search/<str:word_req>', SearchBook.as_view(), name='search'),
    path('advanced-search/<str:expression>', AdvancedSearchBook.as_view(), name='advanced-search'),
    path('search-language/<str:language>', SearchBookByLanguage.as_view(), name='search-language'),
    path('add-click/<int:book_id>', AddBookClick.as_view(), name='add-click'),
    path('search-title/<str:title>', SearchByTitle.as_view(), name='search-title'),
    path('languages', LanguageView.as_view(), name='languages'),
    path('<int:book_id>', ShowBook.as_view(), name='book-detail'),
]
