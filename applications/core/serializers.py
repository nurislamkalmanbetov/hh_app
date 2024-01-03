from applications.accounts.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
# from schedule.models import Event



User = get_user_model()


class EmployerCompanySerialzers(serializers.ModelSerializer):

    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'name',
            'iin',
            'description',
            'icon',
        ]

    # def create(self, validated_data):
    #     user_email = validated_data.pop('user', None)  # Обратите внимание на изменение 'user.email' на 'user'
    #     user = User.objects.get(email=user_email)
    #     employercompany = EmployerCompany.objects.create(user=user, **validated_data)
    #     return employercompany

    # def update(self, instance, validated_data):
    #     user_email = validated_data.pop('user', None)  # Извлекаем email, если он передан

    #     if user_email:  # Если email был передан, обновляем пользователя
    #         user = User.objects.get(email=user_email)
    #         instance.user = user

    #     # Обновление остальных полей
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()  # Сохраняем изменения
    #     return instance



class BranchSerializers(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = [
            'id',
            'company',
            'name',
            'address',
            'link_address',
            'description',
        ]   
    

class ReviewBranchSerializers(serializers.ModelSerializer):

    class Meta:
        model = ReviewBranch
        fields = [
            'id',
            'branch',
            'user',
            'review',
            'created_date',
        ]


class RatingEmployerCompanySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = RatingEmployerCompany
        fields = [
            'id',
            'company',
            'user',
            'rating',
        ]   


class RatingEmployerCompanySerializers(serializers.ModelSerializer):
        
        class Meta:
            model = RatingEmployerCompany
            fields = [
                'id',
                'company',
                'user',
                'rating',
            ]


class PositionEmployeeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = PositionEmployee
        fields = [
            'id',
            'employer',
            'name',

        ]


class DutyEmployeeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = DutyEmployee
        fields = [
            'id',
            'employer',
            'name',
            'description',

        ]

class ClothingFormSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = ClothingForm
        fields = [
            'id',
            'name',
            'description',

        ]



