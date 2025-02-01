from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateSourceChannelForm, SignUpForm, UpdateSourceListForm
from .models import SourceChannel


def paginate_queryset(queryset, request, page_size):
    """
    Paginate a queryset and return the page object
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def signup(request):
    """
    Handle user registration
    """
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


def source_list(request):
    """
    Display a list of source channels
    """
    channels = SourceChannel.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    page_obj = paginate_queryset(channels, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    if request.htmx:
        return render(request, "tracker/partials/source_list.html", context)
    else:
        return render(request, "tracker/source_page.html", context)


def check_username(request):
    """
    Check if a username already exists
    """
    username = request.POST.get("username")
    exists = get_user_model().objects.filter(username=username).exists()
    response = (
        '<span class="text-danger">Username already exists</span>'
        if exists
        else '<span class="text-success">Username available</span>'
    )
    return HttpResponse(response)


def check_email(request):
    """
    Check if an email already exists
    """
    email = request.POST.get("email")
    exists = get_user_model().objects.filter(email=email).exists()
    response = (
        '<span class="text-danger">Email already exists</span>'
        if exists
        else '<span class="text-success">Email available</span>'
    )
    return HttpResponse(response)


def update_source_status(request, pk):
    """
    Update the active status of a source channel
    """
    if request.method == "POST":
        source = get_object_or_404(SourceChannel, pk=pk)
        source.active_following = not source.active_following
        source.save()
        return render(
            request,
            "tracker/partials/active_following_element.html",
            {"channel": source},
        )


def delete_source(request, pk):
    """
    Delete a source channel
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    source.delete()
    return HttpResponse("<div></div>")


def create_source(request):
    """
    Create a new source channel
    """
    if request.method == "POST":
        form = CreateSourceChannelForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.user = request.user
            source.save()

            channels = SourceChannel.objects.filter(
                user=request.user
            ).order_by("-created_at")
            page_obj = paginate_queryset(channels, request, settings.PAGE_SIZE)
            context = {
                "page_obj": page_obj,
                "request": request,
                "source_pk": source.pk,
            }
            return render(
                request,
                "tracker/partials/source_list.html",
                context,
                status=201,
            )
        return render(
            request,
            "tracker/partials/source_modal_form.html",
            {"form": form},
            status=400,
        )
    form = CreateSourceChannelForm()
    return render(
        request, "tracker/partials/source_modal_form.html", {"form": form}
    )


def update_source(request, pk):
    """
    Update a source channel
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    if request.method == "POST":
        form = UpdateSourceListForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return render(
                request,
                "tracker/partials/source_element.html",
                {"channel": source},
            )
    else:
        form = UpdateSourceListForm(instance=source)
        return render(
            request,
            "tracker/partials/source_form.html",
            {"channel": source, "form": form},
        )


def search_source(request):
    """
    Search for a source channel by name
    """
    query = request.GET.get("query")
    result = SourceChannel.objects.filter(
        user=request.user, name__icontains=query
    ).order_by("-created_at")
    page_obj = paginate_queryset(result, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    return render(request, "tracker/partials/source_list.html", context)


def check_source_link(request, pk):
    """
    Check the status of a source channel link
    """
    from .tasks import validate_link_task

    task = validate_link_task.delay(pk, "SourceChannel")
    source = get_object_or_404(SourceChannel, pk=pk)
    return render(
        request,
        "tracker/partials/source_element.html",
        {"channel": source, "task_id": task.id},
    )


def check_task_status(request, pk):
    """
    Check the status of a SourceChannel link
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    return render(
        request,
        "tracker/partials/source_element.html",
        {"channel": source},
    )
