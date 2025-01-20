from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import SourceChannel


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "registration/registration.html", {"form": form})


def source_channel_list(request):
    channels = SourceChannel.objects.filter(user=request.user)
    context = {"channels": channels}
    return render(request, "tracker/source_list.html", context)


def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        response = '<span class="text-danger">Username already exists</span>'
        return HttpResponse(response)
    else:
        response = '<span class="text-success">Username available</span>'
        return HttpResponse(response)


def check_email(request):
    email = request.POST.get("email")
    if get_user_model().objects.filter(email=email).exists():
        response = '<span class="text-danger">Email already exists</span>'
        return HttpResponse(response)
    else:
        response = '<span class="text-success">Email available</span>'
        return HttpResponse(response)
