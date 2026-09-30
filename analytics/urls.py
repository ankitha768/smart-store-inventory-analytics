from django.urls import path
from .views import SummaryView
urlpatterns=[path("analytics/summary/",SummaryView.as_view())]
