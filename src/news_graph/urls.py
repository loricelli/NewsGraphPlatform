"""news_graph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from pages.views import home_view,signup,signin,signout
from node.views import tail_news,head_news
from confirmation.views import create_confirmation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view,name='home'),
    path('signup/', signup,name='signup'),
    path('signin/', signin,name='signin'),
    path('signout/', signout,name='signout'),
    path('read_news/',tail_news,name='read'),
    path('compare_news/<int:edge_id>', head_news, name="compare"),
    path('confirm/<int:edge_id>-<int:vote>', create_confirmation, name="confirm"),

]
