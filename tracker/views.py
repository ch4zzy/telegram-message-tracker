from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .forms import (
    CreateSourceChannelForm,
    CreateTargetChannelForm,
    SignUpForm,
    UpdatePostListForm,
    UpdateSourceDetailForm,
    UpdateSourceListForm,
    UpdateTargetListForm,
)
from .models import Post, SourceChannel, TargetChannel
from .tasks import post_message_task, validate_link_task


def paginate_queryset(queryset, request, page_size):
    """
    Paginate a queryset and return the page object

    Methods: GET
    Args:
        queryset: The queryset to paginate
        request: The request object
        page_size: The number of items per page
    Returns:
        page_obj: The paginated page object
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def login_view(request):
    """
    Handle user login

    Methods: GET, POST
    Args:
        request: The request object
    Returns:
        render: Render the login page with the authentication form
    """
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=user, password=password)
            if user:
                login(request, user)
                return redirect("source_list")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def signup(request):
    """
    Handle user registration

    Methods: GET, POST
    Args:
        request: The request object
    Returns:
        render: Render the registration page with the signup form
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


@require_GET
@login_required
def source_list(request):
    """
    Display a list of source channels

    Methods: GET
    Args:
        request: The request object
    Returns:
        render: Render the source list page with the paginated channels
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


@require_GET
@login_required
def source_list_component(request):
    """
    Display a partial list of source channels

    Methods: GET
    Args:
        request: The request object
    Returns:
        render: Render the partial source list component
    """
    channels = SourceChannel.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    page_obj = paginate_queryset(channels, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    return render(
        request, "tracker/partials/source_list_compound.html", context
    )

@require_GET
@login_required
def post_list_component(request, pk):
    """
    Display a partial list of posts from a source channel

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial post list component
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    posts = source.messages.all().order_by("-created_at")
    targets = source.target_channel.all()

    page_obj = paginate_queryset(posts, request, settings.PAGE_SIZE)
    context = {
        "page_obj": page_obj,
        "channel": source,
        "targets": targets,
        "posts_count": posts.count(),
        "pending_posts": posts.filter(status="pending").count(),
        "posted_posts": posts.filter(status="posted").count(),
    }
    return render(request, "tracker/partials/post_list_compound.html", context)


