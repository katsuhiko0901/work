from django.contrib import admin
from django.urls import path , include
from django.views.generic import RedirectView

urlpatterns = [
    path('ai_analysis/', include('ai_analysis.urls')),
    path('api_mock/', include('api_mock.urls')),
    path('admin/', admin.site.urls),
    path('',RedirectView.as_view(url='/ai_analysis/')),
]
