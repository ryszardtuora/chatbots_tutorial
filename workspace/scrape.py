import requests
import json
import numpy
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

address = "https://www.cdc.gov/coronavirus/2019-ncov/faq.html"
page = requests.get(address)

soup = BeautifulSoup(page.content, "html.parser")

elements = soup.findAll("div", id=lambda el: el is not None and el.endswith("-question"))

questions = [el.find("span").text for el in elements]
answers = [el.find("div", class_="card-body").text for el in elements]

qa = [(q, a) for q,a in zip(questions, answers)]

with open("QA.json", "w") as f:
    json.dump(qa, f, indent=2)


model = SentenceTransformer("distiluse-base-multilingual-cased-v2")

emb = model.encode(questions)
emb.save("emb.npy", vec)

cos = lambda a,b: numpy.dot(a,b)/(numpy.sqrt(numpy.dot(a,a)) * numpy.sqrt(numpy.dot(b,b)))
