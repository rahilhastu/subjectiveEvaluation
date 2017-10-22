from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import algo
from textwrap import dedent,wrap

def page (request):
    return render(request, 'en/public/index.html', {})

def question(request) :
    context = {}
    return render(request, 'en/public/question.html', context)

@csrf_exempt
def postdata(request):
    answer1 = request.POST['question1']
    answer2 = request.POST['question2']
    answer3 = request.POST['question3']
    file = open("studentAns.txt", "w")
    file.write('1 '+answer1+'\n')
    file.write("2 "+answer2+"\n")
    file.write("3 "+answer3)
    file.close()
    algo.fun()
    res = open('result.txt', 'r').readlines()
    context = {
        'res': res,
    }
    return render(request, 'en/public/result.html', context)


