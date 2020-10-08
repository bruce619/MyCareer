from accounts.api.serializers import UserSerializer, ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from ..models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from .serializers import AuthCustomTokenSerializer
from django.core.exceptions import ObjectDoesNotExist


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data['response'] = "successfully registered new user"
            data["email"] = user.email
            token = Token.objects.get(user=user).key
            data["token"] = token
            data["status"] = status.HTTP_201_CREATED
            headers = self.get_success_headers(serializer.data)
            data["headers"] = headers

        else:
            data = serializer.errors
        return Response(data)


class CustomAuthToken(auth_views.ObtainAuthToken):
    serializer_class = AuthCustomTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


obtain_auth_token = CustomAuthToken.as_view()


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_user_api_view(request):

    try:
        users = User.objects.all()
        profile = Profile.objects.all()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    staff_user = request.user.is_staff

    admin_user = request.user.is_admin

    if not staff_user and not admin_user:
        return Response({'Response': 'You do not have the permission to view this'})

    if request.method == 'GET':
        user_serializer = UserSerializer(users, many=True)
        profile_serializer = ProfileSerializer(profile, many=True)
        return JsonResponse({'users': user_serializer.data,
                             'profile': profile_serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_update_profile_api_view(request):

    user = request.user.id

    try:
        my_profile = Profile.objects.filter(user=user)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(my_profile, many=True)
        return JsonResponse({"profile": serializer.data}, safe=False, status=status.HTTP_200_OK)

    try:
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not profile:
        return Response({'Response': 'You do not have the permission to edit / delete this'})

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'profile': serializer.data}, safe=False, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'profile': serializer.data}, safe=False, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




