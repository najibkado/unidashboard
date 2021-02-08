from .models import Event
from django.db import IntegrityError



def create_event(request, staff, desc):

    try:
        event = Event(
            creator = staff,
            desc = desc
        )
        event.save()
    except IntegrityError:
        pass

def get_my_events(request, user):

    try:
        return Event.objects.filter(creator=user)
    except Event.DoesNotExist:
        return None

def get_events(request):

    try:
        return Event.objects.all()
    except Event.DoesNotExist:
        return None