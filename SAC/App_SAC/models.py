from django.db import models
from django.contrib.auth import get_user_model

class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=24)
    email = models.CharField(max_length=120)
    observacao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nome
    
    
class Atendente(models.Model):
    nome_atend = models.CharField(max_length=120, null=False)
    telefone_atend = models.CharField(max_length=24, null=True)
    observacao_atend = models.TextField(null=True)
    criado_em_atend = models.DateTimeField(auto_now_add=True)
    atualizado_em_atend = models.DateTimeField(auto_now_add=True)
    ativo_atend = models.BooleanField()
    user_atend = models.ForeignKey(get_user_model(), null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome_atend


class Departamento(models.Model):
    descricao_departamento = models.CharField(max_length=30, null=False)
    info_departamento = models.TextField(null=True)
    ativo_departamento = models.BooleanField()

    def __str__(self):
        return self.descricao_departamento


class Situacao(models.Model):
    descricao_situacao = models.CharField(max_length=30, null=False)
    info_situacao = models.TextField(null=True)
    ativo_situacao = models.BooleanField()

    def __str__(self):
        return self.descricao_situacao


class Atendimento (models.Model):
    solicitacao = models.TextField()
    cliente = models.ForeignKey (Cliente, null=True, on_delete=models.PROTECT)
    departamento = models.ForeignKey (Departamento, null=True, on_delete=models.PROTECT)
    atendente = models.ForeignKey (Atendente, null=True, on_delete=models.PROTECT)
    criado_em = models. DateTimeField (auto_now_add=True)
    encerrado = models. BooleanField()

    def __str__(self):
        return self.id


class Situacao_Atendimento(models.Model):
    id_situacao = models.ForeignKey(Situacao, null=True, verbose_name='Situacao', related_name='situacoes', on_delete=models.PROTECT)
    id_atendimento = models.ForeignKey(Atendimento, null=True, verbose_name='Atendimento', related_name='atendimentos', on_delete=models.PROTECT)

    id_atendente = models.ForeignKey(Atendente, null=True, on_delete=models.PROTECT)

    comentario = models.TextField()
    data_hora = models.DateTimeField()

    def __str__(self):
        return self.comentario