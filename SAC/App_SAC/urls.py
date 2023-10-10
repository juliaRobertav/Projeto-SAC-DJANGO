from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'), #url ira chamar a função abre_index que está no arquivo views
    path('cad_cliente', views.cad_cliente, name='cad_cliente'),
    path('salvar_cliente_novo', views.salvar_cliente_novo, name='salvar_cliente_novo'),
    path('cons_cliente', views.cons_cliente, name='cons_cliente'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('excluir_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
    
    path('cad_atend', views.cad_atend, name='cad_atend'),
    path('salvar_atend_novo', views.salvar_atend_novo, name='salvar_atend_novo'),
    path('cons_atend', views.cons_atend, name='cons_atend'),
    path('edit_atend/<int:id>', views.edit_atend, name='edit_atend'),
    path('salvar_atend_editado', views.salvar_atend_editado, name='salvar_atend_editado'),

    path('cad_depto', views.cad_depto, name='cad_depto'),
    path('salvar_depto_novo', views.salvar_depto_novo, name='salvar_depto_novo'),
    path('cons_depto', views.cons_depto, name='cons_depto'),
    path('edit_depto/<int:id>', views.edit_depto, name='edit_depto'),
    path('salvar_depto_editado', views.salvar_depto_editado, name='salvar_depto_editado'),

    path('cad_situacao', views.cad_situacao, name='cad_situacao'),
    path('cons_situacao', views.cons_situacao, name='cons_situacao'),
    path('edit_situacao/<int:id>', views.edit_situacao, name='edit_situacao'),
    path('salvar_situacao_nova', views.salvar_situacao_nova, name='salvar_situacao_nova'),
    path('salvar_situacao_editada', views.salvar_situacao_editada, name='salvar_situacao_editada'),

    path('reg_atend_busca_cliente', views.reg_atend_busca_cliente, name='reg_atend_busca_cliente'),
    path('sel_cliente/<int:id>', views.sel_cliente, name='sel_cliente'),
    path('salvar_atendimento_novo', views.salvar_atendimento_novo, name='salvar_atendimento_novo'),

    path('reg_atendimento_api', views.reg_atendimento_api, name='reg_atendimento_api'),

    path('cons_lista_atendimento', views.cons_lista_atendimento, name='cons_lista_atendimento'),
]
