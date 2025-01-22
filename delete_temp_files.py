import os


def delete_temp_files():
    try:
        if os.path.exists("temp"):
            print("Eliminando archivos temporales ...")
            for file in os.listdir("temp"):
                os.remove(os.path.join("temp", file))
            os.rmdir("temp")
    except Exception as e:
        print(f"Error: {e}")
        exit()

delete_temp_files()