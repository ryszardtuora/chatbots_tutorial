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


# QA
import numpy
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
emb = numpy.load("emb.npy")
questions, answers = [], []
with open("QA.json") as f:
  qa_data = json.load(f)

for q,a in qa_data:
  questions.append(q)
  answers.append(a)

class ActionQA(Action):
  def name(self):
    return "answer_qa"
    
  def run(self, dispatcher, tracker, domain):
    question = tracker.latest_message["text"]
    ques_vec = model.encode(question)
    distances = [cosine(ques_vec, r) for r in emb]
    top_3 = sorted(distances)[:3]
    indices = [distances.index(d) for d in top_3]
    chosen = [(questions[i], answers[i]) for i in indices]
    message = "\n\n".join([f"{q}\n\t{a}" for q,a in chosen])
    dispatcher.utter_message(text=message)
    return []
