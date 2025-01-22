######
#
#   Script para categorizar contenidos gracias a la API OpenAI | TeamPlatino.com
#
#   Creado por https://twitter.com/shanejones
#   Editado por https://twitter.com/chuisochuisez y Darorck
#   Actualizado por @lizardoreyes_ el 24/10/2024
#   Recuerda cambiar los ************ por tu API Key de OpenAI
#
######

import os
import openai
import csv
import time
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

keywordsFile = open("old/lista-keywords.txt", "r", encoding='utf-8')

print("Categorizando títulos...")

counter = 0
for post in keywordsFile:
    f = open("titulos-clickbait.csv", "a", newline='', encoding='utf-8')
    writer = csv.writer(f)

    counter = counter + 1

    prompt = "Indica la palabra clave de este título: \"" + post + "\".  Devuelve solo la palaba clave."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=110,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[","]
    )

    output = [post, response["choices"][0]["message"]["content"].strip().title()]

    writer.writerow(output)

    print(str(counter) + " títulos categorizados.")

    # lets not spam the API too much
    time.sleep(0.35)

    f.close()

    # Finalmente continua en:
    # https://docs.google.com/spreadsheets/d/18P5rFfirEcgcKLCs6_H5CpPNPiDX_gNJNSz1EWkx3mw/edit#gid=0
