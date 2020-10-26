from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View

movies = [
    {
        'title': 'Catchfire',
        'year': 1990,
    },
    {
        'title': 'Mighty Ducks the Movie: The First Face-Off',
        'year': 1997,
    },
    {
        'title': 'Le Zombi de Cap-Rouge',
        'year': 1997,
    },
]


class MovieView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'BluePages/index.html', context={
                'director': settings.DIRECTOR,
                'movies': movies,
            }
        )
