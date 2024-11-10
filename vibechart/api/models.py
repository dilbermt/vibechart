from django.db import models


# Create your models here.
class Song(models.Model):
    title= models.CharField(max_length=256)
    url = models.CharField(max_length=300)
    number_of_votes = models.IntegerField(default=0)

    def upvote(self):
        return "upvote"

    def downvote(self):
        return "downvote"

    def supervote(self):
        return "supervote"

    def list_voters(self):
        return "list voters"

    # sample property
    @property
    def sample_property(self):
        return "sample property"

class Votes(models.Model):
    song_id = models.IntegerField(models.ForeignKey("Song", on_delete=models.CASCADE))