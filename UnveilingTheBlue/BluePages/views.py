from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View


class BlueView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'BluePages/index.html', context={
            }
        )
