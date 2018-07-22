# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import views, status
from .serializers import UserSerializer, SSHKeySerializer, MessageSerializer
from sparta_webapp.users.models import UserKey, User
from sparta_webapp.common.models import ServerGroup,ServerInfor,CommandsSequence,Credential
from .serializers import ServerGroupSerializer, ServerInforSerializer, CommandsSequenceSerializer, CredentialSerializer

### API ViewSets ###

class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(queryset, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(queryset, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_202_ACCEPTED
        )

class SSHKeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users SSHKey to be viewed or edited.
    """
    queryset = UserKey.objects.all().order_by('-name')
    serializer_class = SSHKeySerializer

    @action(methods=['post'], detail=True)
    def add_key(self, request, pk=None):
        pass

class UserCreate(generics.CreateAPIView):
    """
    Create a User
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a User
    """
    queryset = User.objects.all()


class ServerGroupViewSet(viewsets.ModelViewSet):
    queryset = ServerGroup.objects.all()
    serializer_class = ServerGroupSerializer


class ServerInforViewSet(viewsets.ModelViewSet):
    queryset = ServerInfor.objects.all()
    serializer_class = ServerInforSerializer

class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer


class CommandsSequenceViewSet(viewsets.ModelViewSet):
    queryset = CommandsSequence.objects.all()
    serializer_class = CommandsSequenceSerializer
    serializer_class = UserSerializer
