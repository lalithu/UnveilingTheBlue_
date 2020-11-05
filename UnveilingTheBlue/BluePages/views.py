from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail

# Mission Control Dependencies
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

import numpy as np

import astropy.units as u
from astropy import time

from poliastro import iod
from poliastro.bodies import Earth, Mars, Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
from poliastro.util import time_range

from poliastro.plotting.misc import plot_solar_system
from poliastro.frames import Planes

from astropy.coordinates import solar_system_ephemeris
from poliastro.plotting import OrbitPlotter2D


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
    if request.method == "POST":
        launch_date = request.POST['launch_date']
        arrival_date = request.POST['arrival_date']

        # Set Date and Time
        datetime_launch = launch_date
        # print(datetime_launch)
        datetime_arrival = arrival_date
        # print(datetime_arrival)

        # Curiosity: 2011-11-26 15:02, Perserverance: 2020-6-30 11:50
        date_launch = time.Time(datetime_launch, scale="utc").tdb
        # Curiosity: 2012-08-06 05:17 Perserverance: 2021-2-18 12:30
        date_arrival = time.Time(datetime_arrival, scale="utc").tdb

        # Earth Launch
        Earth2dL = OrbitPlotter2D()

        Earth2dL_div = plot(Earth2dL.plot_body_orbit(
            Earth, date_launch), output_type='div')

        # Mars Launch
        Mars2dL = OrbitPlotter2D()

        Mars2dL_div = plot(Mars2dL.plot_body_orbit(
            Mars, date_launch), output_type='div')

        # Frame Launch
        Frame2dL = OrbitPlotter2D()

        Frame2dL.plot_body_orbit(Mars, date_launch)

        Frame2dL_div = plot(Frame2dL.plot_body_orbit(
            Earth, date_launch), output_type='div')

        # Earth Arrival
        Earth2dA = OrbitPlotter2D()

        Earth2dA_div = plot(Earth2dA.plot_body_orbit(
            Earth, date_arrival), output_type='div')

        # Mars Arrival
        Mars2dA = OrbitPlotter2D()

        Mars2dA_div = plot(Mars2dA.plot_body_orbit(
            Mars, date_launch), output_type='div')

        # Frame Arrival
        Frame2dA = OrbitPlotter2D()

        Frame2dA.plot_body_orbit(Mars, date_launch)

        Frame2dA_div = plot(Frame2dA.plot_body_orbit(
            Earth, date_launch), output_type='div')

        # THE GOOD STUFF - Visualizing Desired Trajectory
        earth = Ephem.from_body(Earth, time_range(
            date_launch, end=date_arrival))
        mars = Ephem.from_body(Mars, time_range(date_launch, end=date_arrival))

        # Solve for departure and target orbits
        ss_earth = Orbit.from_ephem(Sun, earth, date_launch)
        ss_mars = Orbit.from_ephem(Sun, mars, date_arrival)

        # Solve for the transfer maneuver
        man_lambert = Maneuver.lambert(ss_earth, ss_mars)

        # Get the transfer and final orbits
        ss_trans, ss_target = ss_earth.apply_maneuver(
            man_lambert, intermediate=True)

        plotter = OrbitPlotter3D()
        plotter.set_attractor(Sun)

        plotter.plot_ephem(earth, date_launch,
                           label="Earth at launch position")
        plotter.plot_ephem(mars, date_arrival,
                           label="Mars at arrival position")
        plotter.plot_trajectory(
            ss_trans.sample(max_anomaly=180 * u.deg), color="black", label="Transfer orbit"
        )
        plotter_div = plot(plotter.set_view(
            30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

        return render(request, 'BluePages/simulator.html', {'launch_date': launch_date, 'arrival_date': arrival_date, 'Earth2dL_div': Earth2dL_div, 'Mars2dL_div': Mars2dL_div, 'Frame2dL_div': Frame2dL_div, 'Earth2dA_div': Earth2dA_div, 'Mars2dA_div': Mars2dA_div, 'Frame2dA_div': Frame2dA_div, 'plotter_div': plotter_div})

    else:
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
