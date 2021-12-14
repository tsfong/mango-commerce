from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
