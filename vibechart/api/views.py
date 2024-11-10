from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import SongSerializer
from .models import Song

@api_view(["GET"])
def home(request, *args, **kwargs):

    instance = Song.objects.all().order_by("?").first()

    data = {}

    if instance:
        data = SongSerializer(instance).data
    return Response(data)

@api_view(["POST"])
def add_song(request,*args,**kwargs):
    # data = request.data
    # print("data ->",data)

    # validate the incoming data
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # print("data", serializer.data)
        # save to db
        instance = serializer.save()
        data = serializer.data
    return Response(data)
   
@api_view(["GET"])
def get_song_details(request,id=None,*args,**kwargs):
    if id is not None:
        instance = Song.objects.filter(id=id).first()
        if not instance:
            return Response({"error":"not found"},404)
        data = SongSerializer(instance).data
        return Response(data)
    queryset = Song.objects.all()
    data = SongSerializer(queryset,many=True).data
    return Response(data)

@api_view(["PUT"])
def update_song(request,id=None,*args, **kwargs):
    if id is not None:
        instance = Song.objects.filter(id=id).first()
        data = request.data
        print("request data--->>>",data)
        serializer = SongSerializer(instance,data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            data = serializer.data
            return Response(data,status=status.HTTP_200_OK)
    return Response({"error":"id not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
def delete_song(request,id=None,*args,**kwargs):
    if id is not None:
        instance = Song.objects.filter(id=id).first()

        if instance is None:
            return Response({"error":"Song not found"},status=status.HTTP_404)
        
        instance.delete()
        return Response({"message":"Song deleted successfully"},status=status.HTTP_200_OK)
    
    return Response({"error":"Id not provided"},status=status.HTTP_400_BAD_REQUEST)