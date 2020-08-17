from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.views.generic import View
from django.contrib import messages


from users.models import User
from .models import Conversation, Message
from .forms import MessageForm

# Create your views here.
def go_conversation(request, host_pk, guest_pk):
    host = User.objects.get_or_none(pk=host_pk)
    guest = User.objects.get_or_none(pk=guest_pk)

    print(host, guest)

    if host is not None and guest is not None:
        try:
            conversation = Conversation.objects.filter(Q(participants=host)).filter(
                Q(participants=guest)
            )
            if conversation.count() == 0:
                raise Conversation.DoesNotExist()

            conversation = conversation.first()
            print(conversation)

        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))
    return redirect(reverse("core:home"))


class ConversationDetailView(View):

    form = MessageForm()

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")

        conversation = Conversation.objects.get_or_none(pk=pk)

        if conversation is not None:
            return render(
                self.request,
                "conversations/conversation_detail.html",
                {"object": conversation, "form": self.form},
            )

        messages.error(self.request, "Illegal access")
        return redirect(reverse("core:home"))

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        print(kwargs)
        posted_message = self.request.POST.get("message", None)
        conversation = Conversation.objects.get_or_none(pk=pk)

        if conversation is not None and posted_message is not None:
            Message.objects.create(
                message=posted_message,
                user=self.request.user,
                conversation=conversation,
            )
            return redirect(
                reverse("conversations:detail", kwargs={"pk": conversation.pk})
            )
        return redirect(reverse("core:home"))
