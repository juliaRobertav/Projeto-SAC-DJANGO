
from rest_framework import viewsets
from App_SAC.api import serializers
from App_SAC import models
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClienteSerializer
    queryset = models.Cliente.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'telefone', 'email', 'observacao']