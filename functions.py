import requests
import os
import json

def set_current_memory():
    print("setting memory")

def get_current_weather(latitude,longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,wind_speed_10m&timezone=auto"
    response = requests.get(url)
    current = response.json()['current']
    json_res = {"Temperature": current['temperature_2m'],"Precipitation":current['precipitation'],"Wind Speed":current['wind_speed_10m']}
    return json_res

weatherTool = {
    "name": "get_current_weather",
    "description": "Get the info and current weather in a given latitude and longitude",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
              "type": "number",
              "description": "The latitude of a place",
            },
            "longitude": {
              "type": "number",
              "description": "The longitude of a place",
            },
            "Comment": {
              "type": "string",
              "description": "A line of comment to show function is in process",
            }
          },
          "required": ["latitude", "longitude","Comment"],
        },
      }