from django import template
from rooms.models import Room
from lists.models import List

register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_fav(context, room_pk):
    print(room_pk)
    room = Room.objects.get_or_none(pk=room_pk)

    if room is not None:
        fav_list = List.objects.get_or_none(
            user=context.request.user, name="favorite list")
        if fav_list:
            return room in fav_list.rooms.all()

    return False
