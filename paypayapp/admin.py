from django.contrib import admin


from .models import Employee
from .models import Rating
from .models import Question
from .models import Answer
from .models import PerformanceReview
from .models import PerformanceReviewSubmission

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_filter = ['first_name']
    filter_horizontal = ('reviewers',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Rating)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(PerformanceReview)
admin.site.register(PerformanceReviewSubmission)


