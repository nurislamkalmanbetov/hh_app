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


    


class VacancySerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='employer_company.user.id')

    class Meta:
        model = Vacancy
        fields = [
            'user_id', 
            'branch',
            'position', 
            'duty', 
            'experience', 
            'clothingform', 
            'employee_count',
            'time_start', 
            'time_end', 
            'salary', 
            'increase_choices', 
            'description',

            ]
    

    def create(self, validated_data):
        user_id = validated_data.pop('employer_company')['user']['id']
        user = User.objects.get(id=user_id)
        employer_company = EmployerCompany.objects.get(user=user)
        vacancy = Vacancy.objects.create(employer_company=employer_company, **validated_data)
        return vacancy

    def update(self, instance, validated_data):
        instance.branch = validated_data.get('branch', instance.branch)
        instance.position = validated_data.get('position', instance.position)
        instance.duty = validated_data.get('duty', instance.duty)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.clothingform = validated_data.get('clothingform', instance.clothingform)
        instance.employee_count = validated_data.get('employee_count', instance.employee_count)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.increase_choices = validated_data.get('increase_choices', instance.increase_choices)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class VacancyDetailSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='employer_company.user.id')
    employer_company_icon = serializers.ImageField(source='employer_company.icon')
    employer_company_name = serializers.CharField(source='employer_company.name')
    branch = serializers.CharField(source='branch.name')
    branch_city = serializers.CharField(source='branch.city.name')
    branch_address = serializers.CharField(source='branch.address')
    position = serializers.CharField(source='position.name')
    created_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'user_id', 
            'employer_company_name',
            'employer_company_icon',
            'branch',
            'branch_city',
            'branch_address',
            'position', 
            'duty', 
            'experience', 
            'clothingform', 
            'employee_count',
            'time_start', 
            'time_end', 
            'salary', 
            'increase_choices', 
            'description',
            'views_vacancy',
            'created_date',


            ]
    
    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")




class VacancyListSerializers(serializers.ModelSerializer):
    employer_company_icon = serializers.ImageField(source='employer_company.icon')
    employer_company_name = serializers.CharField(source='employer_company.name')
    branch = serializers.CharField(source='branch.name')
    branch_city = serializers.CharField(source='branch.city.name')
    branch_address = serializers.CharField(source='branch.address')
    position = serializers.CharField(source='position.name')
    created_date = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Vacancy
        fields = [
            'id',
            'employer_company_name',
            'employer_company_icon',
            'branch',
            'branch_city',
            'branch_address',
            'position', 
            'experience', 
            'employee_count',
            'time_start', 
            'time_end', 
            'salary', 
            'views_vacancy',
            'created_date',
            ]
    
    
    def get_created_date(self, obj):
        return obj.created_date.strftime("%d.%m.%Y")

