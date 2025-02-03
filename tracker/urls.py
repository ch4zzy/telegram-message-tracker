from django.urls import path

from . import views

urlpatterns = [
    path("source/", views.source_list, name="source_list_partial"),
    path("target/", views.target_list, name="target_list_partial"),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    # Edit
    path("create-source/", views.create_source, name="create_source"),
    path("create-target/", views.create_target, name="create_target"),
    path(
        "update-source-status/<int:pk>",
        views.update_source_status,
        name="update_source_status",
    ),
    path(
        "update-target-status/<int:pk>",
        views.update_target_status,
        name="update_target_status",
    ),
    path("update-source/<int:pk>", views.update_source, name="update_source"),
    path("update-target/<int:pk>", views.update_target, name="update_target"),
    path("delete-source/<int:pk>", views.delete_source, name="delete_source"),
    path("delete-target/<int:pk>", views.delete_target, name="delete_target"),
    # Search
    path("search-source/", views.search_source, name="source_search"),
    path("search-target/", views.search_target, name="target_search"),
    # Statuses
    path(
        "source-validate/<int:pk>/",
        views.check_source_link,
        name="check_source_link",
    ),
    path(
        "target-validate/<int:pk>/",
        views.check_target_link,
        name="check_target_link",
    ),
    path(
        "target-bot-validate/<int:pk>/",
        views.check_target_bot,
        name="check_target_bot",
    ),
    path("source/<int:pk>/", views.get_source, name="get_source"),
    path("target/<int:pk>/", views.get_target, name="get_target"),
]

urlpatterns += htmx_patterns
