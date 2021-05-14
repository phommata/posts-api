from app.models import Post
from app.serializers import PostSerializer, UserSerializer, UserFollowSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated


# 1
@api_view(["POST"])
def create_user(request):
    # pass
    data = JSONParser().parse(request)
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "User created"}, status=status.HTTP_201_CREATED)
    else:
        data = {
            "error": True,
            "errors": serializer.errors,
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, ])
def create_post(request):
    data = JSONParser().parse(request)
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Post created"}, status=status.HTTP_201_CREATED)
    else:
        data = {
          "error": True,
          "errors": serializer.errors,
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

# 2
def get_top_users(request):
    users = User.objects.values('username').annotate(posts=Count('posts')).filter(posts__gt=1)
    users_list = list(users) # important: convert the QuerySet to a list object
    return JsonResponse(users_list, status=status.HTTP_200_OK, safe=False)

# 3
@api_view(["POST"])
def follow_user(request):
    data = JSONParser().parse(request)
    serializer = UserFollowSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "User followed"}, status=status.HTTP_200_OK)
    else:
        data = {
          "error": True,
          "errors": serializer.errors,
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

# 4
@api_view(["GET"])
def user_feeds(request, pk=None):
    posts = Post.objects \
        .values('liked_by') \
        .annotate(likes=Count('liked_by')) \
        .filter(Q(user__follow__user=pk) | Q(user=pk)) \
        .order_by('-timestamp') \
        .values('id', 'body', 'user__username', 'likes')
    posts_list = list(posts)  # important: convert the QuerySet to a list object
    return JsonResponse(posts_list, status=status.HTTP_200_OK, safe=False)