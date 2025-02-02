from django.shortcuts import render
from . import forms
from django.views import View
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from threading import Thread
# Create your views here.
class homeView(View):
    def get(self, request):
        register_form = forms.RegisterForm()
        return render(request, "pre/index.html", {"register_form":register_form})

    def post(self, request):
        register_form = forms.RegisterForm(request.POST)
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

            return render(request, "pre/index.html", {"register_form":register_form, "register_success": True,"utkarsh_id":user.username})
        else:
            return render(request, "pre/index.html", {"register_form":register_form, "form_error":True})
        


class MailView(View):
    def get(self, request):
        context = {
            "name":"",
            "ukpass": "",
            "ukid":""
        }
        t =  render_to_string('components/mail.html', context=context)

        send_mail(
            subject="Subject: 🚀 Pre-Registration Confirmed for Utkarsh 2025!",
            message="Pre Registration Successfull!",
            recipient_list=["shubhamchauhan9452@gmail.com", "shubhamsinghania0508@gmail.com"],
            from_email= "website@bbd-utkarsh.org",
            html_message= t,
        )
        return HttpResponse(t)