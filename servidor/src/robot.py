import serial
from log import Log

class Robot():
    def __init__(self, puerto, baudrate=115200, timeout=1,velMax=100):
        self._puerto = puerto
        self._baudrate = baudrate
        self._timeout = timeout
        self._velMax = velMax
        self.serial = None
        self.motor = False
        self.log = Log("Log_Robot")
        pass

    def addToLog (self, mensaje):
        # Si la primera palabra del mensaje es "Error", se agrega al log como error, eliminando la palabra ERROR, si no es un error se agrega como info
        # Si el ultimo caracter es un salto de linea, se elimina solo el ultimo caracter
        if mensaje[-1] == '\n':
            mensaje = mensaje[:-1]
        if mensaje[-1] == '\r':
            mensaje = mensaje[:-1]
        if mensaje.split()[0] == "Error:": 
            mensaje = mensaje.replace("Error: ","")
            self.log.agregarLinea(mensaje, "ERROR")
        elif mensaje.split()[0] == "INFO:":
            mensaje = mensaje.replace("INFO: ","")
            self.log.agregarLinea(mensaje, "INFO MENSAJE DEVUELTO")
        else:
            self.log.agregarLinea(mensaje, "INFO")

        


    def conectar(self):
        try:
            self.addToLog(f"Conectando al puerto {self._puerto}...")
            self.serial = serial.Serial(self._puerto, self._baudrate, timeout=self._timeout)
            self.serial.readline().decode().strip()
            mensaje = ""
            while True:
                info = self.serial.readline().decode().strip()
                if info != "":
                    self.addToLog(info)
                    mensaje += info+'\n'
                else :
                    break
            return mensaje
        
        except serial.SerialException as e:
            # Error específico de conexión serial
            print(f"No se pudo conectar al puerto {self._puerto}: {e}")
            self.addToLog(f"Error: No se pudo conectar al puerto {self._puerto}.")
            return f"Error: No se pudo conectar al puerto {self._puerto}."

        except Exception as e:
            # Cualquier otro error no previsto
            print(f"Ocurrió un error inesperado: {e}")
            self.addToLog(f"Error inesperado: {e}")
            return f"Error inesperado: {e}"
        
    
    def desconectar(self):
        if self.serial is None:
            return "No hay conexión serial abierta"
        else:
            self.addToLog(f"Desconectando del puerto {self._puerto}...")
            try:
                self.serial.close()
                self.serial = None
                self.addToLog(f"Desconectado del puerto {self._puerto}.")
                return "Desconectado"
            except serial.SerialException as e:
                print(f"No se pudo desconectar del puerto {self._puerto}: {e}")
                self.addToLog(f"Error: No se pudo desconectar del puerto {self._puerto}.")
                return f"Error: No se pudo desconectar del puerto {self._puerto}."
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                self.addToLog(f"Error inesperado: {e}")
                return f"Error inesperado: {e}"

    def efector_final(self, arg):
        if arg == 'abrir':
            return (self.enviar_comando('M5'))
        elif arg == 'cerrar':
            return (self.enviar_comando('M3'))
            
        
    def enviar_comando(self, comando):
        if self.serial is None:
            raise Exception("Error: El puerto serie no esta conectado")
        else:
            self.addToLog(f"Enviando comando: {comando}")
            try:
                comando += '\r'
                self.serial.write(comando.encode())
                self.addToLog(f"Comando enviado: {comando}")
            
            except serial.SerialException as e:
                print(f"Error al enviar comando: {e}")
                self.addToLog(f"Error al enviar comando: {e}")
                return f"Error al enviar comando: {e}"
            except Exception as e:
                print(f"Error inesperado al enviar comando: {e}")
                self.addToLog(f"Error inesperado al enviar comando: {e}")
                return f"Error inesperado al enviar comando: {e}"

            try:
                mensaje = ""
                while True:
                    info = self.serial.readline().decode().strip()
                    if info != "":
                        self.addToLog(info)
                        mensaje += info+'\n'
                    else :
                        break
                return mensaje
            except serial.SerialException as e:
                print(f"Error al recibir respuesta: {e}")
                self.addToLog(f"Error al recibir respuesta: {e}")
                return f"Error al recibir respuesta: {e}"
            except Exception as e:
                print(f"Error inesperado al recibir respuesta: {e}")
                self.addToLog(f"Error inesperado al recibir respuesta: {e}")
                return f"Error inesperado al recibir respuesta: {e}"

    def cambiar_puerto(self, puerto):
            if self.serial is None:
                self._puerto = puerto
                self.addToLog(f"Puerto cambiado a {puerto}")
                return f"Puerto cambiado a {puerto}"
            else:
                return "No se puede cambiar el puerto con la conexión abierta"

    def desactivar_motor(self):
        if self.serial is None:
            return "No hay conexión serial abierta"
        else:
            self.motor = False
            return ("INFO: Motores Desactivados" + self.enviar_comando('M18'))

    def activar_motor(self):
        if self.serial is None:
            return "No hay conexión serial abierta"
        else:
            self.motor = True
            return ("INFO: Motores Activados" + self.enviar_comando('M17'))
        
    def estadoActual(self):
        estado = "INFO: Estado actual del robot: "
        if self.serial is None:
            estado += "Puerto = NA "
            estado += "Baudrate = NA "
            estado += "Timeout = NA "
            estado += "Motores = NA "
            estado += "Posición actual = NA "
            estado += "Velocidad máxima = NA "
        else:
            self.addToLog("Solicitando estado actual del robot...")
            estado += f"Puerto = {self._puerto} "
            estado += f"Baudrate = {self._baudrate} "
            estado += f"Timeout = {self._timeout} "
            estado += f"Motores = {self.motor} "
            posactual=self.enviar_comando('M114')
            posactual = posactual.replace("INFO:","")
            estado += f"Posición actual = {posactual} "
            estado += f"Velocidad máxima = {self._velMax} "
            self.addToLog("Estado actual del robot solicitado.")
            self.addToLog(estado)
        return estado
