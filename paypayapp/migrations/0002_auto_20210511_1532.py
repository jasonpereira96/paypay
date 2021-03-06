# Generated by Django 3.1.4 on 2021-05-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paypayapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='reviewers',
            field=models.ManyToManyField(blank=True, related_name='_employee_reviewers_+', to='paypayapp.Employee'),
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='questions',
            field=models.ManyToManyField(blank=True, to='paypayapp.Question'),
        ),
        migrations.AlterField(
            model_name='performancereviewsubmission',
            name='answers',
            field=models.ManyToManyField(blank=True, to='paypayapp.Answer'),
        ),
    ]
