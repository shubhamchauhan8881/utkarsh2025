from django.contrib import admin

# Register your models here.
from . import models
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser, TeamMembers

admin.site.site_title = "UTKARSH 2025"
admin.site.site_header = "UTKARSH Administration"
admin.site.index_title = "UTKARH 2025"


# class EventsRegistrationsAdmin(admin.ModelAdmin):
#     list_display = ["event", "leader", "team_members"]

#     def team_members(self, object):
#         teams = models.TeamMembers.objects.filter(event = object)
#         if teams:
#             return ",".join([f'{team.user.get_full_name().title()} ({team.user.username})' for team in teams])
        
#         return None

class UserAdmin(UserAdmin):
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        ("Login Details", {"fields": ("username", "password")}),
        ("Personal Details", {"fields": ("first_name","last_name", "email", "phone", "college", "city", "course", "gender")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "user_permissions")}),
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



class EventCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug":["title"]
    }



class EventsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug":["title"]
    }


class SoloEvRegAdming(admin.ModelAdmin):
    list_display = ["user", "event", "fee","payments_status", "date_time_registered"]
    search_fields = ["user__username"]
    list_filter = ["event__parent_SubEventsCategory__parent_EventCategory", "event__parent_SubEventsCategory"]

    


class TeamEvRegAdming(admin.ModelAdmin):
    list_display = ["team_name", "teamleader","event", "team_members"]
    search_fields = ["teamleader__username","event__title"]
    list_filter = ["event__parent_SubEventsCategory__parent_EventCategory"]
    
    

    def team_members(admin, object):
        t = TeamMembers.objects.filter(registration = object)
        return ",".join([x.user.username for x in t]) + f" ({str(len(t))} members)"



admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.Configurations)
admin.site.register(models.EventCategory, EventCategoryAdmin)
admin.site.register(models.SubEventsCategory)
admin.site.register(models.Events, EventsAdmin)
admin.site.register(models.TeamMembers)
admin.site.register(models.SoloEventRegistrations, SoloEvRegAdming)
admin.site.register(models.TeamEventRegistrations, TeamEvRegAdming)
admin.site.register(models.WebsiteTeam)
admin.site.register(models.AccomodationDetails)