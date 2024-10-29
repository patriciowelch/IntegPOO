import datetime

class Log():
    def __init__(self, nombre):
        self.path = "servidor\anexo\Logs"
        self.nombre = nombre
        try:
            with open(f"{self.path}\{self.nombre}.txt", "x") as f:
                f.write("Log creado")
            f.close()
        except FileExistsError:
            print(f"Abriendo Archivo LOG {self.nombre} existente")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
        pass

    def agregarLinea(self, linea, tipo):
        ## Agrega una linea al log con el siguiente formato "Fecha Hora Tipo: linea"
        try:
            with open(f"{self.path}\{self.nombre}.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {tipo}: {linea}\n")
            f.close()
            return True
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False

