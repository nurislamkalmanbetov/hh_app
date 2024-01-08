from applications.accounts.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
# from schedule.models import Event



User = get_user_model()



class EmployerProfileSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'icon',
            'first_name',
            'last_name',
            'name',
        ]

class EmployerCompanySerialzers(serializers.ModelSerializer):
    iin = serializers.CharField(required=False, allow_blank=True)
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

class EmployerUpdateSerialzers(serializers.ModelSerializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        iin = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        icon = serializers.ImageField(required=False, allow_null=True)


    
        class Meta:
            model = EmployerCompany
            fields = [
                'id',
                'first_name',
                'last_name',
                'name',
                'iin',
                'description',
                'icon',
            ]


class CitySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = [
            'id',
            'name',
        ]

class BranchSerializers(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name', required=False, allow_null=True)
    

    class Meta:
        model = Branch
        fields = [
            'id',
            'city',
            'company',
            'name',
            'address',
            'link_address',
            'description',
        ]
    #если iin 
    def create(self, validated_data):
        city = validated_data.pop('city')
        city = City.objects.get(name=city['name'])
        branch = Branch.objects.create(city=city, **validated_data)
        return branch
    
    def update(self, instance, validated_data):
        city_data = validated_data.pop('city', None)
        if city_data:
            city = City.objects.get(name=city_data['name'])
            instance.city = city
        else:
            instance.city = None
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.link_address = validated_data.get('link_address', instance.link_address)
        instance.description = validated_data.get('description', instance.description)
    
        instance.save()
        return instance
    

#серилайзер для гет запроса где только название филиала и город
class BranchListSerializers(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    class Meta:
        model = Branch
        fields = [
            'id',
            'city',
            'name',
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


    

class VacancySerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='employer_company.user.id')
    class Meta:
        model = Vacancy
        fields = [
            'user_id', 
            'name', 
            'branch',
            'position', 
            'duty', 
            'experience', 
            'clothingform', 
            'employee_count',
            'time_start', 
            'time_end', 
            'salary', 
            'salary_increase', 
            'description',
            'views_vacancy',

            ]

    def create(self, validated_data):
        user_id = validated_data.pop('employer_company')['user']['id']
        user = User.objects.get(id=user_id)
        employer_company = EmployerCompany.objects.get(user=user)
        vacancy = Vacancy.objects.create(employer_company=employer_company, **validated_data)
        return vacancy
        

