import csv
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from openai import OpenAI
import traceback

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
csv.field_size_limit(500000)


def generate_description(data):
    """Genera una descripción basada en los datos de entrada usando OpenAI."""
    client = OpenAI(api_key=API_KEY)
    prompt = (
        f"Escribe una descripción de 300 palabras basada en los datos: "
        f"Nombre sitio: {data['Nombrecampo1']}, "
        f"Autonomía: {data['Autonomia']}, "
        f"Provincia: {data['Provincia']}, "
        f"Domicilio: {data['Domicilio']}.")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


def process_row(row, existing_keys):
    """Procesa una fila del CSV. Si no existe ya en el output, genera su descripción."""
    if row['Id'] not in existing_keys:
        row['Description'] = generate_description(row)
        return row
    return None


def process_csv(input_path, output_path, max_workers=20, batch_size=20):
    """Lee un CSV, procesa filas en paralelo y escribe el resultado en otro CSV."""
    try:
        # Verificar si el archivo de salida ya existe y leer las claves existentes.
        existing_keys = []
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            with open(output_path, 'r', encoding='utf-8') as output_file:
                existing_keys = [row[0] for row in csv.reader(output_file)]

        # Leer el archivo de entrada en lotes.
        with open(input_path, 'r', encoding='utf-8') as input_file:
            csv_reader = csv.DictReader(input_file)
            headers = csv_reader.fieldnames + ['Description']
            batches = [list(batch) for batch in iter(lambda: list(islice(csv_reader, batch_size)), [])]

        # Procesar cada lote en paralelo.
        with ThreadPoolExecutor(max_workers=max_workers) as executor, \
                open(output_path, 'a', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=headers)

            # Escribir encabezados si el archivo está vacío.
            if not existing_keys:
                csv_writer.writeheader()

            for batch in batches:
                futures = [executor.submit(process_row, row, existing_keys) for row in batch]
                for row, future in zip(batch, futures):
                    result = future.result()
                    if result:
                        csv_writer.writerow(result)
                        print(f"Procesado: {result['Id']}")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        traceback.print_exc()


# Rutas de archivos de entrada y salida.
input_path = 'inputs/input_file.csv'
output_path = 'outputs/output_file.csv'
process_csv(input_path, output_path)