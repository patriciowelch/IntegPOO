
class Tarea():
    def __init__(self,nombre):
        self._nombre = nombre
        self._path = "servidor\anexo\Task_Files"
        self._ultimaLineaLeida = 0
        ##Crea archivo con nombre de la tarea en el path fijo (servidor\anexo\Task_Files)
        try:
            with open(f"{self._path}\{self._nombre}.txt", "x") as f:
                f.write("Tarea creada")
            f.close()
        except FileExistsError:
            print(f"Abriendo Archivo {self._nombre} existente")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
        pass

    def proximaLinea(self):
        try:
            with open(f"{self._path}\{self._nombre}.txt", "r") as f:
                lineas = f.readlines()
                if self._ultimaLineaLeida < len(lineas):
                    self._ultimaLineaLeida += 1
                    return lineas[self._ultimaLineaLeida-1]
                else:
                    return "EOF"
            f.close()
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
    
    def agregarLinea(self, linea, numeroLinea):
        try:
            with open(f"{self._path}\{self._nombre}.txt", "r") as f:
                lineas = f.readlines()
                f.close()
            with open(f"{self._path}\{self._nombre}.txt", "w") as f:
                if numeroLinea < len(lineas):
                    lineas.insert(numeroLinea, linea)
                else:
                    lineas.append(linea)
                f.writelines(lineas)
            f.close()
            self._ultimaLineaLeida = numeroLinea
            return self._ultimaLineaLeida
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
    
    def borrarLinea(self, numeroLinea):
        try:
            with open(f"{self._path}\{self._nombre}.txt", "r") as f:
                lineas = f.readlines()
                f.close()
            with open(f"{self._path}\{self._nombre}.txt", "w") as f:
                if numeroLinea < len(lineas):
                    lineas.pop(numeroLinea)
                else:
                    return "EOF"
                f.writelines(lineas)
            f.close()
            self._ultimaLineaLeida = numeroLinea
            return self._ultimaLineaLeida
        
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None