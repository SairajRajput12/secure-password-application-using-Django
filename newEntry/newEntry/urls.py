from django.contrib import admin
from django.urls import path,include
# from newEntry.SecurePasswordApplication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SecurePasswordApplication.urls')),
]
