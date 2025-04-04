from django.urls import path
from .views import get_nba_stats, get_team_stats, get_all_teams_stats, player_suggestions, team_suggestions, update_player_data, update_team_data, delete_player_data

urlpatterns = [
    path("get_nba_stats/", get_nba_stats, name="get_nba_stats"),
    path('api/get_team_stats/', get_team_stats, name='get_team_stats'),
    path("api/get_all_teams_stats/", get_all_teams_stats, name="get_all_teams_stats"),
    path("api/player_suggestions/", player_suggestions, name="player_suggestions"),
    path("api/team_suggestions/", team_suggestions, name="team_suggestions"),
    path("api/update_player_data/", update_player_data, name="update_player_data"),
    path("api/update_team_data/", update_team_data, name="update_team_data"),
    path("api/delete_player_data/", delete_player_data, name="delete_player_data"),
]
