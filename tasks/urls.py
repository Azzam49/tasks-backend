"""tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from django.views.generic import TemplateView
from django.shortcuts import redirect

from django.conf.urls.static import static
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
        })

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),

    # Token api using 'POST' request
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]


def redirect_to_ui(request):
    return redirect('/ui/dashboard')

# only for production or testing serving react from within django from local
urlpatterns += [
    # Serve React app
    re_path('ui\/.*',TemplateView.as_view(template_name='index.html')),
    # Redirect to React app
    path('', redirect_to_ui),
    path('/', redirect_to_ui),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)