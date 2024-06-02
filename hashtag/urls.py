from django.urls import path
from .views import HashtagView, HashtagSearchView

urlpatterns = [
   path('', HashtagView.as_view(), name='Hashtag'),
   path('<str:tag>', HashtagView.as_view(), name='Hashtag'),
   path('search/', HashtagSearchView.as_view(), name='HashtagSearch'),
]