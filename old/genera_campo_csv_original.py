
import csv
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import islice

from openai import OpenAI
import traceback

# Asegúrate de reemplazar 'tu_clave_api' con tu clave de API real, obtenida desde OpenAI.

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
csv.field_size_limit(500000)


def generate_description_description(data):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=API_KEY
    )
    prompt = (
        f"Por favor, escribe una descripción de 300 palabras de este fdgaffdf basado en los siguientes datos: "
        f"Nombre sitio: {data['Nombrecampo1']}, "
        f"Autonomía: {data['Autonomia']}, "
        f"Provincia: {data['Provincia']}, "
        f"Domicilio: {data['Domicilio']}, "
        f"Pon el prompt que quieras!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


def process_batch(batch):
    return [generate_description_description(row) for row in batch]


def process_row(input_row, existing_keys, fieldnames_output):
    if input_row[fieldnames_output[0]] not in existing_keys:
        return generate_description_description(input_row)
    else:
        return None


def process_csv_in_parallel(input_file_path, output_file_path, max_workers=20, batch_size=20):
    output_vacio = False
    try:
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            with open(output_file, mode='r', encoding='utf-8') as csv_output_file:
                csv_reader_output = csv.reader(csv_output_file)
                existing_first_fields = [row[0] for row in csv_reader_output]
        else:
            existing_first_fields = list()
            output_vacio=True
        with open(input_file_path, mode='r', encoding='utf-8') as csv_input_file:
            csv_reader = csv.DictReader(csv_input_file)
            headers_output = csv_reader.fieldnames + ['Descripcion']

            batches = [list(batch) for batch in iter(lambda: list(islice(csv_reader, batch_size)), [])]

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for batch in batches:
                    futures = [executor.submit(process_row, row, existing_first_fields, headers_output) for row in batch]

                    with open(output_file_path, mode='a', newline='', encoding='utf-8') as csv_output_file:
                        csv_writer = csv.DictWriter(csv_output_file, fieldnames=headers_output)
                        if output_vacio:
                            csv_writer.writeheader()
                        for row, future in zip(batch, futures):
                            result = future.result()
                            if result is not None:
                                row['Descripcion'] = result
                                csv_writer.writerow(row)
                                print(row['Codigo'])

    except Exception as e:
        print(f"Se produjo un error al procesar el archivo: {e}")
        traceback.print_exc()


input_file_path = 'inputs/archivo_de_entrada.csv'
output_file_path = 'outputs/archivo_de_salida.csv'
process_csv_in_parallel(input_file_path, output_file_path)