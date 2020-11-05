from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail

from plotly.offline import plot
from plotly.graph_objs import Scatter

from astropy.time import Time
from astropy import units as u

from poliastro.bodies import Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Sun
from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.plotting import OrbitPlotter3D
from poliastro.util import time_range

import plotly.io as pio

from poliastro.plotting.misc import plot_solar_system

import datetime


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


def simulator(request):
    return render(request, 'BluePages/simulator.html', {})


def spaceExploration(request):
    return render(request, 'BluePages/spaceExploration.html', {})


def astrodev(request):
    return render(request, 'BluePages/astrodev.html', {})


def realtime(request):

    # SolarSys Code
    current_time = datetime.datetime.now()
    print(current_time)

    EPOCH1 = Time(str(current_time), scale="tdb")
    solarsys = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

    solarsys.plot_body_orbit(Mercury, EPOCH1)
    solarsys.plot_body_orbit(Venus, EPOCH1)
    solarsys.plot_body_orbit(Earth, EPOCH1)
    solarsys.plot_body_orbit(Mars, EPOCH1)
    '''solarsys.plot_body_orbit(Jupiter, EPOCH1)
    solarsys.plot_body_orbit(Saturn, EPOCH1)
    solarsys.plot_body_orbit(Uranus, EPOCH1)
    solarsys.plot_body_orbit(Neptune, EPOCH1)'''

    solarsys_div = plot(solarsys.set_view(45 * u.deg, -120 *
                                          u.deg, 4 * u.km), output_type='div')
    # SolarSys Code

    # Roadster Code
    EPOCH = Time("2018-02-18 12:00:00", scale="tdb")

    roadster = Ephem.from_horizons(
        "SpaceX Roadster",
        epochs=time_range(EPOCH, end=EPOCH + 360 * u.day),
        attractor=Sun,
        plane=Planes.EARTH_ECLIPTIC,
        id_type="majorbody",
    )

    frame = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

    frame.plot_body_orbit(Earth, EPOCH)
    frame.plot_body_orbit(Mars, EPOCH)

    frame.plot_ephem(
        roadster, EPOCH, label="SpaceX Roadster", color="black")

    frame_div = plot(frame.set_view(45 * u.deg, -120 *
                                    u.deg, 4 * u.km), output_type='div')
    # Roadster Code
    return render(request, 'BluePages/realtime.html',  context={'frame_div': frame_div, 'solarsys_div': solarsys_div})


def about(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # Sending an Email
        send_mail(
            "Unveiling The Blue - Message from: " + message_name,  # Subject
            message,  # Message
            message_email,  # From Email
            ['lalithuriti@gmail.com'],  # To Email
        )

        return render(request, 'BluePages/about.html', {'message_name': message_name})

    else:
        return render(request, 'BluePages/about.html', {})
