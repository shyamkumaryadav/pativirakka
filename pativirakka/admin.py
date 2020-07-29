from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Experience, Skill, Person, Education, SocialLink, AddMore, AwardCertification

admin.site.site_header = "Pativirakka Admin"
admin.site.site_title = "Pativirakka Site Admin"
admin.site.index_title = "Site Pativirakka"
User = get_user_model()


class TabEducation(admin.StackedInline):
    model = Education
    extra = 1
    min = 1


class TabSkills(admin.StackedInline):
    model = Skill
    extra = 1
    num = 1


class TabExperience(admin.StackedInline):
    model = Experience
    extra = 0
    classes = ('collapse',)


class TabSocial_links(admin.StackedInline):
    model = SocialLink
    extra = 0
    classes = ('collapse',)

class TabAwardCertification(admin.StackedInline):
    model = AwardCertification
    extra = 0
    classes = ('collapse',)

class TabAdd_more(admin.StackedInline):
    model = AddMore
    extra = 0
    classes = ('collapse',)


@admin.register(Person)
class PersonAdmins(admin.ModelAdmin):
    inlines = [TabEducation, TabSkills,
               TabExperience, TabSocial_links, TabAwardCertification, TabAdd_more]
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('image_tag', 'user', 'profile')
        }),
    )
