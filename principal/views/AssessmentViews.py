# -*- coding: iso-8859-1 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from principal.services import TripService, AssessmentService
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def assessment_list(request, trip_id):
    try:
        assert request.user.has_perm('principal.traveller')
        trip = TripService.find_one(trip_id)
        assert trip.traveller.id == request.user.id
        assessments = AssessmentService.find_all_id_trip(trip_id)

        paginator = Paginator(assessments, 5)
        page = request.GET.get('page')
        try:
            assessments = paginator.page(page)
        except PageNotAnInteger:
            assessments = paginator.page(1)
        except EmptyPage:
            assessments = paginator.page(paginator.num_pages)

        return render_to_response('assessment_list.html', {'assessments': assessments}, context_instance=RequestContext(request))
    except Exception:
        return render_to_response('error.html')