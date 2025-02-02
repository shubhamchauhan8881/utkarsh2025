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
    description = models.CharField(max_length=500)
    image =  models.ImageField(upload_to = 'media/EventCategory/')

    def __str__(self):
        return self.title

class SubEventsCategory(models.Model):
    parent_EventCategory = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.parent_EventCategory.title + ' - ' + self.title


class AccomodationDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fee = models.IntegerField(default=0)
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
    image =  models.ImageField(upload_to = 'media/Events/')

    is_team_event = models.BooleanField(default=False)
    team_size = models.IntegerField(default=5)  #if it is a team event
    registration_open = models.BooleanField(default=True)

    registration_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class EventsRegistrations(models.Model):
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    # if team event
    fee = models.IntegerField(default=0)
    extra_charges = models.IntegerField(default=0)
    payments_status =  models.BooleanField(default=False)

    date_time_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title + ' registered by ' + self.leader.get_full_name()

class TeamMembers(models.Model):
    event = models.ForeignKey(EventsRegistrations, on_delete=models.CASCADE, related_name="event_leader_registered")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="member_details")

    def __str__(self):
        return self.user.get_full_name()


class Accomodation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField(default=500)
    days_count = models.IntegerField(default=3)
    paid = models.BooleanField(default=False)




class WebsiteTeam(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'media/team/')
    about = models.CharField(max_length=50, blank=True)

    #links--------------------------------
    insta = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
