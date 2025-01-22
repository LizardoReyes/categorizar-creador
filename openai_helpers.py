import csv

import openai
import re
import time

openai.api_key = "XXXXXXXXXXXXX"

def create_content(counter, prompt_file_name, output_file_name):
    print("Leyendo prompts...")

    prompts = open(prompt_file_name, "r", encoding='utf-8')

    for prompt in prompts:

        prompt = prompt.strip()  # Eliminar espacios y saltos de línea innecesarios

        # Si no hay texto en el prompt, continuar con el siguiente
        if not prompt:
            continue

        try:
            print(f"Procesando prompt #{counter}: {prompt}")

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            responsePrompt: str = response["choices"][0]["message"]["content"].strip().title()

            # Limpiar salida
            cleaned_text = re.sub(r'```Html.*?', '', responsePrompt, flags=re.DOTALL)
            cleaned_text = re.sub(r'```', '', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'<H1>.*?</H1>', '', cleaned_text, flags=re.DOTALL)

            # detectar los <P><B> y cambiarlos por <p><B>
            cleaned_text = re.sub(r'<P>', '<p>', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'</P>', '</p>', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'<B>', '<b>', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'</B>', '</b>', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'<!Doctype Html>', '', cleaned_text, flags=re.DOTALL)

            # detectar <Html\s+Lang="[^"]*">\s*<Head>\s*(<Meta\s+[^>]+>\s*)*<Title>[^<]+</Title>\s*</Head>\s*<Body>
            cleaned_text = re.sub(r'<Html\s+Lang="[^"]*">\s*<Head>\s*(<Meta\s+[^>]+>\s*)*<Title>[^<]+</Title>\s*</Head>\s*<Body>', '', cleaned_text, flags=re.DOTALL)

            cleaned_text = cleaned_text.strip()
            status = "Success"

        except Exception as e:
            cleaned_text = str(e)
            status = "Error"
            print(f"Error procesando el prompt #{counter}: {e}")

        # Guardar en el archivo CSV
        with open(output_file_name, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            output = [counter, prompt, cleaned_text, status]
            writer.writerow(output)

        # Evitar sobrecargar la API
        time.sleep(0.1)

        # Incrementar contador
        counter += 1

    print("Procesamiento completado.")