from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from website.forms import RegisterForm
from website import models
from django.http import JsonResponse
from markdown import markdown
from django.conf import settings
from django.urls import reverse
import re
from django.core.mail import send_mail
from django.template.loader import render_to_string


class HomePageView(View):
    def get(self, request):
        event_category = models.EventCategory.objects.all()
        website_team = models.WebsiteTeam.objects.all()
        return render(request, "app/home.html", {"event_category": event_category, "website_team":website_team})






class EventsPageView(View):
    def get(self, request, eventname =None):

        filter = request.GET.get("filter")

        context = {
            "event_categories":models.EventCategory.objects.all()
        }

        if eventname:
            context["e"] = models.Events.objects.filter(parent_SubEventsCategory__parent_EventCategory__slug = eventname)
        
        else:
            if filter == "solo":
                context["e"]= models.Events.objects.filter(is_team_event = False)

            elif filter == "team":
                context["e"] =  models.Events.objects.filter(is_team_event = True)

            else: context["e"] = models.Events.objects.all()

        return render(request, "app/events.html", context=context)









class EventsDetailedPageView(View):
    def get(self, request, name):
        event = models.Events.objects.filter(slug = name)[0]

        context = {
             
            "title":  event.title,
            "details": event.details,
            "image":  event.image.url,
            "is_team_event": event.is_team_event,
            "team_size":  event.team_size,
            "registration_open":  event.registration_open,
            "registration_amount": event.registration_amount,
            "event_date": event.event_date,
            "venue": event.venu,
            "general_rules": markdown(event.parent_SubEventsCategory.parent_EventCategory.rules) if event.parent_SubEventsCategory.parent_EventCategory.rules else "No General Rules Available For This Category. ",
            "event_rules": markdown(event.description),
        }
        if event.image2 and event.image3 and event.image4:
            context["image2"] = event.image2.url,
            context["image3"] = event.image3.url,
            context["image4"] = event.image4.url,
        # check if enrolled
        if request.user.is_authenticated:
            if event.is_team_event:
                reg = models.TeamEventRegistrations.objects.filter(event = event, teamleader = request.user)
                # check is user is part of any team
                is_part_of_team = models.TeamMembers.objects.filter(user = request.user)
            else:
                reg = models.SoloEventRegistrations.objects.filter(user=request.user, event=event)

            if reg.exists():
                context["is_enrolled"] = reg[0].id
        
        return JsonResponse(data=context)







class EventRegSuccess(View):
    def get(self, request, registration_type, regid):
        context = {
            "type": registration_type
        }

        if registration_type == 'solo':
            context["registration"]  = get_object_or_404(models.SoloEventRegistrations, id=regid)
        else:
            r = get_object_or_404(models.TeamEventRegistrations, id = regid)
            context["registration"] = r
            context["team_members"] = models.TeamMembers.objects.filter(registration = r)

        return render(request, "app/reg_success.html", context=context)




class EventsEnrollPageView(View):
    def get(self, request, eventname):
        if not request.user.is_authenticated:
            url = reverse("loginpage")
            return redirect(f"{url}?next={request.path}")

        try:
            event = models.Events.objects.get(slug = eventname)
        except:
            return render(request, "app/eror.html")

        if event.is_team_event:
            return render(request, "app/enroll_team.html", {"event": event})
        
        else:
            reg = models.SoloEventRegistrations.objects.create(
                user = request.user,
                event = event,
                fee = event.registration_amount
            )
            reg.save()
            registration_type = "team" if event.is_team_event else "solo"
            url = reverse("eventspage")
            return redirect(f"{url}/enroll/{registration_type}/success/{reg.id}")


    def post(self, request, eventname):
        event = models.Events.objects.get(slug = eventname)
        
        teamlist = request.POST.get("teamlist").upper()
        teamname = request.POST.get("teamname")

        matches = re.findall(r'UK\d+', teamlist)
        
        if len(matches) > event.team_size or len(matches) == 0:
            er =  f"Team limit exceeds. Allowed team size: {event.team_size}" if len(matches) > event.team_size else "Invalid Utkarsh ID"
            return render(request, "app/enroll_team.html", {"event": event,"teamname":teamname, "teamlist":teamlist,"error":er})
        # validate each matches
        invalid_ids = []
        teammates = []
        for each in matches:
            v =  models.CustomUser.objects.filter(username =  each)
            if not v.exists():
                invalid_ids.append(each)
            else:
                teammates.append(v[0])

        if invalid_ids:
            err = "Invalid Utkarsh ID's : " + ",".join(invalid_ids)
            return render(request, "app/enroll_team.html", {"event": event, "teamname":teamname, "teamlist":teamlist,"error":err})
        else:
            reg = models.TeamEventRegistrations.objects.create(
                teamleader = request.user,
                event = event,
                team_name = teamname,
                fee = event.registration_amount
            )
            for i in teammates:
                models.TeamMembers.objects.create(
                    registration = reg,
                    user = i
                )
            registration_type = "team" if event.is_team_event else "solo"
            return redirect(f"{reverse("eventspage")}/enroll/{registration_type}/success/{reg.id}")



