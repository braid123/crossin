from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
# Create your views here.


@method_decorator(login_required, 'get')
class MyClassView(View):
    """
    class base views test
    """
    def get(self, request):
        data = request.GET.get('data')
        return HttpResponse(data)


@method_decorator(csrf_exempt, 'dispatch')
class ItemSave(View):
    """
    项目条目问题接口
    """
    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        answer = request.POST.get('answer')
        try:
            item, is_new = QAItem.objects.get_or_create(
                title=title,
                desc=desc,
                answer=answer
            )
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
        else:
            return HttpResponse(json.dumps({'qid': item.id, 'is_new': is_new}))


class KeyToItem(View):
    """
    保存 "关键字-条目" 对应规则接口
    """
    def get(self, request):
        qid = request.GET.get('qid')
        key = request.GET.get('key')
        try:
            qa = get_object_or_404(QAItem, id=qid)
            keyword, is_new_key = KeyItem.objects.get_or_create(keyword=key)
            KeyToQA.objects.get_or_create(
                qa=qa,
                keyword=keyword
            )
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
        else:
            return HttpResponse(json.dumps({'kid': keyword.id, 'new_key': is_new_key}))


@csrf_exempt
def item_save(request):
    title = request.POST.get('title')
    desc = request.POST.get('desc')
    answer = request.POST.get('answer')
    try:
        item, is_new = QAItem.objects.get_or_create(
            title=title,
            desc=desc,
            answer=answer
        )
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'qid': item.id, 'is_new': is_new}))


def key_to_item(request):
    qid = request.GET.get('qid')
    key = request.GET.get('key')
    try:
        qa = get_object_or_404(QAItem, id=qid)
        keyword, is_new_key = KeyItem.objects.get_or_create(keyword=key)
        KeyToQA.objects.get_or_create(
            qa=qa,
            keyword=keyword
        )
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'kid': keyword.id, 'new_key': is_new_key}))
