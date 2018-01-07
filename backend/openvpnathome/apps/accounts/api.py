from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.generics import RetrieveAPIView

from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class AuthenticationApi(ViewSet):

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.data)
        if user:
            login(request, user)
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie('is_logged_in', "true")
            return response
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request):
        logout(request)
        response = HttpResponseRedirect('/')
        response.delete_cookie('is_logged_in')
        return response

    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie('is_logged_in', "true")
        return response


class UserApi(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
