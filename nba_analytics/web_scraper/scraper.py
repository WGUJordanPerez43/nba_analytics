import requests
from bs4 import BeautifulSoup
from .models import PlayerStats, TeamStats

class BaseScraper:
    def __init__(self, base_url):
        self._base_url = base_url

    def _get_soup(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        return None

#scrape the player data
class PlayerScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.basketball-reference.com/players/")

    def get_stats(self, player_name):
        parts = player_name.split(" ")
        if len(parts) != 2:
            return {"error": "Bad player name format"}

        first_name, last_name = parts
        first_name_lower = first_name.lower()
        last_name_lower = last_name.lower()

        url = f"{self._base_url}{last_name_lower[0]}/{last_name_lower[:5]}{first_name_lower[:2]}01.html"

        soup = self._get_soup(url)
        if not soup:
            return {"error": "FAILED to retrieve data"}

        stats_table = soup.find("table", {"id": "per_game_stats"})
        if not stats_table:
            return {"error": "No stats table found for player"}

        rows = stats_table.find("tbody").find_all("tr")

        player_stats = []
        season_counter = 0
        for row in reversed(rows):
            season_text = row.find("th").text.strip()
            if season_text and "career" not in season_text.lower():
                columns = row.find_all("td")

                if season_counter >= 5:
                    break


                column_data = {
                    "season": season_text,
                    "games_played": columns[4].text,
                    "points_per_game": columns[28].text,
                    "assists_per_game": columns[23].text,
                    "rebounds_per_game": columns[22].text,
                }
                player_stats.append(column_data)
                season_counter += 1

        if not player_stats:
            return {"error": f"No data found for player {player_name}"}

        return player_stats






#scrape the team data
class TeamScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.basketball-reference.com/leagues/")

    def get_all_teams_stats(self, season):
        recent_seasons = [str(int(season) - i) for i in range(5)]
        all_teams_data = []

        for season in recent_seasons:
            if TeamStats.objects.filter(season=season).exists():
                continue

            url = f"{self._base_url}NBA_{season}.html"
            soup = self._get_soup(url)
            if not soup:
                continue
            stats_table = soup.find("div", {"id": "div_per_game-team"})
            if not stats_table:
                continue

            rows = stats_table.find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if columns:
                    team_data = {
                        "team_name": columns[0].text.strip(),
                        "season": season,
                        "games_played": int(columns[1].text),
                        "points_per_game": float(columns[23].text),
                        "assists_per_game": float(columns[18].text),
                        "rebounds_per_game": float(columns[17].text),
                    }

                    #clean the team_name by removing '*' character if there is playoff data
                    team_data["team_name"] = team_data["team_name"].replace("*", "")
                    all_teams_data.append(team_data)

                    
                    TeamStats.objects.update_or_create(
                        team_name=team_data["team_name"],
                        season=team_data["season"],
                        defaults=team_data
                    )

        return all_teams_data
