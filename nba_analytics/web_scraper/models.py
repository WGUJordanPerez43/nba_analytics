from django.db import models


class PlayerStats(models.Model):
    player_name = models.CharField(max_length=100)
    season = models.CharField(max_length=6)
    games_played = models.IntegerField(null=True, blank=True, default='')
    points_per_game = models.FloatField(null=True, blank=True, default='')
    assists_per_game = models.FloatField(null=True, blank=True, default='')
    rebounds_per_game = models.FloatField(null=True, blank=True, default='')

        #make sure that each player can only have one record per season
    class Meta:
        unique_together = ('player_name', 'season')


class TeamStats(models.Model):
    team_name = models.CharField(max_length=50)
    season = models.CharField(max_length=6)
    games_played = models.IntegerField(null=True, blank=True, default='')
    points_per_game = models.FloatField(null=True, blank=True, default='')
    assists_per_game = models.FloatField(null=True, blank=True, default='')
    rebounds_per_game = models.FloatField(null=True, blank=True, default='')


            #make sure that each team can only have one record per season
    class Meta:
        unique_together = ('team_name', 'season')
