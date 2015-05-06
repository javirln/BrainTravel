# -*- coding: latin-1 -*-

from principal.models import Likes


def can_vote(id_traveller, id_feedback):
    return True if not Likes.objects.filter(traveller=id_traveller, feedback_id=id_feedback) else False
