from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()

SKILL_LEVEL = [
    ("", "Skill level"),
    ("b", "Beginner"),
    ("e", "Elementary"),
    ("pi", "Pre-intermediate"),
    ("i", "Intermediate"),
    ("ui", "Upper-intermediate"),
    ("a", "Advanced"),
]


class Experience(models.Model):
    title = models.CharField(max_length=225)
    company = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()
    description = RichTextField()


class Education(models.Model):
    institute = models.CharField(max_length=225)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    branche = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()


class Skills(models.Model):
    language = models.CharField(max_length=225)
    logo = models.CharField(max_length=100)
    level = models.CharField(
        max_length=2,
        choices=SKILL_LEVEL,
        help_text="<b>Beginner Elementary Pre-intermediate</b> try to <u>not Include</u>",
    )


class Social_links(models.Model):
    username = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    url = models.CharField(max_length=225)


class Add_more(models.Model):
    title = models.CharField(max_length=225)
    description = RichTextField()


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.ManyToManyField(Education)
    experience = models.ManyToManyField(Experience)
    skills = models.ManyToManyField(Skills)
    social_links = models.ManyToManyField(Social_links)
    add_more = models.ManyToManyField(Add_more)
