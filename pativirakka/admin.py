from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import Experience, Skill, User, Education, SocialLink, AddMore, AwardCertification, PativirakkaFrom

admin.site.site_header = "Pativirakka Admin"
admin.site.site_title = "Pativirakka Site Admin"
admin.site.index_title = "Site Pativirakka"

admin.site.unregister(Group)


@admin.register(PativirakkaFrom)
class AdminPativirakkaFrom(admin.ModelAdmin):
    list_display = ('__str__', '_is_limit')


class TabEducation(admin.StackedInline):
    model = Education
    extra = 0
    classes = ('collapse',)


class TabSkills(admin.StackedInline):
    model = Skill
    extra = 0
    classes = ('collapse',)


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


@admin.register(User)
class UserAdmins(UserAdmin):
    inlines = [TabEducation, TabSkills,
               TabExperience, TabSocial_links, TabAwardCertification, TabAdd_more]
    readonly_fields = ('image_tag','id')
    fieldsets = (
        (None, {'fields': ('id', 'image_tag', 'username', 'email', 'password', 'profile')}),
        ('Personal info', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'address', 'about')}),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
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
