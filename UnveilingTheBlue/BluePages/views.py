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
        mission_name = request.POST['mission_name']
        launch_date = request.POST['launch_date']
        arrival_date = request.POST['arrival_date']

        # Set Date and Time
        datetime_launch = launch_date
        # print(datetime_launch)
        datetime_arrival = arrival_date
        # print(datetime_arrival)

        # Split Date and Time for Validation
        date_lst_launch = datetime_launch.split()
        date_lst_arrival = datetime_arrival.split()

        if not date_lst_launch or not date_lst_arrival or datetime_launch[0] == " " or datetime_launch[-1] == " " or datetime_arrival[0] == " " or datetime_arrival[-1] == " ":
            error_message = "Your Launch and Arrival Date Inputs don't seem to be working. Try again."
            return render(request, 'BluePages/simulator.html', {'error_message': error_message})
        else:
            dateL = date_lst_launch[0]
            dateA = date_lst_arrival[0]

        # Validate Launch and Arrival Dates
        def validate(date_text):
            try:
                datetime.datetime.strptime(date_text, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        if validate(dateL) and validate(dateA):
            launch_lst = date_lst_launch[0].split("-")
            dListL = [int(n) for n in launch_lst]

            arrival_lst = date_lst_arrival[0].split("-")
            dListA = [int(n) for n in arrival_lst]

            L_ = datetime.datetime(dListL[0], dListL[1], dListL[2])
            A_ = datetime.datetime(dListA[0], dListA[1], dListA[2])

            if L_ >= A_:
                error_message = "Your Launch and Arrival Date Inputs don't seem to be working. Try again."
                return render(request, 'BluePages/simulator.html', {'error_message': error_message})
            else:
                pass

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

            # Frame 3d Launch
            Frame3dL = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

            Frame3dL.plot_body_orbit(Earth, date_launch)
            Frame3dL.plot_body_orbit(Mars, date_launch)

            Frame3dL_div = plot(Frame3dL.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            # Earth Arrival
            Earth2dA = OrbitPlotter2D()

            Earth2dA_div = plot(Earth2dA.plot_body_orbit(
                Earth, date_arrival), output_type='div')

            # Mars Arrival
            Mars2dA = OrbitPlotter2D()

            Mars2dA_div = plot(Mars2dA.plot_body_orbit(
                Mars, date_arrival), output_type='div')

            # Frame Arrival
            Frame2dA = OrbitPlotter2D()

            Frame2dA.plot_body_orbit(Mars, date_arrival)

            Frame2dA_div = plot(Frame2dA.plot_body_orbit(
                Earth, date_arrival), output_type='div')

            # Frame 3d Arrival
            Frame3dA = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

            Frame3dA.plot_body_orbit(Earth, date_arrival)
            Frame3dA.plot_body_orbit(Mars, date_arrival)

            Frame3dA_div = plot(Frame3dA.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            # THE GOOD STUFF - Visualizing Desired Trajectory
            earth = Ephem.from_body(Earth, time_range(
                date_launch, end=date_arrival))
            mars = Ephem.from_body(Mars, time_range(
                date_launch, end=date_arrival))

            # Solve for Launch and Landing orbits
            ss_earth = Orbit.from_ephem(Sun, earth, date_launch)
            ss_mars = Orbit.from_ephem(Sun, mars, date_arrival)

            # Lambert's Problem
            man_lambert = Maneuver.lambert(ss_earth, ss_mars)

            # Render Trajectory
            ss_trans, ss_target = ss_earth.apply_maneuver(
                man_lambert, intermediate=True)

            final_traj = OrbitPlotter3D()
            final_traj.set_attractor(Sun)

            final_traj.plot_ephem(earth, date_launch,
                                  label="Earth at Launch Position")
            final_traj.plot_ephem(mars, date_arrival,
                                  label="Mars at Arrival Position")
            final_traj.plot_trajectory(
                ss_trans.sample(max_anomaly=180 * u.deg), color="black", label="Spacecraft's Trajectory"
            )
            final_traj_div = plot(final_traj.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            # Render Trajectory - 2d
            final_traj2d = OrbitPlotter2D()
            final_traj2d.set_attractor(Sun)

            final_traj2d.plot_body_orbit(
                Earth, date_launch, label="Earth at Launch Position", trail=True)

            final_traj2d.plot_trajectory(ss_trans.sample(
                max_anomaly=180 * u.deg), color="black", label="Spacecraft's Trajectory")

            final_traj2d_div = plot(final_traj2d.plot_body_orbit(
                Mars, date_arrival, label="Mars at Arrival Position", trail=True), output_type='div')

            return render(request, 'BluePages/simulator.html', {'mission_name': mission_name, 'launch_date': launch_date, 'arrival_date': arrival_date, 'Earth2dL_div': Earth2dL_div, 'Mars2dL_div': Mars2dL_div, 'Frame2dL_div': Frame2dL_div, 'Frame3dL_div': Frame3dL_div, 'Earth2dA_div': Earth2dA_div, 'Mars2dA_div': Mars2dA_div, 'Frame2dA_div': Frame2dA_div, 'Frame3dA_div': Frame3dA_div, 'final_traj_div': final_traj_div, 'final_traj2d_div': final_traj2d_div})
        else:
            error_message = "Your Launch and Arrival Date Inputs don't seem to be working. Try again."
            return render(request, 'BluePages/simulator.html', {'error_message': error_message})

    else:
        return render(request, 'BluePages/simulator.html', {})


def spaceExploration(request):
    return render(request, 'BluePages/spaceExploration.html', {})


def astrodev(request):
    return render(request, 'BluePages/astrodev.html', {})


def interplanetaryFlight(request):
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
    return render(request, 'BluePages/interplanetaryFlight.html',  context={'frame_div': frame_div, 'solarsys_div': solarsys_div})


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
