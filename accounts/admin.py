from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.


class AccountAdmin(UserAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-raduis:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'last_activity', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ['first_name','last_name','email']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Authenticators', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'matric_number','phone', 'profile_picture', 'city', 'state', 'country','department','faculty','session')}),
        ('School Fees', {'fields':('year1_fee','year2_fee','year3_fee','year4_fee','year5_fee','department_fee','faculty_fee','library_fee','medical_fee')}),
        ('Checks', {'fields': ('date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
    )
    list_per_page = 25

admin.site.register(Account, AccountAdmin)

class SchoolFeesAdmin(admin.ModelAdmin):
    list_display = ('department',)
    list_display_links = ('department',)
    ordering = ('-date',)

    filter_horizontal = ()
    list_filter = ('department',)
    list_per_page = 25
    search_fields = ['department',]

admin.site.register(SchoolFees, SchoolFeesAdmin)

class DepartmentFeesAdmin(admin.ModelAdmin):
    list_display = ('department',)
    list_display_links = ('department',)
    ordering = ('-date',)

    filter_horizontal = ()
    list_filter = ('department',)
    list_per_page = 25
    search_fields = ['department',]

admin.site.register(DepartmentFees, DepartmentFeesAdmin)

class FacultyFeesAdmin(admin.ModelAdmin):
    list_display = ('department',)
    list_display_links = ('department',)
    ordering = ('-date',)

    filter_horizontal = ()
    list_filter = ('department',)
    list_per_page = 25
    search_fields = ['department',]

admin.site.register(FacultyFees, FacultyFeesAdmin)

class libraryFeesAdmin(admin.ModelAdmin):
    list_display = ('department',)
    list_display_links = ('department',)
    ordering = ('-date',)

    filter_horizontal = ()
    list_filter = ('department',)
    list_per_page = 25
    search_fields = ['department',]

admin.site.register(libraryFees, libraryFeesAdmin)

class MedicalFeesAdmin(admin.ModelAdmin):
    list_display = ('department',)
    list_display_links = ('department',)
    ordering = ('-date',)

    filter_horizontal = ()
    list_filter = ('department',)
    list_per_page = 25
    search_fields = ['department',]

admin.site.register(MedicalFees, MedicalFeesAdmin)

class PaystackAdmin(admin.ModelAdmin):
    list_display = ('user','email','service','amount',)
    list_display_links = ('user',)
    ordering = ('-generated',)

    filter_horizontal = ()
    list_filter = ('user',)
    list_per_page = 25
    search_fields = ['user',]

# admin.site.register(Paystack, PaystackAdmin)

class UserhistoryAdmin(admin.ModelAdmin):
    list_display = ('user','email','amount','confirm',)
    list_display_links = ('user',)
    ordering = ('-date_created',)

    filter_horizontal = ()
    list_filter = ('user',)
    list_per_page = 25
    search_fields = ['user',]

admin.site.register(Userhistory, UserhistoryAdmin)