from django.shortcuts import render
from django.views import View
from .models import ShortUrl
from django.shortcuts import redirect
from django.utils import timezone
import uuid

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'shortner/index.html')

    def post(self, request):
        url = request.POST.get('url')
        slug = str(uuid.uuid4())[0:8]
        if request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'
        host = request.get_host()
        slug = protocol + host + '/' + slug + '/'
        obj = ShortUrl.objects.create(slug= slug, original_url= url)
        context = {'url': url,
                   'slug': slug}

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
