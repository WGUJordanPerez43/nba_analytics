from django.shortcuts import render
from django.http import JsonResponse
import json
from .scraper import PlayerScraper, TeamScraper
from .models import PlayerStats, TeamStats
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def get_nba_stats(request):
    player_name = request.GET.get('player_name', None)
    season = request.GET.get('season', None)

    response_data = {}

    if player_name:
        player_scraper = PlayerScraper()
        player_stats = player_scraper.get_stats(player_name)
        
        if "error" in player_stats:
            response_data['error'] = player_stats["error"]
        else:
            for stat in player_stats:
                if season and season not in stat['season']:
                    continue
                
                PlayerStats.objects.update_or_create(
                    player_name=player_name,
                    season=stat['season'],
                    defaults=stat
                )

            response_data['player_stats'] = player_stats
    
    return JsonResponse(response_data)

def get_team_stats(request):
    team_name = request.GET.get('team_name', '').strip()
    season = request.GET.get('season', None)

    if not team_name:
        return JsonResponse({"error": "missing team_name parameter"}, status=400)
    if season:
        team_stats = TeamStats.objects.filter(team_name__iexact=team_name, season=season).values()
    else:
        team_stats = TeamStats.objects.filter(team_name__iexact=team_name).values()

    if not team_stats:
        return JsonResponse({"error": f"no data found for {team_name}"}, status=404)

    return JsonResponse(list(team_stats), safe=False)

def get_all_teams_stats(request):
    current_year = datetime.now().year
    recent_seasons = [str(current_year - i) for i in range(5)]

    scraper = TeamScraper()
    for season in recent_seasons:
        scraper.get_all_teams_stats(season)

    teams_data = list(TeamStats.objects.filter(season__in=recent_seasons).values())
    return JsonResponse(teams_data, safe=False)

def player_suggestions(request):
    query = request.GET.get("query", "").strip()
    
    if not query:
        return JsonResponse({"suggestions": []})

    matching_players = (
        PlayerStats.objects
        .filter(player_name__icontains=query)
        .values_list("player_name", flat=True)
        .distinct()
    )

    return JsonResponse({"suggestions": list(matching_players)})

def team_suggestions(request):
    query = request.GET.get("query", "").strip()
    
    if not query:
        return JsonResponse({"suggestions": []})

    matching_teams = (
        TeamStats.objects
        .filter(team_name__icontains=query)
        .values_list("team_name", flat=True)
        .distinct()
    )

    return JsonResponse({"suggestions": list(matching_teams)})

@csrf_exempt
def update_player_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "invalid request"}, status=405)

    try:
        data = json.loads(request.body)
        player_name = data.get("player_name", "").strip()

        if not player_name:
            return JsonResponse({"error": "player name required"}, status=400)

        scraper = PlayerScraper()
        scraped_stats = scraper.get_stats(player_name)

        if "error" in scraped_stats:
            return JsonResponse({"error": scraped_stats["error"]}, status=404)

        updated_stats = []
        for stat in scraped_stats:
            obj, created = PlayerStats.objects.update_or_create(
                player_name=player_name,
                season=stat['season'],
                defaults=stat
            )
            if not created:
                updated_stats.append(stat)

        return JsonResponse({"updated_stats": updated_stats})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_team_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        team_name = data.get("team_name", "").strip()

        if not team_name:
            return JsonResponse({"error": "team_name required"}, status=400)

        scraper = TeamScraper()
        all_stats = scraper.get_all_teams_stats(season=datetime.now().year)
        updated_stats = []

        for stat in all_stats:
            if stat['team_name'].lower() == team_name.lower():
                updated_stats.append(stat)

        return JsonResponse({"updated_stats": updated_stats})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def delete_player_data(request):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        player_name = data.get("player_name", "").strip()

        if not player_name:
            return JsonResponse({"error": "player_name required"}, status=400)

        deleted_count, _ = PlayerStats.objects.filter(player_name__iexact=player_name).delete()

        return JsonResponse({"deleted_records": deleted_count})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

