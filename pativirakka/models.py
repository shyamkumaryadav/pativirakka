import secrets
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.template.defaultfilters import filesizeformat, truncatechars_html
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe, escape
from django.core import validators
from django.contrib.auth.models import AbstractUser


SIZE_OK = 1024 * 1024 * 0.75


SKILL_LEVEL = [
    ("", "Skill levels"),
    ("b", "Beginner"),
    ("e", "Elementary"),
    ("pi", "Pre-intermediate"),
    ("i", "Intermediate"),
    ("ui", "Upper-intermediate"),
    ("a", "Advanced"),
]

LANGUAGE_TAGS = [
    (None, "Language tags"),
    ('<i class="fab fa-python"></i>', 'Python')
]

SOCIAL_TAGS = [
    (None, "Social Tages"),
    ('<i class="fab fa-docker"></i>', 'Docker'),
    ('<i class="fab fa-facebook-f"></i>', 'Facebook'),
    ('<i class="fab fa-gitlab"></i>', 'GitLab'),
    ('<i class="fab fa-github"></i>', 'GitHub'),
    ('<i class="fab fa-instagram"></i>', 'Instagram'),
    ('<i class="fab fa-linkedin-in"></i>', 'LinkedIN'),
    ('<i class="fab fa-npm"></i>', 'NPM'),
    ('<i class="fab fa-patreon"></i>', 'Patreon'),
    ('<i class="fab fa-python"></i>', 'Python'),
    ('<i class="fab fa-telegram"></i>', 'Telegram'),
    ('<i class="fab fa-twitch"></i>', 'Twitch'),
    ('<i class="fab fa-twitter"></i>', 'Twitter'),
    ('<i class="fab fa-youtube"></i>', 'YouTube')
]


def upload_to(instance, filename):
    return f"{instance.first_name}-{instance.last_name}-{secrets.token_hex()}.{filename.split('.')[-1]}"


def SizeOk(value):
    if value.size > SIZE_OK:
        raise ValidationError(
            f"Your Image size is {filesizeformat(value.size)} > {filesizeformat(SIZE_OK)}")


class User(AbstractUser):
    address = models.TextField(max_length=150, null=True, blank=True)
    about = RichTextField(null=True, blank=True)
    email = models.EmailField(verbose_name='email address')
    is_email = models.BooleanField(verbose_name="Email verification",
                                   help_text='Designates whether this user email should be treated as active.', default=False)
    profile = models.FileField(upload_to=upload_to, default='default.png', blank=True, null=True, help_text=f'Size <b>{filesizeformat(SIZE_OK)}</b> or less.[500 x 500]',
                               validators=[validators.FileExtensionValidator(allowed_extensions=validators.get_available_image_extensions(), message="'%(extension)s' not valid Profile Image."), SizeOk])

    def __str__(self):
        return self.username

    def image_tag(self):
        return mark_safe('<img src="{}" width="200px" />'.format(escape(self.profile.url)))
    image_tag.short_description = 'Profile'
    image_tag.allow_tags = True


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    company = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True, null=True, help_text="For Present Date blank this Field.")
    description = RichTextField(config_name="my-custom-toolbar")

    def __str__(self):
        return self.title


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=225)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    branche = models.CharField(max_length=225, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True, null=True, help_text="For Present Date <a href='javascript:void(0);' onclick=\"var tag_id=this.parentNode.parentNode.getElementsByTagName('input')[0].id.split('-').slice(0, -1);tag_id.push('end_date');document.getElementById(tag_id.join('-')).value = '';\"><u>Blank</u></a> this Field.")

    def __str__(self):
        return self.institute


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=225)
    logo = models.CharField(max_length=100, blank=True, choices=SOCIAL_TAGS,
                            help_text="Find Logo on <a href='#' onclick=\"var tag_id=this.parentNode.parentNode.getElementsByTagName('input')[0].id.split('-').slice(0, -1);tag_id.push('language');this.href = 'https://fontawesome.com/icons?d=gallery&q='+document.getElementById(tag_id.join('-')).value+'&s=brands&m=free';\" target=\"_blank\">Font Awesome</a><b> Ex.: python '&lt;i class=&#x27;fab fa-python&#x27;&gt;&lt;/i&gt;'</b>")
    level = models.CharField(
        max_length=2,
        choices=SKILL_LEVEL,
        help_text="<b>Beginner Elementary Pre-intermediate</b> try to <u>not Include</u>",
    )

    class META:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.language


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    logo = models.CharField(max_length=100, choices=SOCIAL_TAGS)
    url = models.URLField()

    def __str__(self):
        return "@" + self.username


class AddMore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    description = RichTextField()

    def __str__(self):
        return self.title


class AwardCertification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=110)

    def __str__(self):
        return self.name


class PativirakkaFrom(models.Model):
    from_user = models.CharField(max_length=16, blank=True, null=True)
    contect = models.CharField(max_length=220)
    limit = models.IntegerField(default=1)
    limit_number = models.IntegerField(default=10)


    def __str__(self):
        return self.from_user or '-'

    def save(self, *args, **kwargs):
        self.from_user = self.contect.split(':')[-1]
        super().save(*args, **kwargs)

    def _is_limit(self):
        return self.limit <= self.limit_number

    _is_limit.boolean = True
    _is_limit.short_description = "Limit Not Done"
    is_limit = property(_is_limit)
