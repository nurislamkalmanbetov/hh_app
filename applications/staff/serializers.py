from rest_framework import serializers
from applications.accounts.models import *
from applications.core.models import *
from .models import *
from applications.accounts.serializers import UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Подставьте соответствующий сериализатор для модели User

    class Meta:
        model = Employee
        fields = ['id', 'user', 'first_name', 'last_name', 'middle_name', 'email', 'department', 'position', 'birthday', 'mobile_phone', 'internal_phone', 'is_created', 'is_updated', 'is_deleted']



class StaffEmployerUpdateSerialzers(serializers.ModelSerializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        position = serializers.CharField(required=False)
        contact_info = serializers.CharField(required=False, allow_blank=True)
        contact_person = serializers.CharField(required=False, allow_blank=True)
        name = serializers.CharField(required=False)
        iin = serializers.CharField(required=False, allow_blank=True)
        payment_info = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        icon = serializers.ImageField(required=False, use_url=True,allow_null=True)



        class Meta:
            model = EmployerCompany
            fields = [
                'id',
                'first_name',
                'last_name',
                'position',
                'contact_info',
                'contact_person',
                'name',
                'iin',
                'payment_info',
                'description',
                'icon',
            ]

        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.position = validated_data.get('position', instance.position)
            instance.contact_info = validated_data.get('contact_info', instance.contact_info)
            instance.contact_person = validated_data.get('contact_person', instance.contact_person)
            instance.name = validated_data.get('name', instance.name)
            instance.iin = validated_data.get('iin', instance.iin)
            instance.payment_info = validated_data.get('payment_info', instance.payment_info)
            instance.description = validated_data.get('description', instance.description)
            instance.icon = validated_data.get('icon', instance.icon)
            instance.save()
            return instance