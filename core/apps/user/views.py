from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request, *args, **kwargs):
    '''
        Manages the creation of a user. It makes use of serializer in which a custom validation is run
    '''
    try:
        # Get data from body
        user_data = request.data

        new_user_serializer = UserSerializer(data=user_data, context=user_data)

        if new_user_serializer.is_valid():
            new_user_serializer.save()
            return Response({'success': True, 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': new_user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(ObtainAuthToken):

    '''
        Manages the user login.
    '''

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
                    }, status=status.HTTP_200_OK)
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

                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'The user cannot login'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(login_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    '''
        Manages the user logout.
    '''

    try:
        user = request.user
        token_user = Token.objects.get(user=user)
        token_user.delete()
        return Response({'success': True, 'message': 'Logout successfully'}, status=status.HTTP_200_OK)
    except:
        return Response({'success': False, 'message': 'Something went wrong...'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
