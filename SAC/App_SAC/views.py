from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from datetime import datetime
from .models import Cliente, Atendente, Departamento, Situacao, Atendimento, Situacao_Atendimento
from django.contrib.auth.models import User


# estrutura das funções
def abre_index(request):
    usuario_logado = request.user.username
    return render(request, 'index.html', {'usuario_logado': usuario_logado})


@login_required
def cad_cliente(request):
    usuario_logado = request.user.username
    return render(request, 'cad_cliente.html', {'usuario_logado': usuario_logado})


@login_required
def salvar_cliente_novo(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        grava_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            email=email,
            observacao=observacao
        )
        grava_cliente.save()
        messages.info(request, 'Cliente ' + nome + ' cadastrado com sucesso!')
        return render(request, 'cad_cliente.html', {'usuario_logado': usuario_logado})


@login_required
def cons_cliente(request):
    usuario_logado = request.user.username
    dado_pesquisa_nome = request.POST.get('cliente')
    dado_pesquisa_telefone = request.POST.get('telefone')
    dado_pesquisa_email = request.POST.get('email')

    page = request.GET.get('page')
    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        usuarios = Cliente.objects.filter(nome__icontains=dado_pesquisa)
        usuario_paginator = Paginator(usuarios, 3)
        page = usuario_paginator.get_page(page)
        return render(request, 'edit_cliente.html',
                      {'page': page, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})

    if dado_pesquisa_nome != None and dado_pesquisa_nome != '':
        clientes_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        usuario_paginator = Paginator(clientes_lista, 3)
        page = request.GET.get('page')
        clientes = usuario_paginator.get_page(page)
        return render(request, 'cons_cliente_lista.html',
                      {'page': clientes, 'dado_pesquisa': dado_pesquisa_nome, 'usuario_logado': usuario_logado})

    elif dado_pesquisa_telefone != None and dado_pesquisa_telefone != '':
        clientes = Cliente.objects.filter(telefone__icontains=dado_pesquisa_telefone)
        return render(request, 'cons_cliente_lista.html', {'page': clientes, 'usuario_logado': usuario_logado})

    elif dado_pesquisa_email != None and dado_pesquisa_email != '':
        clientes = Cliente.objects.filter(email__icontains=dado_pesquisa_email)
        return render(request, 'cons_cliente_lista.html', {'page': clientes, 'usuario_logado': usuario_logado})

    else:
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado})


@login_required
def edit_cliente(request, id):
    usuario_logado = request.user.username
    dados_editar = get_object_or_404(Cliente, pk=id)
    return render(request, 'edit_cliente.html', {'dados_do_cliente': dados_editar, 'usuario_logado': usuario_logado})


@login_required
def salvar_cliente_editado(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_cliente = request.POST.get('id_cliente')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')

        Cliente_Editado = Cliente.objects.get(id=id_cliente)

        Cliente_Editado.nome = nome
        Cliente_Editado.telefone = telefone
        Cliente_Editado.email = email
        Cliente_Editado.observacao = observacao

        Cliente_Editado.save()

        messages.info(request, 'Cliente ' + nome + ' editado com sucesso!')
        return render(request, 'cons_cliente_lista.html', {'usuario_logado': usuario_logado})


@login_required
def delete_cliente(request, id):
    usuario_logado = request.user.username
    cliente_deletado = get_object_or_404(Cliente, pk=id)
    nome = cliente_deletado.nome
    cliente_deletado.delete()

    messages.info(request, 'Cliente ' + nome + ' excluído com sucesso...')
    return redirect('cons_cliente', {'usuario_logado': usuario_logado})


@login_required
def cad_atend(request):
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})


