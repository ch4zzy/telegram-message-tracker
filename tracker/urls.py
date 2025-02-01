from django.urls import path

from . import views

urlpatterns = [
    path("source/", views.source_list, name="source_list_partial"),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    # Edit
    path("create-source/", views.create_source, name="create_source"),
    path(
        "update-source-status/<int:pk>",
        views.update_source_status,
        name="update_source_status",
    ),
    path("update-source/<int:pk>", views.update_source, name="update_source"),
    path("delete-source/<int:pk>", views.delete_source, name="delete_source"),
    # Search
    path("search-source/", views.search_source, name="source_search"),
    # Statuses
    path(
        "source-validate/<int:pk>/",
        views.check_source_link,
        name="check_source_link",
    ),
    path(
        "check-task-status/<int:pk>/",
        views.check_task_status,
        name="check_task_status",
    ),
]

urlpatterns += htmx_patterns
