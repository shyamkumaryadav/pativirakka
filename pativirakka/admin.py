from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Experience, Skill, Person, Education, Social_link, Add_more

admin.site.site_header = "Pativirakka Admin"
admin.site.site_title = "Pativirakka Site Admin"
admin.site.index_title = "Site Pativirakka"
User = get_user_model()


class TabEducation(admin.StackedInline):
    model = Education
    extra = 1
    min = 1
    # classes = ('collapse',)


class TabSkills(admin.StackedInline):
    model = Skill
    extra = 1
    num = 1
    # classes = ('collapse',)


class TabExperience(admin.StackedInline):
    model = Experience
    extra = 0
    classes = ('collapse',)


class TabSocial_links(admin.StackedInline):
    model = Social_link
    extra = 0
    classes = ('collapse',)


class TabAdd_more(admin.StackedInline):
    model = Add_more
    extra = 0
    classes = ('collapse',)

# @admin.register(Experience, Skills, Education, Social_links, Add_more)
# class AllAdmin(admin.ModelAdmin):
#     pass


# admin.site.unregister(User)

@admin.register(Person)
class PersonAdmins(admin.ModelAdmin):
    inlines = [TabEducation, TabSkills,
               TabExperience, TabSocial_links, TabAdd_more]
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('image_tag', 'user', 'profile')
        }),
    )