from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=100)
    maker = models.CharField(max_length=100)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)