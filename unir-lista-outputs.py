# Unimos los archivos de la carpeta temp

import os

def unir_archivos_output():
    try:
        if os.path.exists("output"):
            print("Uniendo archivos temporales ...")
            with open("resultados-prompts.csv", "w", encoding="utf-8") as file_w:
                # header
                file_w.write("Id,prompt,result,status\n")
                for file in os.listdir("output"):
                    with open(os.path.join("output", file), "r", encoding="utf-8") as file_r:
                        file_w.write(file_r.read())
            print("Archivos unidos en resultados-prompts.csv")
    except Exception as e:
        print(f"Error: {e}")
        exit()

unir_archivos_output()