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
import math
import plotly.graph_objects as go

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

import requests
'''
class BlueView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'BluePages/index.html', context={
            }
        )
'''


def home(request):
    response = requests.get("https://api.spacexdata.com/v4/launches")
    launches = response.json()

    flight_numbers = []
    patches = []
    names = []
    details = []
    date_utc = []

    for launch in launches:
        flight_numbers.append(launch["flight_number"])
        names.append(launch['name'])
        details.append(launch['details'])
        if "links" in launch:
            link_dict = launch["links"]
            if "patch" in link_dict:
                patch_keys = link_dict["patch"]
                if "large" in patch_keys:
                    patches.append(patch_keys['large'])

    print(flight_numbers)
    print(patches)

    flight_numbers.reverse()
    patches.reverse()
    names.reverse()
    details.reverse()

    cards = []
    n = 0
    for _ in flight_numbers:
        cards.append([flight_numbers[n], patches[n], names[n], details[n]])
        n += 1

    print(cards)

    def Sort(cards_sort):
        cards_sort.sort(key=lambda x: x[0])
        return cards_sort

    cards = Sort(cards)

    cards.reverse()

    return render(request, 'BluePages/index.html', {'cards': cards})


def simulator(request):
    if request.method == "POST":
        mission_name = request.POST['mission_name']
        origin = request.POST['origin']
        destination = request.POST['destination']
        launch_date = request.POST['launch_date']

        print(mission_name)

        # Set Date and Time
        datetime_launch = launch_date
        # print(datetime_launch)

        # Split Date and Time for Validation
        date_lst_launch = datetime_launch.split()

        if not date_lst_launch or datetime_launch[0] == " " or datetime_launch[-1] == " ":
            error_message = "Your Launch and Arrival Date Inputs don't seem to be working. Try again."
            return render(request, 'BluePages/simulator.html', {'error_message': error_message})
        else:
            dateL = date_lst_launch[0]

        # Validate Launch and Arrival Dates
        def validate(date_text):
            try:
                datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
                return True
            except ValueError:
                return False

        if validate(dateL):
            launch_lst = date_lst_launch[0].split("-")
            dListL = [int(n) for n in launch_lst]

            L_ = datetime.datetime(dListL[0], dListL[1], dListL[2])

            # Curiosity: 2011-11-26 15:02, Perserverance: 2020-6-30 11:50
            date_launch = time.Time(datetime_launch, scale="utc").tdb
            # Curiosity: 2012-08-06 05:17 Perserverance: 2021-2-18 12:30

            planets = {"Mercury": Mercury, "Venus": Venus, "Earth": Earth, "Mars": Mars,
                       "Jupiter": Jupiter, "Saturn": Saturn, "Uranus": Uranus, "Neptune": Neptune}

            origin_planet_inp = str(origin)
            destination_planet_inp = str(destination)

            origin_planet = planets[origin_planet_inp]
            destination_planet = planets[destination_planet_inp]

            # Origin Planet Launch
            Origin2dL = OrbitPlotter2D()

            Origin2dL_div = plot(Origin2dL.plot_body_orbit(
                origin_planet, date_launch), output_type='div')

            # Destination Planet Launch
            Destination2dL = OrbitPlotter2D()

            Destination2dL_div = plot(Destination2dL.plot_body_orbit(
                destination_planet, date_launch), output_type='div')

            # Frame Launch
            Frame2dL = OrbitPlotter2D()

            Frame2dL.plot_body_orbit(destination_planet, date_launch)

            Frame2dL_div = plot(Frame2dL.plot_body_orbit(
                origin_planet, date_launch), output_type='div')

            # Planeatary Positions, Velocities, Orbits at Launch
            # launch_planetary_positions = OrbitPlotter2D()

            origin_position = Ephem.from_body(origin_planet, date_launch)
            origin_orbit = Orbit.from_ephem(Sun, origin_position, date_launch)

            destination_position = Ephem.from_body(
                destination_planet, date_launch)
            destination_orbit = Orbit.from_ephem(
                Sun, destination_position, date_launch)

            # launch_planetary_positions.plot(origin_orbit)

            # launch_planetary_positions_div = plot(launch_planetary_positions.plot(destination_orbit), output_type='div')

            # Frame 3d Launch
            Frame3dL = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

            Frame3dL.plot_body_orbit(origin_planet, date_launch)
            Frame3dL.plot_body_orbit(destination_planet, date_launch)

            Frame3dL_div = plot(Frame3dL.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            print(origin_orbit.r)
            print(origin_orbit.v)
            print(origin_orbit.a)

            print(destination_orbit.r)
            print(destination_orbit.v)
            print(destination_orbit.a)

            sun_mu = 1.32712e11

            origin_sm_axis = origin_orbit.a
            destination_sm_axis = destination_orbit.a

            spacecraft_sm_axis = (origin_sm_axis + destination_sm_axis) / 2.0
            spacecraft_ecc = 1 - origin_sm_axis / destination_sm_axis

            transfer_time = np.pi * np.sqrt(spacecraft_sm_axis ** 3 / sun_mu)

            print(float(str(origin_sm_axis).strip("km")))
            print(float(str(destination_sm_axis).strip("km")))

            print(float(str(spacecraft_sm_axis).strip("km")))
            print(float(str(spacecraft_ecc).strip("km")))

            print(float(str(transfer_time / 60 / 60 / 24).rstrip('km(3/2)')))

            v_origin = np.sqrt(sun_mu / float(str(origin_sm_axis).strip("km")))
            v_destination = np.sqrt(
                sun_mu / float(str(destination_sm_axis).strip("km")))

            v_spacecraft_depart = np.sqrt(sun_mu * (2.0 / float(str(origin_sm_axis).strip(
                "km")) - 1.0 / float(str(spacecraft_sm_axis).strip("km"))))
            v_spacecraft_arrive = np.sqrt(sun_mu * (2.0 / float(str(destination_sm_axis).strip(
                "km")) - 1.0 / float(str(spacecraft_sm_axis).strip("km"))))

            deltaV_depart = v_spacecraft_depart - v_origin
            deltaV_arrive = v_destination - v_spacecraft_arrive

            print(v_origin)
            print(v_spacecraft_depart)
            print(deltaV_depart)

            print(v_destination)
            print(v_spacecraft_arrive)
            print(deltaV_arrive)

            print(float(str(transfer_time / 60 / 60 / 24).rstrip('km(3/2)')))

            print(int(round(float(str(transfer_time / 60 / 60).rstrip('km(3/2)')), 1)))

            date_time_str = launch_date
            date_time_obj = datetime.datetime.strptime(
                date_time_str, '%Y-%m-%d %H:%M:%S')

            transfer_time_hours = int(
                round(float(str(transfer_time / 60 / 60).rstrip('km(3/2)')), 1))

            datetime_transfer = datetime.timedelta(hours=transfer_time_hours)
            arrival_date = str(date_time_obj + datetime_transfer)

            print(arrival_date)

            date_launch = time.Time(launch_date, scale="utc").tdb
            date_arrival = time.Time(arrival_date, scale="utc").tdb

            # Origin Planet Arrival
            Origin2dA = OrbitPlotter2D()

            Origin2dA_div = plot(Origin2dA.plot_body_orbit(
                origin_planet, date_arrival), output_type='div')

            # Destination Planet Arrival
            Destination2dA = OrbitPlotter2D()

            Destination2dA_div = plot(Destination2dA.plot_body_orbit(
                destination_planet, date_arrival), output_type='div')

            # Frame Arrival
            Frame2dA = OrbitPlotter2D()

            Frame2dA.plot_body_orbit(destination_planet, date_arrival)

            Frame2dA_div = plot(Frame2dA.plot_body_orbit(
                origin_planet, date_arrival), output_type='div')

            # Frame 3d Arrival
            Frame3dA = OrbitPlotter3D(plane=Planes.EARTH_ECLIPTIC)

            Frame3dA.plot_body_orbit(origin_planet, date_arrival)
            Frame3dA.plot_body_orbit(destination_planet, date_arrival)

            Frame3dA_div = plot(Frame3dA.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            # Visualizing Desired Trajectory
            origin_ephem = Ephem.from_body(
                origin_planet, time_range(date_launch, end=date_arrival))
            destination_ephem = Ephem.from_body(
                destination_planet, time_range(date_launch, end=date_arrival))

            # Solve for Launch and Landing orbits
            origin_orbit = Orbit.from_ephem(Sun, origin_ephem, date_launch)
            destination_orbit = Orbit.from_ephem(
                Sun, destination_ephem, date_arrival)

            # Lambert's Problem
            man_lambert = Maneuver.lambert(origin_orbit, destination_orbit)

            # Render Trajectory
            transfer_orbit, target_orbit = origin_orbit.apply_maneuver(
                man_lambert, intermediate=True)
            print(transfer_orbit)

            flight_path = OrbitPlotter3D()
            flight_path.set_attractor(Sun)

            flight_path.plot_ephem(
                origin_ephem, date_launch, label="{} at Launch Position".format(origin_planet))
            flight_path.plot_ephem(
                destination_ephem, date_arrival, label="{} at Arrival Position".format(destination_planet))

            flight_path.plot_trajectory(transfer_orbit.sample(
                max_anomaly=180 * u.rad), label="Flight Path")

            flight_path_div = plot(flight_path.set_view(
                30 * u.deg, 260 * u.deg, distance=3 * u.km), output_type='div')

            # Flight Path - 2d
            flight_path2d = OrbitPlotter2D()
            flight_path2d.set_attractor(Sun)

            flight_path2d.plot_body_orbit(
                origin_planet, date_launch, label="{} at Launch Position".format(origin_planet), color='#1b60a5', trail=True)

            flight_path2d.plot_trajectory(transfer_orbit.sample(
                max_anomaly=180 * u.rad), color='#269321', label="Flight Path")

            flight_path2d_div = plot(flight_path2d.plot_body_orbit(
                destination_planet, date_arrival, color='#fd6b10', label="{} at Arrival Position".format(destination_planet), trail=True), output_type='div')

            return render(request, 'BluePages/simulator.html', {
                'mission_name': mission_name,
                'origin_planet': origin_planet,
                'destination_planet': destination_planet,
                'launch_date': launch_date,
                'arrival_date': arrival_date,
                'Origin2dL_div': Origin2dL_div,
                'Destination2dL_div': Destination2dL_div,
                'Frame2dL_div': Frame2dL_div,
                'Frame3dL_div': Frame3dL_div,
                'Origin2dA_div': Origin2dA_div,
                'Destination2dA_div': Destination2dA_div,
                'Frame2dA_div': Frame2dA_div,
                'Frame3dA_div': Frame3dA_div,
                'flight_path_div': flight_path_div,
                'flight_path2d_div': flight_path2d_div
            })
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
