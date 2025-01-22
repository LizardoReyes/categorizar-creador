import math
import os

def get_prompts(index):
    # verificar que existe archivo de prompts
    try:
        with open("lista-prompts.txt", "r", encoding="utf-8") as file:

            lines = file.readlines()
            numberLines = len(lines)
            interval = math.ceil(numberLines / 5)

            print(f"Archivo de prompts encontrado: {numberLines} lineas")
            print(f"Intervalos de: {interval}")

            # Verificamos si existe el carpeta temp
            if not os.path.exists("temp"):
                os.makedirs("temp")

            # Verificamos que la carpeta temp tiene archivos
            if len(os.listdir("temp")) <= 0:
                # Dividir el archivo en 5 partes por el intervalo
                print("Dividiendo archivo de prompts en 5 partes ...")
                for i in range(5):
                    with open(os.path.join("temp", f"lista-prompts-{i + 1}.txt"), "w", encoding="utf-8") as file_w:
                        file_w.writelines(lines[interval * i:interval * (i + 1)])
            else:
                print("Archivos de prompts ya existen ...")

            prompts = [
                (1, os.path.join("temp", "lista-prompts-1.txt"), os.path.join("output", "resultados-prompts-1.csv")),
                (1 + interval, os.path.join("temp", "lista-prompts-2.txt"), os.path.join("output", "resultados-prompts-2.csv")),
                (1 + 2 * interval, os.path.join("temp", "lista-prompts-3.txt"), os.path.join("output", "resultados-prompts-3.csv")),
                (1 + 3 * interval, os.path.join("temp", "lista-prompts-4.txt"), os.path.join("output", "resultados-prompts-4.csv")),
                (1 + 4 * interval, os.path.join("temp", "lista-prompts-5.txt"), os.path.join("output", "resultados-prompts-5.csv"))
            ]

            return prompts[index - 1]

    except FileNotFoundError:
        print("Archivo de prompts no encontrado ...")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()