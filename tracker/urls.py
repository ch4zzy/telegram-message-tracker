from django.urls import path
from . import views
urlpatterns = [
    path("slist/", views.source_channel_list, name="source_channel_list"),
]

htmx_patterns = [
    path("check-username/", views.check_username, name="check_username"),
]

urlpatterns += htmx_patterns