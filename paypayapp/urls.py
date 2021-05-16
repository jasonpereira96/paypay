from rest_framework import status
from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.views import obtain_auth_token 
from .models import Employee, PerformanceReviewSubmission, PerformanceReview, Question, Rating
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token

def getReviewees(employee_id):
    employees = Employee.objects
    reviewees = employees.filter(reviewers__id__contains=employee_id)
    return reviewees

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating_text']


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    reviewers = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Employee.objects.all())

    def create(self, validated_data):
        user = User.objects.create(username=validated_data.get('email'), password='thisisatestpassword')
        user.save()
        employee = Employee.objects.create()    
        employee.first_name = validated_data.get('first_name')
        employee.last_name = validated_data.get('last_name')
        employee.email = validated_data.get('email')
        employee.password = 'test123'
        employee.user = user

        employee.save()
        return employee


    class Meta:
        model = Employee
        fields = ['id', 'reviewers', 'first_name', 'last_name', 'email', 'deleted']


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) #be careful here!

    class Meta:
        model = Question
        fields = ['id', 'question_text']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.deleted = True
        employee.save()
        return Response(data='delete success')

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PerformanceReviewSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=False)
    
    def update(self, instance, validated_data):
        id = instance.id
        questions_data = validated_data.pop('questions')
        performance_review = instance
        # performance_review.questions.clear()

        # for question_data in questions_data:
        #     question_data.pop('id')
        #     question = Question.objects.create(**question_data)
        #     performance_review.questions.add(question)
        
        for question_data in questions_data:
            if 'id' not in question_data:
                question = Question.objects.create(**question_data)
                performance_review.questions.add(question)
            else:
                question = Question.objects.get(id=question_data['id'])
                question_data.pop('id')
                question.question_text = question_data['question_text']
                question.save()

        performance_review.title = validated_data.get('title')
        performance_review.save()
        return performance_review

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        questions = []
        performance_review = PerformanceReview.objects.create()
        performance_review.title = validated_data.get('title')
        performance_review.save()
        for question_data in questions_data:
            question = Question.objects.create(**question_data)
            questions.append(question)
        performance_review.questions.set(questions)
        performance_review.save()
        return performance_review

    class Meta:
        model = PerformanceReview
        fields = ['id', 'title', 'questions']

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer

class PerformanceReviewSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceReviewSubmission
        fields = ['id', 'performance_review', 'employee', 'reviewer', 'review_data']

# ViewSets define the view behavior.
class PerformanceReviewSubmissionViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReviewSubmission.objects.all()
    serializer_class = PerformanceReviewSubmissionSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        try:
            # admin login
            if email == 'admin@paypay.com' and password == 'admin':
                admin_user = User.objects.get(username='admin')
                token = Token.objects.create(user=admin_user)
                return JsonResponse({'loginSuccessful' : True, 'employee': {}, 'token': token.key, 'isAdmin': True })
                
            employee = Employee.objects.get(email=email, password=password)
            serializer = EmployeeSerializer(employee)
            token = Token.objects.create(user=employee.user)
            return JsonResponse({'loginSuccessful' : True, 'employee': serializer.data, 'token': token.key })
        except Exception as e:
            print(e)
            return JsonResponse({'loginSuccessful' : False })
            
class LogoutView(APIView):

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return JsonResponse({'logoutSuccessful' : True })

class PendingReviews(APIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, format=None):
        employee_id = request.query_params['id']
        reviewees = getReviewees(employee_id)
        submissions = PerformanceReviewSubmission.objects
        submissions = submissions.filter(reviewer__id=employee_id)
        serializer = EmployeeSerializer(reviewees, many=True)
        return Response(serializer.data)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'reviews', PerformanceReviewViewSet)
router.register(r'submissions', PerformanceReviewSubmissionViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pending-reviews/', PendingReviews.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]