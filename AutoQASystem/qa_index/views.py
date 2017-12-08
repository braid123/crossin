from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .forms import *
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


def questions(request, qid):
    if request.method == 'GET':
        question_id = qid
        qa = get_object_or_404(QAItem, id=qid)
        return render(request, 'question.html', {'qid': question_id,
                                                 'title': qa.title,
                                                 'description': qa.desc,
                                                 'answer': qa.answer})
    elif request.method == 'POST':
        comments = request.GET.get('comments')
        question_id = qid
        print(comments, question_id)
        return HttpResponse(1111111111111)


def ask(request):
    if request.method == 'GET':
        return render(request, 'ask.html')
    elif request.method == 'POST':
        question_title = request.POST.get('title')
        question_desc = request.POST.get('description')
        if question_desc and question_title:
             NewQAItem, is_new = QAItem.objects.get_or_create(title=question_title, desc=question_desc)
        return HttpResponseRedirect('/feedback.html')


def feedback(request):
    return render(request, 'feedback.html')