class LoginPageView(View):
    def get(self, request):
        return render(request, "app/Login.html")

    def post(self, request):
        ukid = request.POST.get("username").upper().strip()
        password = request.POST.get("password").strip()
        
        next_url = request.GET.get("next")

        user = authenticate(request, username=ukid, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url if next_url else "homepage")
        else:
            return render(request, "app/Login.html", {"error":"Invalid Utkarsh Id and/or password.", "ukid":ukid})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("homepage")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "app/register.html", {"register_form":register_form})
    
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()

            # send registeration mail
            context = {
                "name":user.first_name,
                "ukpass": register_form.cleaned_data["set_password"],
                "ukid": user.username
            }
            t =  render_to_string('components/mail.html', context=context)
            send_mail(
                subject="Subject: 🚀 Pre-Registration Confirmed for Utkarsh 2025!",
                message="Pre Registration Successfull!",
                recipient_list=[ user.email ],
                from_email= "website@bbd-utkarsh.org",
                html_message= t,
                fail_silently= True
            )
            login(request, user)
            return render(request, "app/register.html", {"register_form":register_form, "register_success": True,"utkarsh_id":user.username})
        else:
            return render(request, "app/register.html", {"register_form":register_form, "form_error":True})
        


class UnEnrollEvent(View):
    def get(self, request, eventname, regid):
        print(eventname, regid)
        ev = models.Events.objects.filter(slug = eventname)
        if ev.exists():
            if ev[0].is_team_event:
                reg = models.TeamEventRegistrations.objects.filter(teamleader=request.user, id = regid)
            else:
                reg = models.SoloEventRegistrations.objects.filter(user=request.user, id= regid)
            reg.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    


class UserProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:    
            return redirect(f"{reverse("loginpage")}?next={request.path}")
        
        context = {}
        payment = 0
        summary = {}
        p = ["sports","informal"]
        
        # check if enrolled into any events
        # checking for solo events
        solo_events = models.SoloEventRegistrations.objects.filter(user = request.user)
        if solo_events:
            context["solo_events"] = solo_events

            for i in solo_events:
                if i.event.parent_SubEventsCategory.parent_EventCategory.title.lower() in p:
                    summary[i.event.title] = i.event.registration_amount
                    payment += i.event.registration_amount

        # checck if team events
        team_events = models.TeamEventRegistrations.objects.filter(teamleader = request.user)
        if team_events.exists():
            # context["team_events"] = team_events

            # fetch team members details
            temp  = []
            for e in team_events:
                if e.event.parent_SubEventsCategory.parent_EventCategory.title.lower() in p:
                    summary[e.event.title] = e.event.registration_amount
                    payment += e.event.registration_amount
                
                temp.append(
                    [e, models.TeamMembers.objects.filter(registration = e)]
                )
            context["team_events"] = temp

        
        # check if members of any team events
        is_member = models.TeamMembers.objects.filter(user = request.user)
        if is_member.exists():
            context["is_member"] = is_member

        # generating payment summary
        
        accomodation = models.AccomodationDetails.objects.filter(user = request.user)
        if accomodation.exists():
            context["accomodation"] = True
            summary["Accomodation"] = accomodation[0].fee
            payment += accomodation[0].fee

        context["summary"] = summary
        context["total_amount"] = payment

        return render(request, "app/profile.html" , context=context)
    

class Accmodation(View):
    def post(self, request):
        acc = request.POST.get("accommodation").lower()

        if acc == "yes":
            models.AccomodationDetails.objects.create(
                user = request.user
            )
        elif acc == "no":
            models.AccomodationDetails.objects.filter(user = request.user).delete()
        
        return redirect("profilepage")