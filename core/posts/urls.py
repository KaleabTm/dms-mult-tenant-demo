from django.urls import path
from .apis import PostCreateView, PostView


urlpatterns=[
    path('view/',PostView.as_view(),name='all posts view'),
    path('create/',PostCreateView.as_view(), name='create post')
]