@login_required
def salvar_atend_novo(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        nome_atend = request.POST.get('nome_atend')
        telefone_atend = request.POST.get('telefone_atend')
        user_atend = request.POST.get('user_atend')
        observacao_atend = request.POST.get('observacao_atend')
        if user_atend:
            user_atend=User.objects.get(username=user_atend)
        else:
            user_atend = None

        grava_atend = Atendente(
            nome_atend=nome_atend,
            telefone_atend=telefone_atend,
            observacao_atend=observacao_atend,
            ativo_atend=1,
            user_atend=user_atend
        )
        grava_atend.save()
        messages.info(request, 'atendente ' + nome_atend + ' cadastrado com sucesso.')
        cons_users = User.objects.all()
        return render(request, 'Cad_Atendente.html', {'usuario_logado': usuario_logado, 'cons_users': cons_users})


@login_required
def cons_atend(request):

    dado_pesquisa_atendente = request.POST.get('atendente')
    dado_pesquisa_todos = request.POST.get('seleciona_todos')

    usuario_logado = request.user.username

    if dado_pesquisa_todos == 'N' and dado_pesquisa_atendente != None :
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)

    elif dado_pesquisa_todos == 'S' and dado_pesquisa_atendente != None :
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente , ativo_atend=1)

    elif dado_pesquisa_todos == 'N' and dado_pesquisa_atendente == None :
       todos_atendentes = Atendente.objects.all()

    else:

       todos_atendentes  = Atendente.objects.filter(ativo_atend=1)

    page = request.GET.get('page')

    if page :
       #page = request.GET.get('page')
       dado_pesquisa =  request.GET.get('dado_pesquisa')
       atendentes_lista = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa)
       paginas = Paginator(atendentes_lista, 3)  # 3 representa o número de atendentes por página
       atendentes = paginas.get_page(page)
       return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})



    if dado_pesquisa_atendente != None and dado_pesquisa_atendente != '':
       todos_atendentes = Atendente.objects.filter(nome_atend__icontains=dado_pesquisa_atendente)

       paginas = Paginator(todos_atendentes, 3) # 3 representa o número de atendentes por página

       page = request.GET.get('page')

       atendentes = paginas.get_page(page)


       return render(request, 'Cons_Atendente.html', {'todos_atendentes': atendentes, 'dado_pesquisa': dado_pesquisa_atendente, 'usuario_logado': usuario_logado})

    else:

       return render(request, 'Cons_Atendente.html', {'todos_atendentes': todos_atendentes, 'usuario_logado': usuario_logado})

@login_required

def edit_atend(request, id):
    dados_editar = get_object_or_404(Atendente, pk=id)
    cons_users = User.objects.all()
    usuario_logado = request.user.username
    return render(request, 'Edit_Atendente.html', {'dados_do_atendente': dados_editar, 'cons_users': cons_users , 'usuario_logado': usuario_logado})

