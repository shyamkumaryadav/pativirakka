from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.messaging_response import (
    MessagingResponse,
    Body,
    Message,
    Redirect,
    Media,
)


@csrf_exempt
def home(request):
    if request.method == "POST":
        print(request)

        msg = request.POST.get("Body")
        phone = request.POST.get("From")
        response = MessagingResponse()
        message = Message()
        if int(request.POST.get("NumMedia")) != 0:
            message.media(url="https://demo.twilio.com/owl.png")
        if msg != "":
            message.body(f"{phone} said:\n{msg}")
        response.append(message)
        return HttpResponse(str(response))
    return render(request, "index.html")
