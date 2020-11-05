"""UnveilingTheBlue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from BluePages import views
from django.urls import path
'''from BluePages.views import BlueView'''

'''
urlpatterns = [
    path('', BlueView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
'''

urlpatterns = [
    path('', views.home, name="index"),
    path('simulator.html', views.simulator, name="simulator"),
    path('spaceExploration.html', views.spaceExploration, name="spaceExploration"),
    path('astrodev.html', views.astrodev, name="astrodev"),
    path('realtime.html', views.realtime, name="realtime"),
    path('about.html', views.about, name="about"),
]
