from app import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin', admin.site.urls),
    # 1
    path('user/create', views.create_user),
    path('post/create', views.create_post),
    # Add remaining endpoints here
    # 2
    path('users/top', views.get_top_users),
    # 3
    path('users/follow', views.follow_user),
    # 4
    path('users/feed/<int:pk>', views.user_feeds),
]
