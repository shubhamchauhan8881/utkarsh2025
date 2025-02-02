from django.shortcuts import render
from . import forms
from django.views import View
# Create your views here.
class homeView(View):
    def get(self, request):
        register_form = forms.RegisterForm()
        return render(request, "pre/index.html", {"register_form":register_form})

    def post(self, request):
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            ukid = register_form.save()
            return render(request, "pre/index.html", {"register_form":register_form, "register_success": True,"utkarsh_id":ukid})
        else:
            return render(request, "pre/index.html", {"register_form":register_form, "form_error":True})