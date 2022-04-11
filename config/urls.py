from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('src.oauth.urls')),
    path('api/v1/', include('src.routes')),
]
