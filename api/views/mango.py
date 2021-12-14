from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..serializers.mango import MangoSerializer
from ..models.mango import Mango

class MangosView(APIView):
    def post(self, request):
        # Add the user id as owner
        request.data['owner'] = request.user.id
        mango = MangoSerializer(data=request.data)
        if mango.is_valid():
            mango.save()
            return Response(mango.data, status=status.HTTP_201_CREATED)
        else:
            return Response(mango.errors, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        # filter for mangos with our user id
        mangos = Mango.objects.filter(owner=request.user.id)
        data = MangoSerializer(mangos, many=True).data
        return Response(data)


class MangoView(APIView):
    def delete(self, request, pk):
        mango = get_object_or_404(Mango, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        mango.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        mango = get_object_or_404(Mango, pk=pk)
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        data = MangoSerializer(mango).data
        return Response(data)
    
    def patch(self, request, pk):
        mango = get_object_or_404(Mango, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        # Ensure the owner field is set to the current user's ID
        request.data['owner'] = request.user.id
        updated_mango = MangoSerializer(mango, data=request.data, partial=True)
        if updated_mango.is_valid():
            updated_mango.save()
            return Response(updated_mango.data)
        return Response(updated_mango.errors, status=status.HTTP_400_BAD_REQUEST)
