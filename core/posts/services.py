from .models import Post
from core.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

Employee = get_user_model()

def create_post(
        *,
        title=str,
        content=str,
        author,
)-> Post:
    post_author = Employee.objects.get(email=author.email)
    post = Post.objects.create(
        title=title,
        content=content,
        author=post_author,
    )

    post.full_clean()
    post.save()

    return post


def get_post(title: str) -> Post:
    try:
        post = Post.objects.get(title=title)
        return post
    except ObjectDoesNotExist:
        return None 