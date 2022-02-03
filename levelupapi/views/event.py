from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


class EventView(ViewSet):
#match pk that comes from url
    def retrieve(self, request, pk):
        try:
            event= Event.objects.get(pk=pk)
            serializer= Event(event)
            return Response(serializer.data)
        except  Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        events=Event.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            events = events.filter(game_type_id=game_type)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
       
    def create(self, request):
 
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            serializer = CreateEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(organizer=gamer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('game','description','date','time','organizer','attendees')
        depth = 2
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','game','description','date','time','organizer','attendees']