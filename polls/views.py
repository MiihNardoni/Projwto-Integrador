from django.forms.models import BaseModeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from ast import Delete
from .models import Question, Choice

@login_required
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = Choice.objects.filter(question=question).aggregate(total=Sum('votes')) or 0
    total_votes = votes.get('total')
    context = {"question": question}

    context['votes'] + []
    for choice in question.choice_set.all():
        percentage = 0
        if choice.votes > 0 and total_votes > 0:
            percentage = choice.votes / total_votes * 100
        
        context['votes'].append(
            {
                'text': choice.choice_text,
                'votes': choice.votes,
                'percentage': round(percentage, 2)
            }
        )

    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = f'Resultados da pergunta de número {question_id}'
    return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'Selecione uma alternativa para votar')
        else:
            selected_choice.votes += 1
            selected_choice.save()
            messages.success(request, 'Seu voto foi registrado com sucesso')
            return redirect(reverse_lazy("poll_results", args=(question.id,)))
    context = {'question': question}
    return render(request, 'polls/question_detail.html', context)

from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ('question_text',)
    success_url = reverse_lazy('question-list')
    template_name = 'polls/question_form.html'
    success_message = 'Pergunta criada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        votes = Choice.objects.filter(question=context['question']).aggregate(total=Sum('votes')) or 0
        context['total_votes'] = votes.get('total')

        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.User
        dessages.success(self.request, self.success_message)
        return super(QuestionCreateView, self). form_valid(form)

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-pub_date']
    paginate_by: 5

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDeleteView, self). get_context_data(**kwargs)
        votes = Choice.objects.filter(question=context['question']).aggregate(total=Sum('votes')) or 0
        context['total_votes'] = votes.get('total')

        return context

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy("question-list")

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-pub_date']
    paginate_by = 5

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'polls/question_form.html'
    fiels = ('question_text',)
    success_url = reverse_lazy('question-list')
    success_message - 'Enquete atualizada com sucesso!'

    def get_context_data(self, **kwargs)
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a pergunta'

        question_id = self.kwargs.get('pk')
        choices = Choice.objects.filter(question__pk=question_id)
        context['question_choices'] = choices

        return context

    def form_valid(self, request, *args, **kwargs):
        messsages.success(self.request, self.success_message)

        return super(QuestionUpdateView, self).form_valid(request, *args, **kwargs)

class ChoiceCreateView(CreateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields =('choice_text', )
    success_message = 'Opção de voto regisitrada com sucesso!'

    def dispatch(self, request, *args, **kwargs):
        self.questuin - get_object_or_404(Question, pk=self.kwargs.get('pk'))

        return super(ChoiceCreateView, self).dispatch(request, *args. **kwargs)

    def get_context_data(self, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))

        context = super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Alternativa para: {question.question_text}'

        return context

    def form_valid(self, form):
            form.instance.question = self.question
            messsages.success(self.request, self.success_message)

            return super(ChoiceCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
            question_id = self.kwargs.get('pk')
            
            return reverse_lazy('poll_edit', kwargs={'pk': question_id})

class ChoiceUpdateView(UpdateView):
    model: Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Alternativa atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(ChoiceUpdateView, self).get_context_data(**kwargs)
        context['form_tittle'] = 'Editando Alternativa...'

        return context
    
    def form_valid(self, request, *args, **kwargs):
        messsages.success(self.request, self.success_message)

        return super(ChoiceUpdateView, self).form_valid(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id

        return reverse_lazy('poll_edit', kwargs={'pk': question_id})

class ChoiceDeleteView(LoginRequireMixin, DeleteView):
    model: Choice
    template_name ='polls/choice_confirm_delete_form.html'
    success_message ='Alternativa excluída com sucesso!'

    def form_valid(self, request, *args, **kwargs):
        messsages.success(self.request, self.success_message)

        return super(ChoiceDeleteView, self).form_valid(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id

        return reverse_lazy('poll_edit', kwargs={'pk': question_id})

@login_required
