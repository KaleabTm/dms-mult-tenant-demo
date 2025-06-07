from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from core.tenants.service import tenant_create

class TenantCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        tenant_name_am = serializers.CharField(required=True)
        tenant_name_en = serializers.CharField(required=True)
        phone_number = serializers.IntegerField(required=False)
        domain_url = serializers.CharField(required=True)
        on_trial=serializers.BooleanField(required=False, allow_null=True)
        paid_until=serializers.DateField(required=False, allow_null=True)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tenant = tenant_create(**serializer.validated_data)
        response = {
            "detail": "Tenant created successfully",
            "tenant":tenant.data
        }
        return Response(data=response, status=http_status.HTTP_201_CREATED)
        
