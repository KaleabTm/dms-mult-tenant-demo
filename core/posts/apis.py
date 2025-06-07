from guardian.shortcuts import assign_perm
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import create_post, get_post

# Create your views here.


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        content = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        title = serializers.CharField()
        content = serializers.CharField()

    def post(self, request):
        serializer_class = self.InputSerializer(data=request.data)

        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer_class.validated_data

        if not request.user.has_perm("posts.can_create_post"):
            return Response(
                {"error": "You do not have permission to create posts."},
                status=status.HTTP_403_FORBIDDEN,
            )

        post = create_post(
            title=data["title"],
            content=data["content"],
            author=request.user,
        )
        output_serializer = self.OutputSerializer(post)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class PostView(APIView):
    class OutputSerializer(serializers.Serializer):
        title = serializers.CharField()
        content = serializers.CharField()

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()

    def get(self, request):
        serializer_class = self.InputSerializer(data=request.data)
        if request.user.users_permissions.is_staff:
            assign_perm("can_view_post", request.user)

        if not request.user.has_perm("can_view_post"):
            return PermissionDenied()

        if not serializer_class.is_valid():
            # print("Validation Errors:", serializer_class.errors)  # Log for debugging
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer_class.validated_data
        title = data["title"]

        post = get_post(title)

        if post:
            if not request.user.has_perm("can_view_post", post):
                return Response(
                    {"error": "You do not have permission to view this post"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            post_instance = self.OutputSerializer(post)
            return Response(post_instance.data, status=status.HTTP_200_OK)
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