@login_required
def salvar_atend_editado(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_atend = request.POST.get('id_atend')
        nome_atend = request.POST.get('nome_atend')
        telefone_atend = request.POST.get('telefone_atend')
        user_atend = request.POST.get('user_atend')
        observacao_atend = request.POST.get('observacao_atend')
        ativo_atend = request.POST.get('ativo_atend')

        if user_atend:
            user_atend = User.objects.get(username=user_atend)
        else:
            user_atend = None  # Define a variável como Null

        Atende_Editado = Atendente.objects.get(id=id_atend)

        Atende_Editado.nome_atend = nome_atend
        Atende_Editado.telefone_atend = telefone_atend
        Atende_Editado.observacao_atend = observacao_atend
        Atende_Editado.user_atend = user_atend

        if ativo_atend:
            Atende_Editado.ativo_atend = 1
        else:
            Atende_Editado.ativo_atend = 0

        Atende_Editado.save()

        messages.info(request, 'Atendente ' + nome_atend + ' editado com sucesso.')
        return render(request, 'Cons_Atendente.html', {'usuario_logado': usuario_logado})


@login_required
def cad_depto(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_depto_novo(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        descricao_departamento = request.POST.get('depto')
        info_departamento = request.POST.get('informacao')
        grava_depto = Departamento(
            descricao_departamento=descricao_departamento,
            info_departamento=info_departamento,
            ativo_departamento=1
        )
        grava_depto.save()
        messages.info(request, 'Departamento ' + descricao_departamento + ' cadastrado com sucesso!')
        return render(request, 'Cad_Depto.html', {'usuario_logado': usuario_logado})

@login_required
def cons_depto(request):

    dado_pesquisa_depto = request.POST.get('departamento')
    usuario_logado = request.user.username

    if dado_pesquisa_depto != '' and dado_pesquisa_depto != None:
        todos_departamentos = Departamento.objects.filter(descricao_departamento__icontains=dado_pesquisa_depto)
        return render(request, 'Cons_Depto.html', {'todos_departamentos': todos_departamentos, 'dado_pesquisa': dado_pesquisa_depto, 'usuario_logado': usuario_logado})
    else:
        todos_departamentos = Departamento.objects.all()
        return render(request, 'Cons_Depto.html', {'todos_departamentos': todos_departamentos, 'dado_pesquisa': dado_pesquisa_depto, 'usuario_logado': usuario_logado})

@login_required
def edit_depto(request, id):
    dados_depto_editar = get_object_or_404(Departamento, pk=id)
    usuario_logado = request.user.username
    return render(request, 'Edit_Depto.html',
                  {'dados_do_depto': dados_depto_editar, 'usuario_logado': usuario_logado})

@login_required
def salvar_depto_editado(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_depto = request.POST.get('id_depto')
        descricao_departamento = request.POST.get('depto')
        info_departamento = request.POST.get('informacao')

        # ativo_departamento = request.POST.get('ativo_departamento')

        Departamento_Editado = Departamento.objects.get(id=id_depto)

        Departamento_Editado.descricao_departamento = descricao_departamento
        Departamento_Editado.info_departamento = info_departamento

        # Departamento_Editado.ativo_departamento = 1

        Departamento_Editado.save()

        messages.info(request, 'Departamento ' + descricao_departamento + ' editado com sucesso.')
        return render(request, 'Cons_Depto.html', {'usuario_logado': usuario_logado})


@login_required
def cad_situacao(request):
    usuario_logado = request.user.username
    return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def salvar_situacao_nova(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
       descricao_situacao = request.POST.get('situacao')
       info_situacao = request.POST.get('informacao')

       grava_situacao = Situacao(
           descricao_situacao=descricao_situacao,
           info_situacao=info_situacao,
           ativo_situacao=1
       )
       grava_situacao.save()
       messages.info(request, 'SItuação ' + descricao_situacao + ' cadastrada com sucesso !!!')
       return render(request, 'Cad_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def cons_situacao(request):

    dado_pesquisa_situacao = request.POST.get('situacao')
    dado_pesquisa_todos = request.POST.get('seleciona_todos')

    usuario_logado = request.user.username

    page = request.GET.get('page')

    if page :
       #page = request.GET.get('page')
       dado_pesquisa =  request.GET.get('dado_pesquisa')

       if dado_pesquisa != None :
          situacoes_lista = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa)
       else :
          situacoes_lista = Situacao.objects.all()

       paginas = Paginator(situacoes_lista, 3)  # 3 representa o número de atendentes por página
       situacoes = paginas.get_page(page)
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': dado_pesquisa, 'usuario_logado': usuario_logado})


    if dado_pesquisa_todos == 'N' and dado_pesquisa_situacao != None :
       todas_situacoes = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa_situacao)

    elif dado_pesquisa_todos == 'S' and dado_pesquisa_situacao != None :
       todas_situacoes = Situacao.objects.filter(descricao_situacao__icontains=dado_pesquisa_situacao, ativo_situacao=1)

    elif dado_pesquisa_todos == 'N' and dado_pesquisa_situacao == None :
       todas_situacoes = Situacao.objects.all()

    else:
       todas_situacoes  = Situacao.objects.filter(ativo_situacao=1)

    paginas = Paginator(todas_situacoes, 3)  # 3 representa o número de atendentes por página
    page = request.GET.get('page')
    situacoes = paginas.get_page(page)

    if dado_pesquisa_situacao != None :
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': dado_pesquisa_situacao, 'usuario_logado': usuario_logado})
    else :
       return render(request, 'Cons_Situacao.html', {'todas_situacoes': situacoes, 'dado_pesquisa': '', 'usuario_logado': usuario_logado})

@login_required
def edit_situacao(request, id):
    dados_situacao_editar = get_object_or_404(Situacao, pk=id)
    usuario_logado = request.user.username
    return render(request, 'Edit_Situacao.html', {'dados_da_situacao': dados_situacao_editar, 'usuario_logado': usuario_logado})


@login_required
def salvar_situacao_editada(request):
    usuario_logado = request.user.username
    if (request.method == 'POST'):
        id_situacao = request.POST.get('id_situacao')
        descricao_situacao = request.POST.get('descricao_situacao')
        info_situacao = request.POST.get('informacao')
        ativo_situacao = request.POST.get('ativo_situacao')


        Situacao_Editado = Situacao.objects.get(id=id_situacao)

        Situacao_Editado.descricao_situacao = descricao_situacao
        Situacao_Editado.info_situacao = info_situacao


        if ativo_situacao:
            Situacao_Editado.ativo_situacao = 1
        else:
            Situacao_Editado.ativo_situacao = 0

        Situacao_Editado.save()

        messages.info(request, 'Situação ' + descricao_situacao + ' editado com sucesso !!!')
        return render(request, 'Cons_Situacao.html', {'usuario_logado': usuario_logado})

@login_required
def reg_atend_busca_cliente(request):
    usuario_logado = request.user.username
    dado_pesquisa_nome = request.POST.get('sel_cliente')
    cons_depto = Departamento.objects.all()
    data_e_hora = datetime.now()
    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    page = request.GET.get('page')

    if page:
        dado_pesquisa = request.GET.get('dado_pesquisa')
        clientes_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa)
        paginas = Paginator(clientes_lista, 3)
        clientes = paginas.get_page(page)
        return render(request, 'Reg_Atendimento_busca.html', {'dados_clientes': clientes, 'dado_pesquisa':dado_pesquisa,
                              'usuario_logado':usuario_logado, 'cons_depto':cons_depto, 'data_e_hora':data_e_hora})

    if dado_pesquisa_nome != None and dado_pesquisa_nome != '':
        clientes_lista = Cliente.objects.filter(nome__icontains=dado_pesquisa_nome)
        paginas = Paginator(clientes_lista, 2)
        page = request.GET.get('page')
        clientes = paginas.get_page(page)
        return render(request, 'Reg_Atendimento_busca.html',
                      {'dados_clientes': clientes, 'dado_pesquisa': dado_pesquisa_nome, 'usuario_logado': usuario_logado,
                       'cons_depto': cons_depto, 'data_e_hora': data_e_hora})

    else:
        return render(request, 'Reg_Atendimento_busca.html', {'usuario_logado': usuario_logado,
                       'cons_depto': cons_depto, 'data_e_hora': data_e_hora})

@login_required
def sel_cliente(request, id):
    usuario_logado = request.user.username
    cons_depto = Departamento.objects.all()
    data_e_hora = datetime.now()
    data_e_hora = data_e_hora.strftime("%d/%n/%Y %H:%M:%S")
    dados_clientes = get_object_or_404(Cliente, pk=id)
    return render(request, 'Reg_Atendimento_busca.html', {'cliente_sel': dados_clientes, 'usuario_logado': usuario_logado,
                                                          'cons_depto': cons_depto, 'data_e_hora': data_e_hora})

@login_required
def salvar_atendimento_novo(request):
    usuario_logado = request.user.username
    id_atendente = request.user.id
    cons_users = User.objects.all()
    cons_depto = Departamento.objects.all()

    data_e_hora = datetime.now()

    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    if (request.method == 'POST'):
        solicitacao = request.POST.get('solicitacao')
        cliente = request.POST.get('id_cliente')
        departamento = request.POST.get('encaminhar')

        cliente = Cliente.objects.get(id=cliente)

        if departamento:
            departamento = Departamento.objects.get(id=departamento)
        else:
            departamento = None

        situacao = Situacao.objects.get(id=1)

        print("Cheguei aqui antes de instancia Atendente")
        print(id_atendente)

        atendente = Atendente.objects.filter(user_atend_id=id_atendente).last()
        print("cheguei aqui antes de gravar")

        grava_atendimento = Atendimento(
            solicitacao=solicitacao,
            cliente=cliente,
            departamento=departamento,
            atendente=atendente,
            criado_em=datetime.now(),
            encerrado=0
        )
        grava_atendimento.save()
        cons_ultimo = Atendimento.objects.last()
        print(cons_ultimo.id)
        comentario = "Registro automático ao criar o chamado"
        atendimento = Atendimento.objects.get(id=cons_ultimo.id)

        grava_situacao_atendimento = Situacao_Atendimento(
            id_situacao=situacao,
            id_atendimento=atendimento,
            id_atendente = atendente,
            comentario=comentario,
            data_hora=datetime.now()
        )
        grava_situacao_atendimento.save()

        messages.info(request, 'Atendimento ' + str(cons_ultimo.id) + ' registrado com sucesso.')
        return render(request, 'Reg_Atendimento_API.html', {'usuario_logado': usuario_logado,
                                                            'cons_users': cons_users,
                                                            'cons_depto': cons_depto,
                                                            'data_e_hora': data_e_hora,
                                                            })

@login_required
def reg_atendimento_api(request):
    usuario_logado = request.user.username
    cons_users = User.objects.all()
    cons_depto = Departamento.objects.all()

    data_e_hora = datetime.now()

    data_e_hora = data_e_hora.strftime("%d/%m/%Y %H:%M:%S")

    return render(request, 'Reg_Atendimento_API.html', {'usuario_logado': usuario_logado,
                                                        'cons_users':cons_users,
                                                        'cons_depto': cons_depto,
                                                        'data_e_hora': data_e_hora})

@login_required
def cons_lista_atendimento(request):
    usuario_logado = request.user.username

    dado_pesquisa_numero = request.POST.get('numero')

    if dado_pesquisa_numero:
        atendimento = Atendimento.objects.filter(id=dado_pesquisa_numero)
        if atendimento:
            return render(request, 'Cons_Atendimento.html', {'atendimento':atendimento, 'dado_pesquisa':dado_pesquisa_numero, 'usuario_logado':usuario_logado})
        else:
            ultimo_atendimento = Atendimento.objects.last()

            seis_ultimos = ultimo_atendimento.id - 5 # pega o número dos últimos 6 atendimentos

            # Opcoes de filtros para aplicar no instanciamento de objeto DJANGO
            # Greater than use __gt
            #Greater than or equal use __gte
            # Less than use __lt
            # Less than use __lte

            # Para odrder by desc use order_by('-firstname')
            # Para odrder by asc use order_by('-firstname')

            atendimento = Atendimento.objects.filter(id__gte=seis_ultimos).order_by('-id')

            return render(request, 'Cons_Lista_Atendimento.html', {'atendimento':atendimento, 'usuario_logado':usuario_logado})