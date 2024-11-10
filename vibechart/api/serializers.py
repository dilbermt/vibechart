from rest_framework import serializers

from .models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'id',
            'title',
            'url',
            'number_of_votes',
            'sample_property',
            'voters'
        ]
    voters = serializers.SerializerMethodField(read_only=True)
    def get_voters(self,obj):
        try:
            return obj.list_voters()
        except:
            return None