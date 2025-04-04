import unittest
from unittest.mock import patch, MagicMock
from web_scraper.scraper import PlayerScraper, TeamScraper

class TestPlayerScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = PlayerScraper()

    def test_get_stats_invalid_name(self):
        result = self.scraper.get_stats("LeBr0n")
        self.assertEqual(result, {"error": "Bad player name format"})

class TestTeamScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = TeamScraper()

    @patch("web_scraper.scraper.requests.get")
    def test_get_all_teams_stats_no_table(self, mock_get):

        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        result = self.scraper.get_all_teams_stats("2025")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
