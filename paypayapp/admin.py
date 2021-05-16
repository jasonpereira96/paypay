from django.contrib import admin


from .models import Employee
from .models import Rating
from .models import Question
from .models import Answer
from .models import PerformanceReview
from .models import PerformanceReviewSubmission

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id', 'email')
    list_filter = ['first_name']
    filter_horizontal = ('reviewers',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer_rating')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'id')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Rating)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(PerformanceReview)
admin.site.register(PerformanceReviewSubmission)


