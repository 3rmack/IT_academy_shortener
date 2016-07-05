# from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from forms import UrlForm
from models import UrlList
from base62 import encode, decode


def index(request):
    if request.method == 'POST':
        raw_data = UrlForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data

            timestamp = timezone.now()
            original_url = data['original_url']

            url_add = UrlList.objects.create(original_url=original_url, date_add=timestamp, clicks=0)

            short_url = 'http://127.0.0.1:8000/?s={0}'.format(encode(url_add.id))
            url_add.shorten_url = short_url
            url_add.save()
            # shorten_decode = decode(shorten_encode)

            return redirect(index)
            # return HttpResponse('{0} time_add:{1} url_id:{2} encode:{3} decode:{4}'.format(data['original_url'], timestamp.strftime('%d-%m-%y %H:%M'), url_add.id, shorten_encode, shorten_decode))
        # context = {'articles_form': raw_data}
        return HttpResponse('bad')
    else:
        if request.GET.get('s'):
            s = request.GET.get('s')
            id = decode(s)
            url = UrlList.objects.get(id=id)

            timestamp = timezone.now()
            url.date_click = timestamp
            url.clicks += 1
            url.save()

            return redirect(url.original_url)
        else:
            urls = UrlList.objects.filter()
            context = {'url_form': UrlForm(), 'urls': urls}
            return render(request, 'form.html', context)


# def go(request):
#     s = request.GET.get('s')
#     id = decode(s)
#     url = UrlList.objects.get(id=id)
#     return HttpResponse('{0}'.format(url.original_url))
