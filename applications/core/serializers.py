from applications.accounts.models import User
from applications.accounts.models import Profile
from rest_framework import serializers
from applications.accounts.serializers import ProfileListSerializer
from .models import *
from django.contrib.auth import get_user_model




User = get_user_model()


class InvitationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all(), write_only=True)
    employer_email = serializers.EmailField(source='employer.user.email', write_only=True)
    employer_name = serializers.CharField(source='employer.name', read_only=True)
    vacancy_name = serializers.CharField(source='vacancy.name', read_only=True)
    
    class Meta:
        model = Invitation
        fields = ['id', 'user_email', 'message', 'status', 'vacancy_id', 'employer_email', 'employer_name', 'vacancy_name']

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        employer_email = validated_data.pop('employer').get('user').get('email')
        employer = EmployerCompany.objects.get(user__email=employer_email)
        vacancy_id = validated_data.pop('vacancy_id').id

        try:
            user = User.objects.get(email=user_email, is_student=True, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found")

        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("Vacancy not found")

        status = validated_data.get('status')
        invitation = Invitation.objects.create(user=user, vacancy=vacancy, employer=employer, **validated_data)

        # Генерируем сообщение в зависимости от статуса
        if status == 'accepted':
            message = (f'Уважаемый(ая) {user.email}, '
                    f'мы внимательно изучили ваше резюме и были впечатлены вашими достижениями и опытом. '
                    f'С удовольствием приглашаем вас на собеседование в компанию {employer.name} '
                    f'на вакансию {vacancy.name}. Мы с нетерпением ожидаем встречи с вами и обсуждения деталей вашего возможного присоединения к нашей команде.')
        elif status == 'declined':
            message = (f'Уважаемый(ая) {user.email}, '
                    f'благодарим вас за проявленный интерес к вакансии {vacancy.name} в компании {employer.name}. '
                    f'После тщательного рассмотрения ряда кандидатур, к сожалению, мы приняли решение '
                    f'продолжить поиск. Это решение никак не отражает вашей квалификации, и мы надеемся на возможность сотрудничества в будущем. '
                    f'Желаем вам успехов и быстро найти подходящую позицию.')
        else:
            message = (f'Уважаемый(ая) {user.email}, '
                    f'рады сообщить вам, что вы были отобраны на рассмотрение для вакансии {vacancy.name} в компании {employer.name}. '
                    f'Пожалуйста, дайте нам знать о вашей готовности пройти собеседование и продолжить этот важный процесс.')

        invitation.message = message
        invitation.save()

        return invitation


class InvatationGetSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    employer_email = serializers.EmailField(source='employer.user.email')
    
    class Meta:
        model = Invitation
        fields = ['id', 'user_email', 'message', 'status', 'vacancy', 'employer_email']


class EmployerCompanySerialzers(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'user',
            # 'image_back',
            'icon',
            'name',
            'country',
            'description',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user', None)  # Обратите внимание на изменение 'user.email' на 'user'
        user = User.objects.get(email=user_email)
        employercompany = EmployerCompany.objects.create(user=user, **validated_data)
        return employercompany

    def update(self, instance, validated_data):
        user_email = validated_data.pop('user', None)  # Извлекаем email, если он передан

        if user_email:  # Если email был передан, обновляем пользователя
            user = User.objects.get(email=user_email)
            instance.user = user

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # Сохраняем изменения
        return instance

class CompanyReviewSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')
    
    class Meta:
        model = CompanyReview
        fields = ['id', 'company', 'user', 'rating', 'comment', 'created_date']

    def create(self, validated_data):
        user_email = validated_data.pop('user')
        user = User.objects.get(email=user_email)
        company_review= CompanyReview.objects.create(user=user, **validated_data)  # Используем **validated_data
        return company_review
    


class VacancySerializers(serializers.ModelSerializer):
    # employer_company = EmployerCompanySerialzers(read_only=True)
    user = serializers.EmailField(source='employer_company.user.email')


    class Meta:
        model = Vacancy
        fields = [
            'id',
            'user',
            'picture',
            'name', 
            'salary', 
            'exchange',
            'duty', 
            'city', 
            'language',
            'proficiency',
            'accomodation_type', 
            'accomodation_cost', 
            'is_vacancy_confirmed', 
            'insurance',
            'required_positions',
            'transport', 
            'contact_info', 
            'destination_point', 
            'employer_dementions', 
            'extra_info',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('employer_company').get('user').get('email')
        user = EmployerCompany.objects.get(user__email=user_email)
        vacancy = Vacancy.objects.create(employer_company=user, **validated_data)
        return vacancy
    

    def update(self, validated_data):
        user_email = validated_data.pop('employer_company').get('user').get('email')
        user = User.objects.get(email=user_email)
        vacancy = Vacancy.objects.update(employer_company=user.employer_company, **validated_data)
        return vacancy


class VacancyFilterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyChangeSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='employer_company.user.email', read_only=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'picture','user', 'name', 'salary','exchange', 'city', 'accomodation_cost', 'insurance', 'transport',
                  'contact_info', 'destination_point', 'employer_dementions', 'extra_info', 'duty', 'language','required_positions',
                  'proficiency', 'accomodation_type',
        ]



class ReviewVacancySerializer(serializers.ModelSerializer):
    applicant_profile_email = serializers.EmailField(source='applicant_profile.user.email')
    employer_email = serializers.EmailField(source='employer.email')
    applicant_profile_data = ProfileListSerializer(source='applicant_profile', read_only=True)
    vacancy_name = serializers.CharField(source='vacancy.name', read_only=True )

    

    class Meta:
        model = ReviewVacancy
        fields = [
            'id',
            'status',
            'vacancy',
            'vacancy_name',
            'employer_comment',
            'applicant_profile_email',
            'applicant_profile_data',  # Добавляем поле для адреса электронной почты профиля соискателя
            'employer_email',  # Добавляем поле для адреса электронной почты работодателя
        ]

    def create(self, validated_data):
        # Извлекаем почтовые адреса
        applicant_profile_email = validated_data.pop('applicant_profile').get('user').get('email')
        employer_email = validated_data.pop('employer').get('email')

        # Находим соответствующие объекты по почтовым адресам
        applicant_profile = Profile.objects.get(user__email=applicant_profile_email)
        employer = User.objects.get(email=employer_email)

        review_vacancy = ReviewVacancy.objects.create(
            applicant_profile=applicant_profile,
            employer=employer,
            **validated_data
        )

        return review_vacancy


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'text', 'user', 'created_at', 'status')

class ImprovementIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementIdea
        fields = ('id', 'text', 'user', 'created_at', 'status')