from django.urls import path
from .views import *

urlpatterns = [
    path('', MusicManiaView.as_view()),
    path('category/<int:pk>', MusicManiaCatView.as_view()),
    path('listen_later', MusicManiaListenLaterView.as_view()),
    path('listen_later/remove', MusicManiaListenRemoveView.as_view()),
    path('autosuggest', MusicManiaAutosuggestSearchView.as_view()),
]