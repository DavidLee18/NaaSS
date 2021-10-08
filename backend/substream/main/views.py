from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Profile
from .serializers import ProfileSerializer

#profile api

@api_view(['GET'])
def profiles(request):
    ps = Profile.objects.all()
    return JsonResponse(ProfileSerializer(ps, many=True).data, safe=False)

@api_view(['GET'])
def profile(request, id):
    # find profile by (id)
    try: 
        p = Profile.objects.get(id=id)
        return JsonResponse(ProfileSerializer(p).data)
    except Profile.DoesNotExist: 
        return JsonResponse({'message': 'The profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def profile_edit(request, id):
    try: 
        p = Profile.objects.get(id=id)
        profile_data = JSONParser().parse(request)
        serializer = ProfileSerializer(p, data=profile_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist: 
        return JsonResponse({'message': 'The profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

# auth api

@api_view(['POST'])
def log_in(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            p = Profile.objects.get(user=user)
            return JsonResponse(ProfileSerializer(p).data)
        else:
            return JsonResponse({
                'message': 'username or password invalid or doesn\'t match any user'
            }, status=status.HTTP_400_BAD_REQUEST)
    except MultiValueDictKeyError:
        print(request.POST)
        return JsonResponse({'message': 'no username or password found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_out(request):
    try:
        logout(request)
        return HttpResponse(status=status.HTTP_200_OK)
    except:
        return JsonResponse({'message': 'error during logout'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)