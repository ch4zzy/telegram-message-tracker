from django.urls import path

from . import views

urlpatterns = [
    path("slist/", views.source_channel_list, name="source_channel_list"),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
]

urlpatterns += htmx_patterns
