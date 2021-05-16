from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=10000)
    last_name = models.CharField(max_length=10000)
    deleted = models.BooleanField(default=False)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    password = models.CharField(max_length=10000, default="test123")
    reviewers = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Rating(models.Model):
    rating_text = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.rating_text

class Question(models.Model):
    question_text = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=10000)

class PerformanceReview(models.Model):
    title = models.CharField(max_length=10000)
    questions = models.ManyToManyField(Question,  blank=True)

    def __str__(self):
        return self.title

class PerformanceReviewSubmission(models.Model):
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="fk_employee_submission")
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_data = models.TextField(default='')
