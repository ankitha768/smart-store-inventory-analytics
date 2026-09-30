from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns=[
path("admin/",admin.site.urls),
path("",TemplateView.as_view(template_name="dashboard.html"),name="dashboard"),
path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
path("api/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
path("api/",include("inventory.urls")),
path("api/",include("sales.urls")),
path("api/",include("analytics.urls")),
]