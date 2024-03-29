from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import Experience, Skill, User, Education, SocialLink, AddMore, AwardCertification, PativirakkaFrom

admin.site.site_header = "Pativirakka Admin"
admin.site.site_title = "Pativirakka Site Admin"
admin.site.index_title = "Site Pativirakka"

admin.site.unregister(Group)


@admin.register(PativirakkaFrom)
class AdminPativirakkaFrom(admin.ModelAdmin):
    list_display = ('__str__', 'limit', '_is_limit')
    fields = ('from_user', ('limit', 'limit_number'))
    readonly_fields = ('contect', 'from_user')


class TabEducation(admin.StackedInline):
    model = Education
    extra = 1
    fields = (('institute', 'branche'), ('gpa', 'start_date', 'end_date'))
    classes = ('collapse',)


class TabSkills(admin.StackedInline):
    model = Skill
    extra = 1
    fields = (('language', 'level', 'logo'),)
    # classes = ('collapse',)


class TabExperience(admin.StackedInline):
    model = Experience
    extra = 1
    fields = (('title', 'company'), ('start_date', 'end_date'), 'description')
    classes = ('collapse',)


class TabSocial_links(admin.StackedInline):
    model = SocialLink
    extra = 1
    fields = (('username', 'url', 'logo'), )
    classes = ('collapse',)


class TabAwardCertification(admin.StackedInline):
    model = AwardCertification
    extra = 1
    classes = ('collapse',)


class TabAdd_more(admin.StackedInline):
    model = AddMore
    extra = 1
    classes = ('collapse',)


@admin.register(User)
class UserAdmins(UserAdmin):
    inlines = [TabEducation, TabSkills,
               TabExperience, TabSocial_links, TabAwardCertification, TabAdd_more]
    readonly_fields = ('image_tag', 'id')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_email')
    fieldsets = (
        (None, {'fields': ('id', 'image_tag',
                           'username', 'email', 'password', 'profile')}),
        ('Personal info', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'address', 'about')}),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'profile',),
        }),
    )
