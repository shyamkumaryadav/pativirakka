from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from twilio.rest import Client
from twilio.twiml.messaging_response import (
    MessagingResponse,
    Body,
    Message,
    Redirect,
    Media,
)


def home(request):
    context = {}
    if not request.user.is_authenticated:
        form = AuthenticationForm(request.POST or None)
        context['form'] = form
    if request.POST:
        if form.is_valid():
            login(request, form.get_user())
    return render(request, "index.html", context)


def logIn(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None and password:
            user = authenticate(
                request, username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Please enter the correct username and password.'}, safe=False)
            else:
                login(request, user)
                return HttpResponse('ok')
    else:
        raise Http404


class UserCreate(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    model = get_user_model()
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        return super().get(request, *args, **kwargs)


@csrf_exempt
def Pativirakka(request, *args, **kwargs):
    if request.POST:
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
    raise Http404