@require_GET
@login_required
def target_list(request):
    """
    Display a list of target channels

    Methods: GET
    Args:
        request: The request object
    Returns:
        render: Render the target list page with the paginated channels
    """
    channels = TargetChannel.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    page_obj = paginate_queryset(channels, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    if request.htmx:
        return render(request, "tracker/partials/target_list.html", context)
    else:
        return render(request, "tracker/target_page.html", context)


@require_GET
@login_required
def source_detail(request, pk):
    """
    Display details of a source channel

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the source detail page with the channel and posts
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    targets = source.target_channel.all()
    posts = source.messages.all().order_by("-created_at")
    page_obj = paginate_queryset(posts, request, settings.PAGE_SIZE)
    context = {
        "page_obj": page_obj,
        "channel": source,
        "targets": targets,
        "posts_count": posts.count(),
        "pending_posts": posts.filter(status="pending").count(),
        "posted_posts": posts.filter(status="posted").count(),
        "request": request,
    }
    if request.htmx:
        return render(request, "tracker/partials/post_list.html", context)
    else:
        return render(request, "tracker/source_detail.html", context)


def check_username(request):
    """
    Check if a username already exists

    Methods: POST
    Args:
        request: The request object
    Returns:
        HttpResponse: A response indicating whether the username is available
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

    Methods: POST
    Args:
        request: The request object
    Returns:
        HttpResponse: A response indicating whether the email is available
    """
    email = request.POST.get("email")
    exists = get_user_model().objects.filter(email=email).exists()
    response = (
        '<span class="text-danger">Email already exists</span>'
        if exists
        else '<span class="text-success">Email available</span>'
    )
    return HttpResponse(response)


@require_POST
@login_required
def update_source_status(request, pk):
    """
    Update the active status of a source channel

    Methods: POST
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial source element with the updated status
    """
    if request.method == "POST":
        source = get_object_or_404(SourceChannel, pk=pk)
        source.active_following = not source.active_following
        source.save()
        return render(
            request,
            "tracker/partials/source_active_following.html",
            {"channel": source},
        )


@require_POST
@login_required
def update_target_status(request, pk):
    """
    Update the auto post status of a target channel

    Methods: POST
    Args:
        request: The request object
        pk: The primary key of the target channel
    Returns:
        render: Render the partial target element with the updated status
    """
    if request.method == "POST":
        target = get_object_or_404(TargetChannel, pk=pk)
        target.auto_post = not target.auto_post
        target.save()
        return render(
            request,
            "tracker/partials/target_auto_post.html",
            {"channel": target},
        )

@login_required
def delete_source(request, pk):
    """
    Delete a source channel

    Methods: DELETE
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        HttpResponse: A response indicating the deletion was successful
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    source.delete()
    return HttpResponse("<div></div>")


@login_required
def delete_target(request, pk):
    """
    Delete a target channel

    Methods: DELETE
    Args:
        request: The request object
        pk: The primary key of the target channel
    Returns:
        HttpResponse: A response indicating the deletion was successful
    """
    target = get_object_or_404(TargetChannel, pk=pk)
    target.delete()
    return HttpResponse("<div></div>")


@login_required
def create_source(request):
    """
    Create a new source channel

    Methods: GET, POST
    Args:
        request: The request object
    Returns:
        render: Render the source modal form or the source list with the new channel
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


@login_required
def create_target(request):
    """
    Create a new target channel

    Methods: GET, POST
    Args:
        request: The request object
    Returns:
        render: Render the target modal form or the target list with the new channel
    """
    if request.method == "POST":
        form = CreateTargetChannelForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.user = request.user
            target.save()
            channels = TargetChannel.objects.filter(
                user=request.user
            ).order_by("-created_at")
            page_obj = paginate_queryset(channels, request, settings.PAGE_SIZE)
            context = {
                "page_obj": page_obj,
                "request": request,
                "target_pk": target.pk,
            }
            return render(
                request,
                "tracker/partials/target_list.html",
                context,
                status=201,
            )
        return render(
            request,
            "tracker/partials/target_modal_form.html",
            {"form": form},
            status=400,
        )
    form = CreateTargetChannelForm()
    return render(
        request, "tracker/partials/target_modal_form.html", {"form": form}
    )

@login_required
def update_source(request, pk):
    """
    Update a source channel

    Methods: GET, POST
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the source modal form or the source list with the updated channel
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

@login_required
def update_target(request, pk):
    """
    Update a target channel

    Methods: GET, POST
    Args:
        request: The request object
        pk: The primary key of the target channel
    Returns:
        render: Render the target modal form or the target list with the updated channel
    """
    target = get_object_or_404(TargetChannel, pk=pk)
    if request.method == "POST":
        form = UpdateTargetListForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return render(
                request,
                "tracker/partials/target_element.html",
                {"channel": target},
            )
    else:
        form = UpdateTargetListForm(instance=target)
        return render(
            request,
            "tracker/partials/target_form.html",
            {"channel": target, "form": form},
        )

@login_required
def update_post_list(request, pk):
    """
    Update post from list of posts for specific source

    Methods: GET, POST
    Args:
        request: The request object
        pk: The primary key of the post
    Returns:
        render: Render the post modal form or the post list with the updated post
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = UpdatePostListForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return render(
                request,
                "tracker/partials/post_element.html",
                {"post": post},
            )
    else:
        form = UpdatePostListForm(instance=post)
        return render(
            request,
            "tracker/partials/post_form.html",
            {"post": post, "form": form},
        )


@login_required
def search_source(request):
    """
    Search for a source channel by name

    Methods: GET
    Args:
        request: The request object
    Returns:
        render: Render the partial source list with the search results
    """
    query = request.GET.get("query")
    result = SourceChannel.objects.filter(
        user=request.user, name__icontains=query
    ).order_by("-created_at")
    page_obj = paginate_queryset(result, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    return render(request, "tracker/partials/source_list.html", context)


@login_required
def search_target(request):
    """
    Search for a target channel by name

    Methods: GET
    Args:
        request: The request object
    Returns:
        render: Render the partial target list with the search results
    """
    query = request.GET.get("query")
    result = TargetChannel.objects.filter(
        user=request.user, name__icontains=query
    ).order_by("-created_at")
    page_obj = paginate_queryset(result, request, settings.PAGE_SIZE)
    context = {"page_obj": page_obj, "request": request}
    return render(request, "tracker/partials/target_list.html", context)


@login_required
def check_source_link(request, pk):
    """
    Check the status of a source channel link

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial source element with the link status
    """
    from .tasks import validate_link_task

    task = validate_link_task.delay(pk, "SourceChannel")
    source = get_object_or_404(SourceChannel, pk=pk)
    return render(
        request,
        "tracker/partials/source_element.html",
        {"channel": source, "task_id": task.id},
    )

@login_required
def check_target_link(request, pk):
    """
    Check the status of a target channel link

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the target channel
    Returns:
        render: Render the partial target element with the link status
    """
    from .tasks import validate_link_task

    task = validate_link_task.delay(pk, "TargetChannel")
    target = get_object_or_404(TargetChannel, pk=pk)
    return render(
        request,
        "tracker/partials/target_element.html",
        {"channel": target, "task_id": task.id},
    )

@login_required
def check_target_bot(request, pk):
    """
    Check the status of a target channel bot

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the target channel
    Returns:
        render: Render the partial target element with the bot status
    """
    from .tasks import validate_admin_bot_task

    task = validate_admin_bot_task.delay(pk)
    target = get_object_or_404(TargetChannel, pk=pk)
    return render(
        request,
        "tracker/partials/target_element.html",
        {"channel": target, "task_id": task.id},
    )


@login_required
def get_source(request, pk):
    """
    Check the status of a SourceChannel link

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial source element with the link status
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    return render(
        request,
        "tracker/partials/source_element.html",
        {"channel": source},
    )


@login_required
def get_target(request, pk):
    """
    Check the status of a TargetChannel link

    Methods: GET
    """
    target = get_object_or_404(TargetChannel, pk=pk)
    return render(
        request,
        "tracker/partials/target_element.html",
        {"channel": target},
    )


@login_required
def unlink_target(request, source_id, target_id):
    """
    Unlink a target channel from a source channel

    Methods: DELETE
    Args:
        request: The request object
        source_id: The primary key of the source channel
        target_id: The primary key of the target channel
    Returns:
        HttpResponse: A response indicating the unlinking was successful
    """
    if request.method == "DELETE":
        source = get_object_or_404(SourceChannel, id=source_id)
        target = get_object_or_404(TargetChannel, id=target_id)
        source.target_channel.remove(target)
        return HttpResponse("<div></div>")
    return HttpResponse(status=405)


@login_required
def get_target_modal(request, source_id):
    """
    Display a modal form to link a target channel to a source channel

    Methods: GET
    Args:
        request: The request object
        source_id: The primary key of the source channel
    Returns:
        render: Render the target link modal form with available targets
    """
    source = get_object_or_404(SourceChannel, id=source_id)
    available_targets = TargetChannel.objects.filter(
        user=request.user
    ).exclude(id__in=source.target_channel.values_list("id", flat=True))
    context = {"targets": available_targets, "source": source}
    return render(
        request, "tracker/partials/source_link_modal_form.html", context
    )


@login_required
def link_target(request, source_id, target_id):
    """
    Link a target channel to a source channel
    
    Methods: POST
    Args:
        request: The request object
        source_id: The primary key of the source channel
        target_id: The primary key of the target channel
    Returns:
        render: Render the partial source element with the link status
    """
    if request.method == "POST":
        source = get_object_or_404(SourceChannel, id=source_id)
        target = get_object_or_404(TargetChannel, id=target_id)
        source.target_channel.add(target)
        context = {"linked_success": True, "source": source}
        return render(
            request, "tracker/partials/source_linked_success.html", context
        )
    return HttpResponse(status=405)


@login_required
def get_linked_targets(request, source_id):
    """
    Get a list of linked target channels for a source channel

    Methods: GET
    Args:
        request: The request object
        source_id: The primary key of the source channel
    Returns:
        render: Render the partial linked target list with the targets
    """
    source = get_object_or_404(SourceChannel, id=source_id)
    targets = source.target_channel.all()
    context = {"targets": targets, "channel": source}
    return render(request, "tracker/partials/linked_target_list.html", context)


@login_required
@require_POST
def post_message(request, post_id):
    """
    Post a message to a target channel using a delayed task

    Methods: POST
    Args:
        request: The request object
        post_id: The primary key of the post
    Returns:
        render: Render the partial post element with the task ID
    """
    post = get_object_or_404(Post, id=post_id)
    task_id = post_message_task.delay(post_id)
    context = {"post": post, "task_id": task_id}
    return render(request, "tracker/partials/post_element.html", context)


@login_required
@require_POST
def post_reject(request, post_id):
    """
    Reject a post by ID

    Methods: POST
    Args:
        request: The request object
        post_id: The primary key of the post
    Returns:
        render: Render the partial post element with the rejected post details
    """
    post = get_object_or_404(Post, id=post_id)
    post.status = "rejected"
    post.save()
    context = {"post": post}
    return render(request, "tracker/partials/post_element.html", context)


@login_required
@require_GET
def get_post(request, post_id):
    """
    Get a post by ID

    Methods: GET
    Args:
        request: The request object
        post_id: The primary key of the post
    Returns:
        render: Render the partial post element with the post details
    """
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post}
    return render(request, "tracker/partials/post_element.html", context)


