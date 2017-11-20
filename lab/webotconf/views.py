from django.shortcuts import render, get_object_or_404
# from .models import ChatRoom, RuleAddFriend
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from PIL import Image
import re
from labcrm.views import ImgForm
import datetime
# Create your views here.


@login_required
def rule_conf(request):
    if request.method == 'POST':
        is_strict = request.POST.get('is_strict')
        list_keywords = request.POST.getlist('keywords')
        if is_strict == 'True':
            list_orders = [int(order) + 100 for order in request.POST.getlist('orders')]
            list_room = ['#' + room for room in request.POST.getlist('rooms')]
        else:
            list_orders = request.POST.getlist('orders')
            list_room = request.POST.getlist('rooms')
        rules = zip(list_room, list_orders, list_keywords)
        print(len(list_keywords), len(list_orders), len(list_room))
        if len(set(list_room)) < len(list_room):
            return HttpResponse()
        for rule in rules:
            keywords = re.split(r'[,，;；.。| +-]+', rule[2].strip(',，;；.。| +-'))
            print(rule, keywords)
            room, _ = ChatRoom.objects.update_or_create(nickname=rule[0], defaults={
                'order': rule[1]
            })
            for keyword in keywords:
                RuleAddFriend.objects.get_or_create(
                    keyword=keyword,
                    chatroom=room
                )
        if is_strict == 'True':
            rooms = ChatRoom.objects.all().filter(order__gt=100).order_by('order')
        else:
            rooms = ChatRoom.objects.all().filter(order__lt=100).order_by('order')
        return HttpResponse(render(request, 'webotconf/ajax/rules.html', {
            'rooms': rooms,
            'is_strict': is_strict
        }))
    elif request.GET.get('strict'):
        rooms = ChatRoom.objects.all().filter(order__gt=100).order_by('order')
        is_strict = 'True'
    else:
        rooms = ChatRoom.objects.all().filter(order__lt=100).order_by('order')
        is_strict = 'False'
    return render(request, 'webotconf/webot.html', {
        'rooms': rooms,
        'is_strict': is_strict
    })


@login_required
def qa_conf_strict(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        desc = request.POST.get('desc')
        answer = request.POST.get('answer')
        is_modify = request.POST.get('modify')
        print('keyword: ', keyword)
        print('desc: ', desc)
        print('answer: ', answer)
        print('is_modify: ', is_modify)
        qa_keyword, is_new = QAKeyWord.objects.get_or_create(keyword=keyword, is_strict=True)
        form_data = ImgForm(request.POST, request.FILES)
        if is_modify:
            qa_keyword = get_object_or_404(QAKeyWord, keyword=keyword, is_strict=True)
            qa_reply = get_object_or_404(QAReply, keywords=qa_keyword)
            qa_reply.desc = desc
            qa_reply.reply_text = answer
            # qa_reply.save()
            # return HttpResponse(render(request, 'webotconf/ajax/qa_group.html', {
            #     'keyword': qa_keyword,
            # }))
        elif is_new:
            qa_reply = QAReply.objects.create(
                desc=desc,
                reply_text=answer,
            )
            qa_reply.keywords.add(qa_keyword)
        else:
            return HttpResponse()
        if form_data.is_valid():
            pic = form_data.cleaned_data['pic']
            qa_reply.reply_pic = pic
            qa_reply.is_pic = True
        qa_reply.save()
        return HttpResponse(render(request, 'webotconf/ajax/qa_group.html', {
            'keyword': qa_keyword,
        }))
    delete_kid = request.GET.get('delete')
    print('delete_kid: ', delete_kid)
    if delete_kid:
        qa_keyword = get_object_or_404(QAKeyWord, id=delete_kid)
        qa_reply = get_object_or_404(QAReply, keywords=qa_keyword)
        qa_keyword.delete()
        qa_reply.delete()
        return HttpResponse()
    keywords = QAKeyWord.objects.filter(is_strict=True).order_by('keyword')
    return render(request, 'webotconf/qa_conf.html', {
        'keywords': keywords,
        'is_strict_qa': 'True'
    })


@login_required
def qa_conf(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        desc = request.POST.get('desc')
        answer = request.POST.get('answer')
        is_modify = request.POST.get('modify')
        print('keyword: ', keyword)
        print('desc: ', desc)
        print('answer: ', answer)
        print('is_modify: ', is_modify)
    keywords = QAKeyWord.objects.filter(is_strict=False)
    return render(request, 'webotconf/qa_conf.html', {
        'keywords': keywords,
        'is_strict_qa': 'False'
    })


@login_required
def pic_subject(request):
    sid = request.GET.get('close')
    rid = request.GET.get('reSub')
    if sid:
        print('sid: ', sid)
        subject = get_object_or_404(PicSubject, id=sid)
        subject.is_underway = False
        subject.time_off = datetime.datetime.now()
        subject.save()
        print('subject: ', subject, subject.is_underway, subject.time_off)
        return HttpResponse(render(request, 'webotconf/ajax/sub_history.html', {
            'subjectHis': subject
        }))
    elif request.method == 'POST':
        tag = request.POST.get('tag')
        reply = request.POST.get('reply')
        subject = PicSubject.objects.create(
            tag=tag,
            reply=reply,
            time_on=datetime.datetime.now()
        )
        return HttpResponse(render(request, 'webotconf/ajax/sub_underway.html', {
            'subject': subject
        }))
    elif rid:
        subject = get_object_or_404(PicSubject, id=rid)
        subject.is_underway = True
        subject.save()
        return HttpResponse(render(request, 'webotconf/ajax/sub_underway.html', {
            'subject': subject
        }))
    subject = PicSubject.objects.filter(is_underway=True).last()
    subject_history = PicSubject.objects.filter(is_underway=False)
    return render(request, 'webotconf/pic_subject.html', {
        'is_pic': True,
        'subject': subject,
        'subject_history': subject_history
    })


@login_required
def ajax_conf_modify(request):
    is_strict = request.GET.get('strict')
    print('is_strict: ', is_strict, type(is_strict), is_strict==False)
    if is_strict == 'True':
        rooms = ChatRoom.objects.all().filter(order__gt=100).order_by('order')
    else:
        rooms = ChatRoom.objects.all().filter(order__lt=100).order_by('order')
    return HttpResponse(render(request, 'webotconf/ajax/modify.html', {
        'rooms': rooms,
        'is_strict': is_strict
    }))
