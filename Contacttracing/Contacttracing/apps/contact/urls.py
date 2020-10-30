from django.urls import path
from . import views
urlpatterns = [
    path('', views.ContactCheckerView.as_view(), name='contact')
]
