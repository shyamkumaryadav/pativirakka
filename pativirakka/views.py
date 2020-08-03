import requests
import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.forms import modelformset_factory, formset_factory
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.contrib import messages
from twilio.rest import Client
from .models import PativirakkaFrom, Person
from django.db.models import F
from twilio.twiml.messaging_response import (
    MessagingResponse,
    Body,
    Message,
    Redirect,
    Media,
)


def manage_authors(request):
    AuthorFormSet = formset_factory(Person, extra=3)
    if request.method == "POST":
        formset = AuthorFormSet(
            request.POST, request.FILES
        )
        if formset.is_valid():
            user = formset.save()
            return HttpResponse("is Valid")
    else:
        formset = AuthorFormSet()
    return render(request, 'form.html', {'form': formset})


def Instagram_Image_Video_only_Public(url):
    try:
        x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
        if x:
            request_ = requests.get(url)
            src = request_.content.decode('utf-8')
            check_type = re.search(
                r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)
            print(final)

            if final == "image":
                extract_image_link = re.search(
                    r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
                image_link = extract_image_link.group()
                image_url = re.sub(
                    'meta property="og:image" content="', '', image_link)
                print(image_url)
                return image_url

            elif final == "video":
                extract_video_link = re.search(
                    r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
                video_link = extract_video_link.group()
                video_url = re.sub(
                    'meta property="og:video" content="', '', video_link)
                print(video_url)
                return video_url
        else:
            print('id asle not find')
            return False
    except Exception as e:
        print(e)
        pass


def home(request):
    context = {}
    if not request.user.is_authenticated:
        form_signup = UserCreationForm(request.POST or None)
        # form_login = AuthenticationForm(request.POST or None)
        # context['form_login'] = form_login
        context['form_signup'] = form_signup
        if request.POST:
            if form_signup.is_valid():
                user = form_signup.save()
                messages.success(
                    request, 'The user "{}" was successfully created.'.format(user.username))
                login(request, user)
                messages.success(
                    request, 'Welcome {} ji.'.format(user.username))
                return HttpResponseRedirect(request.path)
    return render(request, "index.html", context)


def logIn(request):
    if request.POST:
        username = request.POST.get('username_login')
        password = request.POST.get('password_login')
        if username is not None and password is not None:
            user = authenticate(
                request, username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Please enter the correct username and password.'}, safe=False)
            else:
                login(request, user)
                messages.success(
                    request, 'Welcome {} ji.'.format(user.username))
                return HttpResponse('ok')
    else:
        raise Http404


def logOut(request):
    logout(request)
    messages.success(request, 'Logout.')
    return HttpResponseRedirect('/')


class UserCreate(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    model = get_user_model()
    success_url = '/'
    extra_context = {'title': 'Sign Up'}

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
        pati, created = PativirakkaFrom.objects.get_or_create(contect=phone)
        if created:
            pati.save()
        response = MessagingResponse()
        message = Message()
        message.body(f"""
This bot is for *downloading Instagram public profile videos and images.* To download video 🎬 or Image 📸 just *share the public link of POST* with me ~I will send back your Image 📸 or Video 🎬.~

If You are Not getting Any think You should provide a privet link or wrong link 🔔.

            *🧔 Thank You !!!*

Find me on 🔥:\n
```Facebook & Instagram : @ishyamkumaryadav\n
Twitter: @shyamkumatyada\n
Reddit & GitHub 🌱 & telegram: @shyamkumaryadav```\n\n""")
        if pati.is_limit:
            urls = re.findall("(?P<url>https?://[^\s]+)", msg)
            print(urls)
            for url in urls:
                print(url)
                instagram = Instagram_Image_Video_only_Public(url)
                print(instagram)
                if instagram:
                    message.media(url=instagram)
                    print('Media * '*6)
                    PativirakkaFrom.objects.filter(
                        contect=phone).update(limit=F('limit') + 1)
                    break
        else:
            message.body('\n\n\nHow are you 🌄')
            print('Not url * ' * 6)
        response.append(message)
        return HttpResponse(str(response))
    raise Http404
