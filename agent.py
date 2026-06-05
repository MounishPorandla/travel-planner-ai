import os
from groq import Groq
from dotenv import load_dotenv
from knowledge_base import build_knowledge_base, search_destinations
from tools import get_weather, estimate_budget, get_best_time_to_visit

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("Building knowledge base....")
index, destinations = build_knowledge_base()
print("Knowledg base ready.")

def plan_trip(user_request: str) -> str:
    """ 
    Main function - take user request and return complete travel plan
    """

    client = Groq(api_key=GROQ_API_KEY)

    extraction_response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role": "system",
                "content": """ Extract travel details from user request.
                Return ONLY a JSON object with these fields: 
                { 
                    "destination": "city_name",
                    "duration_days": "number",
                    "budget_style": "budget or comfort or luxury",
                    "month": "month name"
                
                }
                If not mentioned, use sensible defaults."""
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )

    #Parse the extracted details
    import json
    try:
        details_text = extraction_response.choices[0].message.content
        #Clean us response in case LLM adds extra text
        details_text = details_text.strip()
        if "'''" in details_text:
            details_text = details_text.split("'''")[1]
            if details_text.startswith("json"):
                details_text = details_text[4:]
        details = json.loads(details_text)
    except:
        details = {
            "destination": "Goa",
            "duration_days": 3,
            "budget_style": "budget",
            "month": "December"
        }

    destination = details.get("destination", "Goa")
    duration = details.get("duration_days", 3)
    style = details.get("budget_style", "budget")

    #step2 - search knowledge base for destination info
    print(f"Searching knowledge base for {destination}...")
    relevant_info = search_destinations(
        f"travel information about {destination}", index, destinations, k = 2
    )
    knowledge_context = "\n".join(relevant_info)

    #step 3 - call tools to get live data
    print("Fetching weather...")
    weather = get_weather.invoke(destination)

    print("Estimating budget...")
    budget = estimate_budget.invoke({
        "destination": destination, "duration_days": duration, "travel_style": style
    })

    print("Getting best time to visit...")
    timing = get_best_time_to_visit.invoke(destination)

    #step 4 - generate final itenerary with all context
    print("generating itenerary...")

    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """ You are an expert indian travel planner.
                create detailed, practical, exciting travel iteneraries. Use the provided information to give accurate, grounded advice. Format the itenerary clearly with day by day breakdown.
                Be specific about places, food, activities and costs. """
            
            },
            {
                "role": "user",
                "content": f"""
                Plan a {duration} day trip to {destination}.

                DESTINATION KNOWLEDGE:
                {knowledge_context}


                WEATHER INFORMATION:
                {weather}
                
                BUDEGT ESTIMATE:
                {budget}

                TIMING ADVICE:
                {timing}

                USER REQUEST:
                {user_request}

                Create a complete day by day itinerary with morning, afternoon and evening activities.
                Include food recommendations, travel tips, and budget breakdown.
                """
        }


        ]
    )
    return final_response.choices[0].message.content