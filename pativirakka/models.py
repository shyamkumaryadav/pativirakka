import secrets
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core import validators
User = get_user_model()

SKILL_LEVEL = [
    ("", "Skill levels"),
    ("b", "Beginner"),
    ("e", "Elementary"),
    ("pi", "Pre-intermediate"),
    ("i", "Intermediate"),
    ("ui", "Upper-intermediate"),
    ("a", "Advanced"),
]

def upload_to(instance, filename):
    return f"{secrets.token_hex()}-{instance.user.first_name}-{instance.user.last_name}-{secrets.token_hex()}.{filename.split('.')[-1]}"


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.FileField(upload_to=upload_to, default='default.png', blank=True, null=True, help_text='Only Image (png, jpe, jpg, jpeg) extensions',
        validators=[validators.FileExtensionValidator(allowed_extensions=validators.get_available_image_extensions(), message="'%(extension)s' not valid Profile Image.")])
    

    def __str__(self):
        return self.user.__str__()

class Experience(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    company = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()
    description = RichTextField()

    def __str__(self):
        return self.title
    


class Education(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    institute = models.CharField(max_length=225)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    branche = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.institute
    


class Skills(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    language = models.CharField(max_length=225)
    logo = models.CharField(max_length=100,
    help_text="Find Logo on <a href=\"javascript:console.log('Lol...');\" onclick=\"this.href = 'https://fontawesome.com/icons?d=gallery&q='+document.getElementById('id_language').value+'&m=free';console.log(this.href);\" target=\"_blank\">Font Awesome</a>")
    level = models.CharField(
        max_length=2,
        choices=SKILL_LEVEL,
        help_text="<b>Beginner Elementary Pre-intermediate</b> try to <u>not Include</u>",
    )

    def __str__(self):
        return self.language
    


class Social_links(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    url = models.CharField(max_length=225)

    def __str__(self):
        return "@" + self.username
    


class Add_more(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    description = RichTextField()

    def __str__(self):
        return self.title
    
    