# tools.py
# Job: Define tools that the LangChain agent can call autonomously

import requests
import os
from langchain.tools import tool

# ============================================
# TOOL 1 — WEATHER CHECKER
# ============================================

@tool
def get_weather(location: str) -> str:
    """
    Get current weather and forecast for a travel destination.
    Use this when user asks about weather or best time to visit.
    Input should be city name like 'Goa' or 'Manali'
    """
    
    # We're using wttr.in — completely free, no API key needed
    url = f"https://wttr.in/{location}?format=3"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"Weather in {location}: {response.text}"
        else:
            return f"Could not fetch weather for {location}"
    except Exception as e:
        return f"Weather service unavailable: {str(e)}"

# ============================================
# TOOL 2 — BUDGET ESTIMATOR
# ============================================

@tool
def estimate_budget(destination: str, duration_days: int, travel_style: str) -> str:
    """
    Estimate travel budget for a trip.
    Use this when user mentions budget or asks how much a trip costs.
    Input: destination name, number of days, travel style (budget/comfort/luxury)
    """
    
    # Budget ranges per day in rupees (accommodation + food + activities)
    budget_data = {
        "goa": {"budget": 2000, "comfort": 4000, "luxury": 8000},
        "manali": {"budget": 2500, "comfort": 4500, "luxury": 9000},
        "kerala": {"budget": 3000, "comfort": 5000, "luxury": 10000},
        "rajasthan": {"budget": 2500, "comfort": 5000, "luxury": 12000},
        "andaman": {"budget": 4000, "comfort": 7000, "luxury": 15000},
    }
    
    # Travel costs from Hyderabad (one way flight approximate)
    travel_costs = {
        "goa": 4000,
        "manali": 6000,
        "kerala": 3500,
        "rajasthan": 5000,
        "andaman": 8000,
    }
    
    dest_lower = destination.lower()
    style_lower = travel_style.lower()
    
    if dest_lower not in budget_data:
        return f"Budget data not available for {destination}"
    
    if style_lower not in ["budget", "comfort", "luxury"]:
        style_lower = "budget"
    
    daily_cost = budget_data[dest_lower][style_lower]
    travel_cost = travel_costs[dest_lower]
    
    total = (daily_cost * duration_days) + (travel_cost * 2)
    
    return f"""
Budget Estimate for {destination} ({duration_days} days, {travel_style} style):
- Daily expenses: ₹{daily_cost}/day × {duration_days} days = ₹{daily_cost * duration_days}
- Return travel from Hyderabad: ₹{travel_cost * 2}
- TOTAL ESTIMATED BUDGET: ₹{total}
- Per person approximate cost including all expenses
"""

# ============================================
# TOOL 3 — DESTINATION INFO
# ============================================

@tool
def get_best_time_to_visit(destination: str) -> str:
    """
    Get the best time to visit a destination and what to expect.
    Use this when user asks when to visit or about seasons.
    Input should be destination name.
    """
    
    timing_data = {
        "goa": "Best time: November to February. Avoid June-September monsoon. December is peak season with perfect beach weather.",
        "manali": "Best time: October to June for sightseeing. December to February for snow activities. Avoid July-September for landslides.",
        "kerala": "Best time: September to March. Avoid June-August peak monsoon. December is ideal for backwaters.",
        "rajasthan": "Best time: October to March. Avoid April-June extreme heat. December has cold nights but warm days perfect for sightseeing.",
        "andaman": "Best time: October to May. Avoid June-September rough seas. December has crystal clear waters perfect for diving.",
    }
    
    dest_lower = destination.lower()
    
    if dest_lower in timing_data:
        return timing_data[dest_lower]
    else:
        return f"Timing information not available for {destination}"