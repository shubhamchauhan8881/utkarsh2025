from django.contrib import admin

# Register your models here.
from . import models
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser



admin.site.site_title = "UTKARSH 2025"
admin.site.site_header = "UTKARSH Administration"
admin.site.index_title = "UTKARH 2025"


class EventsRegistrationsAdmin(admin.ModelAdmin):
    list_display = ["event", "leader", "team_members"]

    def team_members(self, object):
        teams = models.TeamMembers.objects.filter(event = object)
        if teams:
            return ",".join([f'{team.user.get_full_name().title()} ({team.user.username})' for team in teams])
        
        return None

class UserAdmin(UserAdmin):
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "phone", "college", "city", "course", "gender")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("username","first_name")
    ordering = ("username",)



admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.Configurations)
admin.site.register(models.EventCategory)
admin.site.register(models.SubEventsCategory)
admin.site.register(models.Events)
admin.site.register(models.TeamMembers)
admin.site.register(models.EventsRegistrations, EventsRegistrationsAdmin)
admin.site.register(models.WebsiteTeam)