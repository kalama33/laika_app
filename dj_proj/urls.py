"""
URL configuration for dj_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

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
from django.urls import path, include
from accounts.views import landing_view
from django.conf import settings
from django.conf.urls.static import static
"""
1. `from django.contrib import admin`: This import allows you to include the Django admin site 
in your project.

2. `from django.urls import path, include`: This import is used to define URL patterns in Django and 
include other URL configurations.
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing_view'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),
    path('laika/',include('laika.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
path('admin/', admin.site.urls)`: This URL pattern maps the '/admin/' URL to the Django admin site. 
It allows you to access the admin interface and perform administrative tasks.

path('accounts/', include('allauth.urls')): This URL pattern maps the '/accounts/' URL to the allauth
library. It allows you to access the allauth library and perform authentication tasks.

path('accounts/', include('accounts.urls')): This URL pattern maps the '/accounts/' URL to the
`accounts` app. It allows you to access the `accounts` app and perform authentication tasks.

path('home/', include('home.urls')): This URL pattern maps the '/home/' URL to the `home` app.
It allows you to access the `home` app and perform authentication tasks.
"""
