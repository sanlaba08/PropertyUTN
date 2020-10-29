from datetime import datetime
from decimal import *
from random import random
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout, authenticate
from django.shortcuts import render, redirect
from .models import *
import random
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def index(request):
    cities = City.objects.all()
    properties = Property.objects.filter(rentaldate__date__gte=datetime.now(),
                                         rentaldate__reservation__isnull=True).distinct().order_by('id')
    context = {
        'properties': properties,
        'cities': cities
    }
    return render(request, '../templates/index.html', context)


# def my_reserved_properties1(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             return redirect('/admin/')
#         else:
#             rents_per_reservation = []
#             reservations = Reservation.objects.filter(
#                 rentaldate__reservation__isnull=False,
#                 rentaldate__property__owner__id=request.user.id
#             ).distinct().order_by('code')
#             for r in reservations:
#                 rents = RentalDate.objects.filter(reservation=r.id)  # array de fechas de alquiler con id de reserva
#                 rents_per_reservation.append(rents)  # array de array
#             return render(request, '../templates/my_reserved_properties.html', {'reservations': rents_per_reservation})


def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "../templates/register.html", {'form': form})


def login(request):
    return render(request, "../templates/login.html")


def my_reserved_properties(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect('/admin/')
                else:
                    rents_per_reservation = []
                    reservations = Reservation.objects.filter(
                        rentaldate__reservation__isnull=False,
                        rentaldate__property__owner__id=request.user.id
                    ).distinct().order_by('code')
                    for r in reservations:
                        rents = RentalDate.objects.filter(
                            reservation=r.id)  # array de fechas de alquiler con id de reserva
                        rents_per_reservation.append(rents)  # array de array
                    return render(request, '../templates/my_reserved_properties.html',
                                  {'reservations': rents_per_reservation})
            # return redirect('/admin/')

    return render(request, "../templates/login.html")


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')


def filter(request):
    cities = City.objects.all()
    if request.method == 'POST':
        filterProperty = Property.objects.all().filter(
            city=request.POST['idCity'],
            rentaldate__date__gte=request.POST['dateFrom'],
            rentaldate__date__lte=request.POST['dateTo'],
            rentaldate__reservation__isnull=True,
            maxPax__gte=request.POST['passengers']).distinct().order_by('id')
        context = {
            'properties': filterProperty,
            'cities': cities,
        }
        return render(request, '../templates/index.html', context)


def detail(request, id=0):
    if request.method == "GET":
        property = Property.objects.filter(id=id)
        rentalDates = RentalDate.objects.filter(property=id, reservation__isnull=True, date__gte=datetime.now())
        return render(request, '../templates/reservation.html', {'property': property, 'rentalDates': rentalDates, })
    return redirect('/')


def reserve(request, id=0):
    if request.method == "POST":

        property = Property.objects.get(id=id)

        listOfDays = request.POST.getlist('dateList')
        amountOfDays = len(listOfDays)
        totalCost = (property.dailyCost + property.dailyCost * Decimal(0.08)) * amountOfDays

        name = request.POST['name']
        lastName = request.POST['lastName']
        email = request.POST['email']
        pax = request.POST['pax']
        r = Reservation(property=property, name=name, lastName=lastName, email=email, totalCost=totalCost,
                        code=random.randrange(999, 99999), pax=pax)
        r.save()

        for idRentalDate in listOfDays:
            RentalDate.objects.filter(id=idRentalDate).update(reservation=r)

        return render(request, '../templates/thanks.html',
                      {'property': property, 'reservation': r,
                       'total': round(r.totalCost, 2)}, )
    return redirect('/')
