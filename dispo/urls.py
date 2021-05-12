from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/create/', views.create_user),
    path('post/create/', views.create_post),
    # Add remaining endpoints here
]
