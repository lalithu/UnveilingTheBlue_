from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View

'''
class BlueView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'BluePages/index.html', context={
            }
        )
'''


def home(request):
    return render(request, 'BluePages/index.html', {})


def astronomy(request):
    return render(request, 'BluePages/astronomy.html', {})


def spaceExploration(request):
    return render(request, 'BluePages/spaceExploration.html', {})


def astrodev(request):
    return render(request, 'BluePages/astrodev.html', {})


def blog(request):
    return render(request, 'BluePages/blog.html', {})


def about(request):
    return render(request, 'BluePages/about.html', {})
