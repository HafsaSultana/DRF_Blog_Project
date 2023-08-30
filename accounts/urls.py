from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import UserRegister, UserLoginView, BlogPostList, BlogPostDetail, BlogPostViewset

router = routers.SimpleRouter()
router.register(r'blogs', BlogPostViewset)

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('blogs/', BlogPostList.as_view(), name='blogs_list'),
    # path('blogs/<int:pk>/', BlogPostDetail.as_view(), name='blogs_details'),
]

urlpatterns = router.urls



"""
//user reg:
{
    "username":"Tuli",
    "email":"tuli@gmail.com",
    "password":123,
    "role":3
}

//blog create:
{
    "title": "Congratulations",
    "content": "Hi Hafsa! Congratulations to your success!",
    "author" : 3
}

"""
