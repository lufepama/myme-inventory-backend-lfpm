from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request, *args, **kwargs):

    try:
        user_data = request.data
        new_user_serializer = UserSerializer(data=user_data, context=user_data)

        if new_user_serializer.is_valid():
            new_user_serializer.save()
            return Response({'success': True, 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': new_user_serializer.errors}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    return Response({
                        'success': True,
                        'token': token.key,
                        'username': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email,
                        'msg': 'Loggin successfully'
                    }, status=status.HTTP_201_CREATED)
                else:
                    token.delete()
                    new_token = Token.objects.create(user=user)
                    return Response({
                        'success': True,
                        'token': new_token.key,
                        'username': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email,
                        'msg': 'Loggin successfully'

                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'El usuario no puede inciar sesion'}, status=status.HTTP_303_SEE_OTHER)
        else:
            return Response(login_serializer.errors, status=status.HTTP_303_SEE_OTHER)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        user = request.user
        token_user = Token.objects.get(user=user)
        token_user.delete()
        return Response({'success': True, 'msg': 'Logout successfully'}, status=status.HTTP_200_OK)

    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_403_FORBIDDEN)
