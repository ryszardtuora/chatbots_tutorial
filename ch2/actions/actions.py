# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

  

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import json


# API
import requests

api_address = "https://corona.lmao.ninja/v2/countries/Poland?yesterday=true&strict=true&query"

class ActionAPI(Action):
  def name(self):
    return "action_api"
    
  def run(self, dispatcher, tracker, domain):
    response = requests.get(api_address)
    data = json.loads(response.content)
    message = f"Yesterday {data['todayCases']} people got sick, and {data['todayDeaths']}\
 people died because of the coronavirus pandemic."
    dispatcher.utter_message(text=message)
    return []
