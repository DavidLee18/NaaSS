from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view


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