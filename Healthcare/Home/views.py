from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from jsonview.decorators import json_view
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from Home.forms import BecomeMemberForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Home.models import Become_member

def homeview(request):
    return render(request, 'HomePageFinal.html')

def member(request):
    context = {}
    if request.method == 'POST':
        form = BecomeMemberForm(request.POST)
        if form.is_valid():
		    #form.save()
            Institution_Name = form.cleaned_data.get('Institution_name')
            Institution_Email_ID = form.cleaned_data.get('Email_ID')
            Institution_Phone_Number = form.cleaned_data.get('Phone_Number')
            Institution_Source_of_Info = form.cleaned_data.get('Source_of_Info')
            form.save()
            return redirect('/Home/member/success')

        else:
            context['form'] = form
            print(form.errors)
    else:
        form = BecomeMemberForm()
        context['form'] = form
    return render(request, 'Become_a_Member.html', context)

def success(request):
    return render(request, 'MemberSuccess.html')