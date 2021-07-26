from django.shortcuts import render
from django.views import View
from .models import ShortUrl
from django.shortcuts import redirect
from django.http import Http404
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .forms import ShortUrlForm


# Create your views here.

class HomeView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {}
        user =  request.user
        urls = ShortUrl.objects.filter(user= user)
        if urls:
            context['urls'] = urls
       
        return render(request, 'shortner/index.html', context)

    @method_decorator(login_required())
    def post(self, request):
        url = request.POST.get('url')
        user = request.user
        urls = ShortUrl.objects.filter(user= user)
        slug = str(uuid.uuid4())[0:8]
        if request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'
        host = request.get_host()
        slug = protocol + host + '/' + slug + '/'
        obj = ShortUrl.objects.create(user= user, slug= slug, original_url= url)
        context = {'url': url,
                   'slug': slug}

        if urls:
            context['urls'] = urls

        return render(request, 'shortner/index.html', context)


def redirectView(request, slug):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    host = request.get_host()
    slug = protocol + host + '/' + slug + '/'
    obj = ShortUrl.objects.filter(slug= slug).first()
    if not obj.expired:
        return redirect(obj.original_url)
    else:
        raise Http404("URL does not exist")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username, password= password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'shortner/login.html', {'message': 'Incorrect Value Credentials, Please try again!'})
    return render(request, 'shortner/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))    

def signup(request):
    form = ShortUrlForm(request.POST, None)
    context = {}
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('login'))
    context['form'] = form
    return render(request, 'shortner/create_account.html', context)
