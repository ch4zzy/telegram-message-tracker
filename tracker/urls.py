from django.urls import path

from . import views

urlpatterns = [
    path("source/", views.source_list, name="source_list"),
    path("source/<int:pk>/", views.source_detail, name="source_detail"),
    path("target/", views.target_list, name="target_list"),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    # List partial
    path(
        "source-list/",
        views.source_list_component,
        name="source_list_component",
    ),
    path(
        "post-list/source/<int:pk>",
        views.post_list_component,
        name="source_post_list_component",
    ),
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
    path("update-post/<int:pk>", views.update_post_list, name="update_post"),
    path("delete-source/<int:pk>", views.delete_source, name="delete_source"),
    path("delete-target/<int:pk>", views.delete_target, name="delete_target"),
    path(
        "update-detail-source/<int:pk>",
        views.update_detail_source,
        name="update_detail_source",
    ),
    path(
        "update-detail-active-following/<int:pk>",
        views.update_detail_active_following,
        name="update_detail_active_following",
    ),
    path(
        "verify-detail-source/<int:pk>",
        views.verify_detail_source,
        name="verify_detail_source",
    ),
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
    path("get-source/<int:pk>/", views.get_source, name="get_source"),
    path("get-target/<int:pk>/", views.get_target, name="get_target"),
    path(
        "unlink-target/<int:source_id>/<int:target_id>/",
        views.unlink_target,
        name="unlink_target",
    ),
    path(
        "source/<int:source_id>/get-targets/",
        views.get_target_modal,
        name="get_target_modal",
    ),
    path(
        "source/<int:source_id>/link-target/<int:target_id>/",
        views.link_target,
        name="link_target",
    ),
    path(
        "source/<int:source_id>/linked-targets/",
        views.get_linked_targets,
        name="get_linked_targets",
    ),
    # Post
    path(
        "post/<int:post_id>/approve/", views.post_message, name="post_message"
    ),
    path("post/<int:post_id>/reject/", views.post_reject, name="post_reject"),
    path("post/<int:post_id>/", views.get_post, name="get_post"),
    path("post/<int:pk>/filter/", views.filter_posts, name="filter_posts"),
]


urlpatterns += htmx_patterns
