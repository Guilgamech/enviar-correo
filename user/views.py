import mailqueue.receivers
from django.core.mail import send_mail
from mailqueue.models import MailerMessage
from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from enviocorreo import settings
from user.models import CustomUser
from user.serializer import LogoutSerializer, UserSerializer


class LogoutView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = LogoutSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=None, status=status.HTTP_205_RESET_CONTENT)


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    queryset = CustomUser.objects.all()

    @action(detail=False, methods=["post"])
    def registrar(self, request):
        user_serializer = UserSerializer(data = request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            usuario_new = user_serializer.data['username']
            subject = "Activa tu cuenta"
            message = "Hola " + usuario_new + " Activate"
            email_from = settings.EMAIL_HOST_USER
            user_new_email = user_serializer.data["email"]
            send =MailerMessage(subject=subject, content=message, from_address=email_from, to_address=user_new_email)
            send.save()
            send.send_mail()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)


    @action(detail=False, methods=["get"])
    def activarCuenta(self, request):
        user: CustomUser = self.request.user
        read = UserSerializer(user)
        return Response({"user": read.data}, status=status.HTTP_200_OK)
