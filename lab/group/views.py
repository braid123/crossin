from django.shortcuts import render
from testools.declog import log_this
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
# from ..labcrm import models
import labcrm.models
from group import models


@log_this
@login_required
def student_group(request):
    if request.method == 'POST':
        return _student_group_post(request)
    else:
        return _student_group_get(request)


@log_this
def _student_group_get(request):
    groups = models.StudentGroup.objects.all()
    users = labcrm.models.LabUser.objects.filter(is_del=False).order_by('-user__date_joined')
    group_id = request.GET.get('group', 0)
    print('group_id:', group_id)
    if group_id != 0:
        group = models.StudentGroup.objects.get(id=group_id)
        return render(request, 'group/student.html', {
            'users': users,
            'groups': groups,
            'group': group,
        })
    elif group_id == 0:
        return render(request, 'group/student.html', {
                'users': users,
                'groups': groups,
                'group': group_id
            })


@log_this
def _student_group_post(request):
    groupname = request.POST.get('groupname')
    groupnote = request.POST.get('groupnote')
    groupid = request.POST.get('groupid', 0)
    if groupname and groupnote:
        group, is_new = models.StudentGroup.objects.get_or_create(group_name=groupname,group_note=groupnote)
        if is_new:
            return HttpResponse(group.group_name, group.group_note)
        else:
            return HttpResponse()
    elif not groupid:
        studentgroup = request.POST.getlist('studentgroup')
        newgroup = request.POST.get('selectgroup')
        newgrouptest = get_object_or_404(models.StudentGroup, id=newgroup)
        students = labcrm.models.LabUser.objects.filter(id__in=studentgroup)
        for student in students:
            student.group = newgrouptest
            student.save()
        groups = models.StudentGroup.objects.all()
        users = labcrm.models.LabUser.objects.filter(is_del=False).order_by('-user__date_joined')
        group_id = request.GET.get('group', 0)
        print('group_id:', group_id)
        if group_id != 0:
            group = models.StudentGroup.objects.get(id=group_id)
            return render(request, 'group/student.html', {
                'users': users,
                'groups': groups,
                'group': group,
            })
        elif group_id == 0:
            return render(request, 'group/student.html', {
                'users': users,
                'groups': groups,
                'group': group_id
            })
    elif groupid:
        print('groupid', groupid)
        return HttpResponse()
