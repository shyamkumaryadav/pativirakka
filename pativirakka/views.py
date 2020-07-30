import requests
import re
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

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.user:
            return super().post(request, *args, **kwargs)
        raise Http404


@csrf_exempt
def Pativirakka(request, *args, **kwargs):
    if request.POST:
        msg = request.POST.get("Body")
        phone = request.POST.get("From")
        response = MessagingResponse()
        message = Message()
        if len(msg) > 5:
            find_link = re.search("(?P<url>https?://[^\s]+)", msg)
            if find_link:
                link = find_link.group()
                instagram = Instagram_Image_Video_only_Public(url=link)
                message.body('url: \n', instagram)
        message.body(f"""This bot is for downloading Instagram public profile videos and images. To download video 🎬 or Image 📸 just share the link of POST with me I will send back your Image 📸 or Video 🎬. If You are Not getting Any think You should provide a privet post link or wrong link 🔔.

            *🧔 Thank You !!!*

Find me on 🔥:
```Facebook & Instagram : @ishyamkumaryadav
Twitter: @shyamkumatyada
Reddit & GitHub 🌱 & telegram: @shyamkumaryadav```""")
        response.append(message)
        return HttpResponse(str(response))
    raise Http404


def Instagram_Image_Video_only_Public(url="https://www.instagram.com/p/CB_GbiCsMQt"):
    try:
        x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
        if x:
            request_image = requests.get(url)
            src = request_image.content.decode('utf-8')
            check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)

            if final == "image":
                extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
                image_link = extract_image_link.group()
                image_url = re.sub('meta property="og:image" content="', '', image_link)
                return image_url

            if final == "video":
                extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
                video_link = extract_video_link.group()
                video_url = re.sub('meta property="og:video" content="', '', video_link)
                return video_url
    except:
        return None
