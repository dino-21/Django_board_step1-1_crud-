from django.http import HttpResponse  # 삭제
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib import messages

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo2/question_list.html', context)



def detail(request, question_id):
    question =  get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo2/question_detail.html', context)



def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo2:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo2/question_detail.html', context)






def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo2:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo2/question_form.html', context)



# @login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # if request.user != question.author:
    #     messages.error(request, '수정권한이 없습니다')
    #     return redirect('pybo2:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo2:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo2/question_form.html', context)




# @login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # if request.user != question.author:
    #     messages.error(request, '삭제권한이 없습니다')
    #     return redirect('pybo2:detail', question_id=question.id)
    question.delete()
    return redirect('pybo2:index')




# @login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    # if request.user != answer.author:
    #     messages.error(request, '수정권한이 없습니다')
    #     return redirect('pybo2:detail',
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo2:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo2/answer_form.html', context)



# @login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    # if request.user != answer.author:
    #     messages.error(request, '삭제권한이 없습니다')
    # else:
    answer.delete()
    return redirect('pybo2:detail', question_id=answer.question.id)