@login_required
def filter_posts(request, pk):
    """
    Filter posts by status and query

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial post list with the filtered posts
    """
    status = request.GET.get("status", "all")
    query = request.GET.get("query", "")
    posts = Post.objects.filter(channel_id=pk)
    if status != "all":
        posts = paginate_queryset(
            posts.filter(status=status), request, settings.PAGE_SIZE
        )
    if query:
        posts = paginate_queryset(
            posts.filter(content__icontains=query), request, settings.PAGE_SIZE
        )
    return render(
        request, "tracker/partials/post_list.html", {"page_obj": posts}
    )


@login_required
def update_detail_source(request, pk):
    """
    Update the details of a source channel

    Methods: GET, POST
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the source detail form or the partial source detail element with the updated channel
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    available_targets = TargetChannel.objects.filter(
        user=request.user
    ).exclude(id__in=source.target_channel.values_list("id", flat=True))
    posts = source.messages.all().order_by("-created_at")
    if request.method == "POST":
        form = UpdateSourceDetailForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            source.verified_status = False
            source.save()
            return render(
                request,
                "tracker/partials/source_detail_element.html",
                {
                    "channel": source,
                    "targets": available_targets,
                    "posts_count": posts.count(),
                    "pending_posts": posts.filter(status="pending").count(),
                    "posted_posts": posts.filter(status="posted").count(),
                },
            )
    form = UpdateSourceListForm(instance=source)
    return render(
        request,
        "tracker/partials/source_detail_form.html",
        {"channel": source, "form": form},
    )


@login_required
def update_detail_active_following(request, pk):
    """
    Update the active status of a source channel

    Methods: POST
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial source detail element with the updated status
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    source.active_following = not source.active_following
    source.save()
    return render(
        request,
        "tracker/partials/source_detail_active_following.html",
        {"channel": source},
    )


@login_required
def verify_detail_source(request, pk):
    """
    Verify the source channel using a delayed task

    Methods: GET
    Args:
        request: The request object
        pk: The primary key of the source channel
    Returns:
        render: Render the partial source detail element with the task ID
    """
    source = get_object_or_404(SourceChannel, pk=pk)
    task_id = validate_link_task.delay(pk, "SourceChannel")
    return render(
        request,
        "tracker/partials/source_detail_element.html",
        {"channel": source, "task_id": task_id},
    )
