from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import SourceChannel


def signup(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data, form.errors)
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
