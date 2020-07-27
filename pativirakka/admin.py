from django.contrib import admin
from .models import Experience, Skills, Person, Education, Social_links, Add_more

admin.AdminSite.site_header = "Pativirakka Admin"
admin.AdminSite.site_title = "Pativirakka Site Admin"
admin.AdminSite.index_title = "Site Pativirakka"


@admin.register(Experience, Skills, Education, Person, Social_links, Add_more)
class modelAdmins(admin.ModelAdmin):
    pass
