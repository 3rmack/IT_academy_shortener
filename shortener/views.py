# coding: UTF-8
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from forms import UrlForm
from models import UrlList
from base62 import encode, decode


def index(request):
    if request.method == 'POST':  # обрабатываем POST запрос, т.е. добавления url
        raw_data = UrlForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data

            timestamp = timezone.now()  # отметка времени
            original_url = data['original_url']  # получаем введенный в форму url
            url_add = UrlList.objects.create(original_url=original_url, date_add=timestamp, clicks=0)  # пишем в базу введенный url, время добавления и количество кликов, которые пока равны нулю

            request_url = request.get_raw_uri()  # получаем url запроса
            short_url = '{0}?s={1}'.format(request_url, encode(url_add.id))  # формируем короткий url из url запроса и закодированного id записи
            url_add.shorten_url = short_url  # добавляем короткий url в базу
            url_add.save()  # сохраняем

            return redirect(index)  # добавление url в базу окончена, перенаправляем на заглавную страницу

        # если введенный url прошел валидацию на форме html, но не прошел в обработке POST запроса, то выводим сообщение пользователю о некорректном url
        urls = UrlList.objects.filter()
        context = {'url_form': UrlForm(), 'urls': urls, 'message': 'You pasted a bad URL'}
        return render(request, 'form.html', context)
    else:  # обрабатываем GET запрос
        if request.GET.get('s'):  # если в GET запросе существет ключ s, значит пользователь нажал на короткий url - обрабатываем его
            s = request.GET.get('s')  # получаем закодированный id
            '''
            Если пользователь вручную введет GET запрос в адресной строке браузера с произвольным 's',
            то приложение может обратиться к базе с несуществующим id, что вызовет exception.
            Ловим такие обращения с помощью try-except и выводим соответствующее сообщение.
            '''
            try:
                url_id = decode(s)  # декодируем id
                url = UrlList.objects.get(id=url_id)  # получаем объект url из базы

                timestamp = timezone.now()  # отметка времени
                url.date_click = timestamp  # дата и время клика по короткому url
                url.clicks += 1  # увеличиваем счетчик кликов по короткому url
                url.save()  # сохраняем изменения в базу
            except Exception:  # ловим ошибки обращения к несуществующему id в базе
                request_url = request.get_raw_uri()  # получаем url запроса
                return HttpResponse('Page "{0}" does not exist.'.format(request_url))  # возвращаем пользователю сообщение, что такого url нет
            return redirect(url.original_url)  # выносим редирект на оригинальный url из try блока, т.к. в нем не считаются клики и timestamps
        else:  # если в GET запросе нет ключа s, значит пользователь заходит на заглавную страницу
            urls = UrlList.objects.filter()  # получаем все записи в базе
            context = {'url_form': UrlForm(), 'urls': urls}
            return render(request, 'form.html', context)  # рисуем пользователю заглавную страницу
