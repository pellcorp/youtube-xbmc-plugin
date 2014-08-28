import BaseTestCase
import nose
import sys
import io
from mock import Mock, patch
from  YouTubeScraper import YouTubeScraper 


class TestYouTubePurchasesScraper(BaseTestCase.BaseTestCase): 
    def test_scrapePurchases_correctly(self):
        import CommonFunctions
        sys.modules["__main__"].common = CommonFunctions
        
        self.scraper = YouTubeScraper()
        self.scraper.createUrl = Mock()
        self.scraper.createUrl.return_value = "some_url"
        
        result = {}
        
        result["content"] = io.open("./resources/purchases.html").read()
        result["status"] = "200"
        
        sys.modules["__main__"].core._fetchPage.return_value = result
        
        playlists = self.scraper.scrapeUserPurchases({"scraper": "purchases"})[0]
        
        assert(playlists[0]["Title"] == "Angels & Demons")
        assert(playlists[0]["videoid"] == "xGqzck1dtYM")
        assert(playlists[0]["thumbnail"] == "http://i.ytimg.com/vi/xGqzck1dtYM/movieposter.jpg")
        
        assert(playlists[1]["playlist"] == "ELueUibNZhl8o")
        assert(playlists[1]["Title"] == "Game of Thrones: Season 4")
        assert(playlists[1]["user_feed"] == "playlist")
        assert(playlists[1]["thumbnail"] == "http://i.ytimg.com/sh/UBWMnSm4n5A/showposter_thumb.jpg?v=52f12e4a")
    
if __name__ == "__main__":
    nose.runmodule()
