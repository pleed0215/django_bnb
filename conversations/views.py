from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.views.generic import DetailView

from users.models import User
from .models import Conversation, Message

# Create your views here.
def go_conversation (request, host_pk, guest_pk):
    host = User.objects.get_or_none (pk=host_pk)
    guest = User.objects.get_or_none (pk=guest_pk)

    print (host, guest)

    if host is not None and guest is not None:
        try:
            conversation = Conversation.objects.filter ( Q(participants__in=[host, guest])).first()
            print (conversation)
            
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create ()
            conversation.participants.add (host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}) )
    return redirect(reverse("core:home"))        


class ConversationDetailView (DetailView):
    
    model = Conversation