from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.users.models.user import User

from .selectors import user_list, user_profile_details
from .serializers import UserDetailSerializer, UserListSerializer
from .services import user_create, user_update


class UserListApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        filter = serializers.ChoiceField(
            choices=[
                ("all", "All users"),
                ("staff", "Staff only"),
                ("admin", "Admin only"),
                ("staff_and_admin", "Staff and Admin"),
            ],
            required=True,
        )
        include_current_user = serializers.BooleanField(required=False, default=False)

    serializer_class = UserListSerializer
    filter_class = FilterSerializer

    def get(self, request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        try:
            users = user_list(current_user=request.user, filters=filter_serializer.validated_data)

            output_serializer = self.serializer_class(users, many=True)

            response_data = {"users": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

        first_name_en = serializers.CharField()
        middle_name_en = serializers.CharField()
        last_name_en = serializers.CharField()

        first_name_am = serializers.CharField()
        middle_name_am = serializers.CharField()
        last_name_am = serializers.CharField()

        job_title = serializers.UUIDField()
        department = serializers.UUIDField()
        phone_number = serializers.IntegerField()

        is_admin = serializers.BooleanField()
        is_staff = serializers.BooleanField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            user_create(**input_serializer.validated_data)

            response_data = {"message": "User has been successfully added to the tenant."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserDetailApi(ApiAuthMixin, APIView):
    serializer_class = UserDetailSerializer

    def get(self, request, user_id) -> Response:
        try:
            user_instance = user_profile_details(id=user_id)

            output_serializer = UserDetailSerializer(user_instance)

            response_data = {"user": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class UserUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        first_name_en = serializers.CharField()
        middle_name_en = serializers.CharField()
        last_name_en = serializers.CharField()

        first_name_am = serializers.CharField()
        middle_name_am = serializers.CharField()
        last_name_am = serializers.CharField()

        use_email = serializers.BooleanField()
        use_sms = serializers.BooleanField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.prefetch_related(
                "user_profile",
                "users_permissions",
                "user_settings",
                "user_preferences",
            ).get(email=request.user.email)
            user_update(user_instance=user, **input_serializer.validated_data)

            response_data = {"message": "User has been successfully added to the tenant."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)
