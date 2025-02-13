from django.urls import path
from main_app.views import *

app_name = 'main_app'


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('search/all', AllDiseasesView.as_view(), name='search_all'),
    path('search', SearchView.as_view(), name='search'),
]

