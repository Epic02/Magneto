from django.urls import path, include

from . import views


urlpatterns = [
    # URLs
    path('', views.UserView.as_view(), name='user-crud'),
    path('<int:user_id>', views.UserView.as_view(), name='user-crud'),
]
