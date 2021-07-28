from django.urls import path
from . import views
from .views import ResourceListView

app_name = 'resources'
urlpatterns = [
    path('', ResourceListView.as_view(), name='resource-list')
]
