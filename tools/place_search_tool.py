import os
from utils.place_info_search import TavilyPlaceSearchTool, GooglePlaceSearchTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        if not self.google_api_key:
            raise ValueError("GPLACES_API_KEY environment variable is not set.")
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_serach_tool_list = self._setup_tools()
        
    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        
        @tool
        def search_attractions(place: str) -> str:
            """Search all tool for the place tool"""
            
            try:
                attraction_result = self.google_places_search.google_search_attractions(place)
                if attraction_result:
                    return f"Following are the attractions of {place} as suggestted by Google: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.search_attractions(place)
                return f"Google cannot find details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"
            return f"No attractions found for {place}."
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search all tool for the place tool"""
            
            try:
                restaurant_result = self.google_places_search.google_search_restaurants(place)
                if restaurant_result:
                    return f"Following are the restaurants of {place} as suggestted by Google: {restaurant_result}"
            except Exception as e:
                tavily_result = self.tavily_search.search_restaurants(place)
                return f"Google cannot find details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"
            return f"No restaurants found for {place}."
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activities_result = self.google_places_search.google_search_activity(place)
                if activities_result:
                    return f"Following are the activities in and around {place} as suggested by google: {activities_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"
            return f"No activities found for {place}."
            
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transportation_result = self.google_places_search.google_search_transportation(place)
                if transportation_result:
                    return f"Following are the modes of transportation available in {place} as suggested by google: {transportation_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"
            return f"No transportation information found for {place}."
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]