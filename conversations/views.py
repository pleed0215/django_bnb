from django.shortcuts import render

from users.models import User
from .models import Conversation, Message

# Create your views here.
def go_conversation (request, host_pk, guest_pk):
    pass