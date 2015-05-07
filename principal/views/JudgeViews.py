# -*- coding: latin-1 -*-

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from principal.models import Judges, Trip, Traveller, CoinHistory


@login_required()
def judge(request, trip_id, like):
    try:
        assert request.user.has_perm("principal.traveller")

        trip = Trip.objects.get(id=trip_id)
        traveller = Traveller.objects.get(id=request.user.id)

        assert trip.state == 'ap'
        assert trip.traveller.id != request.user.id

        count_judges = Judges.objects.filter(trip_id=trip_id, traveller_id=traveller.id).count()

        if like == '0':
            like = False
        else:
            like = True

        if count_judges == 0:

            # Crear 'judge'
            new_judge = Judges(
                trip=trip,
                traveller=traveller,
                like=like
            )
            new_judge.save()

            # Contar las entradas que tiene el viajero para el viaje (maximo 1)
            new_count_judges = Judges.objects.filter(trip_id=trip_id, traveller_id=traveller.id).count()
            assert new_count_judges == 1

            if like:

                # Obtener el viaje e incrementar el 'like'
                trip = Trip.objects.get(id=trip_id)
                trip.likes += 1
                trip.save()

                if (trip.likes % 5) == 0:

                    # Obtener el viajero que ha realizado el viaje
                    traveller_trip = Traveller.objects.get(id=trip.traveller.id)
                    traveller_trip.coins += long(2)
                    traveller_trip.save()

                    # Crear un nuevo 'coin history'
                    new_coin_history = CoinHistory(
                        amount=2,
                        date=datetime.now(),
                        concept="Gift for number of likes",
                        traveller=traveller_trip
                    )
                    new_coin_history.save()

            else:
                # Obtener el viaje e incrementar el 'dislike'
                trip = Trip.objects.get(id=trip_id)
                trip.dislikes += 1
                trip.save()
        else:
            list_judges = Judges.objects.filter(trip_id=trip_id, traveller_id=traveller.id)
            judges = list(list_judges)[0]

            if judges.like != like:

                judges.like = like
                judges.save()

                if like:
                    trip = Trip.objects.get(id=trip_id)
                    trip.dislikes -= 1
                    trip.likes += 1
                    trip.save()

                else:
                    trip = Trip.objects.get(id=trip_id)
                    trip.dislikes += 1
                    trip.likes -= 1
                    trip.save()
        return HttpResponseRedirect('/public_trip_details/' + trip_id)

    except:
        return render_to_response('error.html', context_instance=RequestContext(request))