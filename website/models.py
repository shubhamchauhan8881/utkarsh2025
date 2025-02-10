from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class Configurations(models.Model):
    taking_registration = models.BooleanField(default=True)
    pre_registration_phase = models.BooleanField(default=False)

    def __str__(self):
        return "Core Configurations"


# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10)
    college = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, default="NA")


class EventCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    # stored in markdown format
    rules = models.TextField(blank=True, null=True, max_length=8000)
    image =  models.ImageField(upload_to = 'media/EventCategory/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title


class SubEventsCategory(models.Model):
    parent_EventCategory = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.parent_EventCategory.title + ' - ' + self.title


class AccomodationDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fee = models.IntegerField(default=1000)
    is_paid = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)


class Gallery(models.Model):
    title = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(upload_to="media/gallery/")



class Events(models.Model):
    parent_SubEventsCategory = models.ForeignKey(SubEventsCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    description = models.TextField(max_length=10000)
    image =  models.ImageField(upload_to = 'media/Events/', null=True, blank=True)
    image2 =  models.ImageField(upload_to = 'media/Events/', null=True, blank=True)
    image3 =  models.ImageField(upload_to = 'media/Events/', null=True, blank=True)
    image4 =  models.ImageField(upload_to = 'media/Events/', null=True, blank=True)

    is_team_event = models.BooleanField(default=False)
    team_size = models.IntegerField(default=5)  #if it is a team event
    registration_open = models.BooleanField(default=True)

    registration_amount = models.IntegerField(default=0)

    event_date = models.DateField(null=True, blank=True)
    venu = models.CharField(null=True, blank=True, max_length=300)

    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title



class SoloEventRegistrations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    fee = models.IntegerField(default=0)
    extra_charges = models.IntegerField(default=0)
    payments_status =  models.BooleanField(default=False)

    date_time_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title + ' registered by ' + self.user.get_full_name()



#this is for team event 
class TeamEventRegistrations(models.Model):
    #it will be the leader if any group registration...
    teamleader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="team_leader")
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="event_name")

    team_name = models.CharField(max_length=50)

    fee = models.IntegerField(default=0)
    extra_charges = models.IntegerField(default=0)
    payments_status =  models.BooleanField(default=False)
    date_time_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name 
   

class TeamMembers(models.Model):
    registration = models.ForeignKey(TeamEventRegistrations, on_delete=models.CASCADE, related_name="event_leader_registered", null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="member_details", null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()



class WebsiteTeam(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'media/team/')
    about = models.CharField(max_length=50, blank=True)

    #links--------------------------------
    linkedin = models.URLField(blank=True, null=True)
