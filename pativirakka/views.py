import requests
import re
import json
import bs4 as bs
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.forms import modelformset_factory, formset_factory, inlineformset_factory
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.contrib import messages
from twilio.rest import Client
from .forms import UserCreationForm, ExpUser
from .models import PativirakkaFrom, User, Experience
from django.db.models import F
from twilio.twiml.messaging_response import MessagingResponse, Message
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def test(request):
    context = {}
    UserExp = inlineformset_factory(
        User, Experience, form=ExpUser, extra=3)
    if request.method == "POST":
        form = UserExp(request.POST, request.FILES,
                       instance=request.user, prefix='article')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
        else:
            context['formset'] = form
    else:
        form = UserExp(prefix='article', instance=request.user)
        context['formset'] = form
    return render(request, 'form.html', context)


def home(request):
    context = {}
    if not request.user.is_authenticated:
        form_signup = UserCreationForm(request.POST or None)
        context['form_signup'] = form_signup
        if request.POST:
            if form_signup.is_valid():
                user = form_signup.save()
                login(request, user)
                messages.success(
                    request, 'Welcome {} ji.'.format(user.username))
                return HttpResponseRedirect(request.path)
    return render(request, "index.html", context)


def logIn(request):
    if request.method == 'POST':
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
    model = User
    fields = ('username', 'email', 'password', 'profile')
    success_url = '/'
    extra_context = {'title': 'User test'}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        raise Http404

    def post(self, request, *args, **kwargs):
        if request.user:
            return super().post(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = ChildFormset(self.request.POST)
        else:
            data["children"] = ChildFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("parents:list")



@csrf_exempt
def Pativirakka(request, *args, **kwargs):
    if request.method == 'POST':
        msg = request.POST.get("Body")
        phone = request.POST.get("From")
        pati, created = PativirakkaFrom.objects.get_or_create(contect=phone)
        if created:
            pati.save()
        response = MessagingResponse()
        message = Message(body = f"""
This bot is for *downloading Instagram public profile videos and images.* To download video 🎬 or Image 📸 just *share the public link of POST* with me I will send back your Image 📸 or Video 🎬.

~This also send a text which is inside a Image.~

If You are getting 404. You provide a privet link or wrong link 🔔.

            *🧔 Thank You !!!*

Find me on 🔥:\n
```Facebook & Instagram : @ishyamkumaryadav\n
Twitter: @shyamkumaryada\n
Reddit & GitHub 🌱 & telegram: @shyamkumaryadav```\n\n\n""")
        if pati.is_limit:
            urls = re.findall("(?P<url>https?://[^\s]+)", msg)
            print(urls)
            for url in urls:
                print(url) # Hope this work
                x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
                print(x)
                if x:
                    from faker import Faker
                    fake = Faker()
                    req = requests.get(url=url, headers={'User-Agent': fake.user_agent(), 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'})
                    print(req)
                    data=bs.BeautifulSoup(req.content, 'html.parser')
                    print(data)
                    type_ = data.find('meta', {'name':'medium'})['content']
                    print(type_)
                    message.media(url=data.find('head').find(property=f"og:{type_}")['content'])
                    if type_ == 'image':
                        try:
                            raw = data.find_all('script')[3].contents[0].replace('window._sharedData =', '').replace(';', '')
                            print(raw)
                            json_data = json.loads(raw)
                            print(json_data)
                            message.body(json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['accessibility_caption'])
                        except Exception as e:
                            print(type_, e)
                    print('Media * '*6)
                    PativirakkaFrom.objects.filter(
                        contect=phone).update(limit=F('limit') + 1)
            # except Exception as e:
            #     message.media(url="https://cdn.icon-icons.com/icons2/1483/PNG/512/404browser_102160.png")
            #     print(e)
        else:
            message.body('You complete your Trial. Please contact to admin@shyamkumaryadav using mention link on message 🌄')
        response.append(message)
        return HttpResponse(str(response))
    raise Http404
