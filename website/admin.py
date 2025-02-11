from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser, TeamMembers
from django.shortcuts import HttpResponse
import csv

from django.contrib import messages

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
    list_filter = ("is_staff", "is_active",)
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

    list_filter = ["parent_SubEventsCategory__parent_EventCategory","registration_open"]
    search_fields = ["title"]
    list_display = ["category", "title","is_team_event", "registration_amount","registration_open"]
    actions = ["close","open"]


    def category(self, queryset):
        return queryset.parent_SubEventsCategory.parent_EventCategory


    @admin.action(description="Close Registration")
    def close(self, request, queryset):
        queryset.update(registration_open = False)

    @admin.action(description="Open Registration")
    def open(self, request, queryset):
        queryset.update(registration_open = True)

class SoloEvRegAdming(admin.ModelAdmin):
    list_display = ["user", "event", "fee","payments_status", "date_time_registered"]
    search_fields = ["user__username", "event__title"]
    list_filter = ["event__parent_SubEventsCategory__parent_EventCategory", "event__parent_SubEventsCategory"]
    actions = ["exportSoloReg"]
    
    
    @admin.action(description="Export")
    def exportSoloReg(self, request, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="solo-registrations-data.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(["Category", "Event Name","Utkarsh ID", "Participant Name", "Phone","Gender","Email", "College name","City","Course"])
        temp = []
        for each in queryset:
            temp.append(
                [
                each.event.parent_SubEventsCategory.parent_EventCategory,
                each.event.title,
                each.user.username,
                each.user.first_name,
                each.user.phone,
                each.user.gender,
                each.user.email,
                each.user.college,
                each.user.city,
                each.user.course,

                ]
            )
        writer.writerows(temp)
        return response


class TeamEvRegAdming(admin.ModelAdmin):
    list_display = ["team_name", "teamleader","event", "team_members"]
    search_fields = ["teamleader__username","event__title"]
    list_filter = ["event__parent_SubEventsCategory__parent_EventCategory"]

    actions = ["export"]

    def team_members(self, object):
        t = TeamMembers.objects.filter(registration = object)
        return ", ".join([x.user.first_name for x in t]) 

    def export(self, request, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="tean-registrations-data.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(["Category", "Event Name","Team Name","Team Leader","Teammates", "Phone","Gender","Email", "College name"," City","Course"])
        temp = []

        for each in queryset:
            temp.append(
                [
                each.event.parent_SubEventsCategory.parent_EventCategory,
                each.event.title,
                each.team_name,
                f"{each.teamleader.first_name} ({each.teamleader.username})",
                self.team_members(each),
                each.teamleader.phone,
                each.teamleader.gender,
                each.teamleader.email,
                each.teamleader.college,
                each.teamleader.city,
                each.teamleader.course,

                ]
            )

        writer.writerows(
            temp
        )
        return response


class AccomodationAdmin(admin.ModelAdmin):
    list_display = ["user","user__gender","user__phone","user__college","fee","is_paid"]
    actions = ["export"]

    @admin.action(description="Export")
    def export(self, request, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="accomodation-data.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(["Utkarsh Id","Name", "Phone","Gender","Email", "College name"," City","Course"])
        temp = []

        for each in queryset:
            temp.append(
                [
                    each.user.username,
                    each.user.first_name,
                    each.user.phone,
                    each.user.gender,
                    each.user.email,
                    each.user.college,
                    each.user.city,
                    each.user.course,
                ]
            )

        writer.writerows(
            temp
        )
        return response



admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.Configurations)
admin.site.register(models.EventCategory, EventCategoryAdmin)
admin.site.register(models.SubEventsCategory)
admin.site.register(models.Events, EventsAdmin)
admin.site.register(models.TeamMembers)
admin.site.register(models.SoloEventRegistrations, SoloEvRegAdming)
admin.site.register(models.TeamEventRegistrations, TeamEvRegAdming)
admin.site.register(models.WebsiteTeam)
admin.site.register(models.AccomodationDetails, AccomodationAdmin)