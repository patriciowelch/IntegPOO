from datetime import datetime

class Log():
    def __init__(self, nombre):
        self.path = "servidor/anexo/Logs"
        self.nombre = nombre
        ## Crea un archivo de log con el nombre especificado, en caso de que ya exista lo borra y empesar a escribirlo desde 0
        try:
            with open(f"{self.path}\\{self.nombre}.txt", "x") as f:
                f.write(f"Log creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")
            f.close()
        except FileExistsError:
            #Si el archivo ya existe, lo abre y comienza a escribir desde el comienzo
            with open(f"{self.path}\\{self.nombre}.txt", "w") as f:
                f.write(f"Log creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")
            f.close()
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def agregarLinea(self, linea, tipo, usuario = "", ip = "", gerarquiaUsuario = ""):
        ## Agrega una linea al log con el siguiente formato "Fecha Hora Tipo: linea"
        try:
            with open(f"{self.path}\\{self.nombre}.txt", "a") as f:
                log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S') } {tipo}"
                if ip != "":
                    log += f" IP: {ip}"
                if usuario != "":
                    log += f" USER: {usuario} "
                if gerarquiaUsuario != "":
                    log += f" ROL: {gerarquiaUsuario} "
                log += f": {linea}\n"
                f.write(log)
            f.close()
            return linea
        except Exception as e:
            print(f"Error inesperado: {e}")
            return linea
        
    def leerLog(self,ultimasLineas):
        ## Lee las ultimas lineas del log
        try:
            with open(f"{self.path}\\{self.nombre}.txt", "r") as f:
                lineas = f.readlines()
                f.close()
            if ultimasLineas > len(lineas):
                return lineas #Si se pide mas lineas de las que hay, devuelve todas
            else:
                return lineas[-ultimasLineas:]
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

