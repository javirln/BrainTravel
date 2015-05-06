# -*- coding: latin-1 -*-
from principal.models import Assessment


def find_all_id_trip(trip_id):
    assessments = Assessment.objects.filter(scorable_id=trip_id)
    return assessments
