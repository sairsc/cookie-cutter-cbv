from django.urls import path

from . import views

urlpatterns = [
    path("feedback/list/", views.FeedbackListView.as_view(), name="feedback_list"),
    path("feedback/new/", views.FeedbackCreateView.as_view(), name="feedback_new"),
]
