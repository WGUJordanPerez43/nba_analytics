"""
URL configuration for nba_analytics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web_scraper.views import get_nba_stats, get_team_stats, get_all_teams_stats, player_suggestions, team_suggestions, update_player_data, update_team_data, delete_player_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("web_scraper.urls")),
    path('api/get_team_stats/', get_team_stats, name='get_team_stats'),
    path("api/get_all_teams_stats/", get_all_teams_stats, name="get_all_teams_stats"),
    path("api/player_suggestions/", player_suggestions, name="player_suggestions"),
    path("api/team_suggestions/", team_suggestions, name="team_suggestions"),
    path("api/update_player_data/", update_player_data, name="update_player_data"),
    path("api/update_team_data/", update_team_data, name="update_team_data"),
    path("api/delete_player_data/", delete_player_data, name="delete_player_data"),
]
