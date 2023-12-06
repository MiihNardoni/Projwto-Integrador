from django.urls import path

from . import views

urlpatterns = [

    path('pergunta/<int:question_id>/index/', 
    views.index, 
    name="poll_index"
    ),
    
    path('pergunta/<int:question_id>/detail/', 
    views.detail, 
    name="poll_detail"
    ),
    
    path('pergunta/<int:question_id>/results/', 
    views.results, 
    name="poll_results"
    ),
    
    path('<int:question_id>/vote/', 
    views.vote, 
    name="poll_vote"
    ),

    #class based views
    path('listar', views.QuestionListView.as_view(), name="question-list"),
    path('cadastrar', views.QuestionCreateView.as_view(), name="question-create"),
    path('<int:pk>', views.QuestionDetailView.as_view(), name="question-detail"),
    path('<int:pk>/deletar', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('<int:pk/atualizar', views.QuestionUpdateView.as_view(), name="question-update"),
    
    #rotas para criar, editar e deletar alternativas de perguntas
    path('pergunta/<int:pk>/alternativa/add', views.ChoiceCreateView.as_view(), name="choice_add"),
    path('pergunta/<int:pk>/alternativa/edit', views.ChoiceUpdateView.as_view(), name="choice_edit"),
    path('pergunta/<int:pk>/alternativa/delete', views.ChoiceDeleteView.as_view(), name="choice_delete")
]