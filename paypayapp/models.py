from django.db import models

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=10000)
    last_name = models.CharField(max_length=10000)
    email = models.EmailField()
    reviewers = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Rating(models.Model):
    rating_text = models.CharField(max_length=10000)

class Question(models.Model):
    question_text = models.CharField(max_length=10000)

class Answer(models.Model):
    answer_text = models.ForeignKey(Rating, on_delete=models.CASCADE)

class PerformanceReview(models.Model):
    title = models.CharField(max_length=10000)
    questions = models.ManyToManyField(Question,  blank=True)

class PerformanceReviewSubmission(models.Model):
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="fk_employee_submission")
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer,  blank=True)
