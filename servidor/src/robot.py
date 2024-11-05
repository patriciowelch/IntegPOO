import serial
from log import Log
import json
import sounddevice as sd
import numpy as np
import threading

class Robot():
    def __init__(self, timeout=1,velMax=100):
        self.path = "servidor/anexo/serialConfig.json"
        with open(self.path) as file:
            data = json.load(file)
            self._puerto = data["puerto"]
            self._baudrate = data["baudrate"]
        self._timeout = timeout
        self._velMax = velMax
        self.serial = None
        self.motor = False
        self.sound_thread = None
        self.log = Log("Log_Robot")
        pass

    def addToLog (self, mensaje):
        # Si la primera palabra del mensaje es "Error", se agrega al log como error, eliminando la palabra ERROR, si no es un error se agrega como info
        # Si el ultimo caracter es un salto de linea, se elimina solo el ultimo caracter
        if mensaje.split()[0] == "ERROR:":
            mensaje = mensaje.replace("ERROR: ","")
            self.log.agregarLinea(mensaje, "ERROR")
        elif mensaje.split()[0] == "INFO:":
            mensaje = mensaje.replace("INFO: ","")
            self.log.agregarLinea(mensaje, "INFO MENSAJE DEVUELTO")
        else:
            self.log.agregarLinea(mensaje, "INFO")

        


    def conectar(self):
        try:
            if self.serial is None:
                self.addToLog(f"Conectando al puerto {self._puerto}...")
                self.serial = serial.Serial(self._puerto, self._baudrate, timeout=self._timeout)
                self.sonido("conectar")
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
            else:
                return "Ya hay una conexión serial abierta"
        
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
                self.sonido("desconectar")
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
        
    def sonido_no_bloqueante(self, sound):
        waves=[]
        for i in range(sound[3]):
            t= np.linspace(0,sound[0],int(sound[2]*sound[0]))
            wave = sound[0]*np.sin(2*np.pi*sound[1]*t)
            waves.append(wave)
            pause = np.zeros(int(sound[2] * sound[4]))
            waves.append(pause)
        full_wave = np.concatenate(waves)
        sd.play(full_wave,samplerate=sound[2])
        sd.wait()
            
    def sonido(self, arg):
        if arg == 'conectar':
            sound = [0.2,1318.51,44100,2,0.05]
        elif arg == 'desconectar':
            sound = [0.40,1046.5,44100,1,0]
        elif arg == 'Error':
            sound = [0.8,1975.53,44100,1,0.07]
        elif arg == 'comando':
            sound = [0.4,587.33,44100,3,0.07]
        self.sound_thread = threading.Thread(target=self.sonido_no_bloqueante, args=(sound,))
        self.sound_thread.start()
        
        
    def enviar_comando(self, comando):
        if self.serial is None:
            self.sonido("Error")
            raise Exception("Error: El puerto serie no esta conectado")
        else:
            self.addToLog(f"Enviando comando: {comando}")
            try:
                comando += '\r'
                self.serial.write(comando.encode())
                self.sonido("comando")
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
                        if "error" in info.lower():
                            self.sonido("Error")
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
            #abrir archivo en lectura y escritura para modificar el puerto
            with open(self.path, "r+") as file:
                data = json.load(file)
                data["puerto"] = puerto
                file.seek(0)
                json.dump(data, file, indent=4)
            self.addToLog(f"Puerto cambiado a {puerto}")
            return f"Puerto cambiado a {puerto}"
        else:
            return "No se puede cambiar el puerto con la conexión abierta"
    
    def cambiar_baudrate(self, baudrate):
        if self.serial is None:
            self._baudrate = baudrate
            #abrir archivo en lectura y escritura para modificar el baudrate
            with open(self.path, "r+") as file:
                data = json.load(file)
                data["baudrate"] = baudrate
                file.seek(0)
                json.dump(data, file, indent=4)
            self.addToLog(f"Baudrate cambiado a {baudrate}")
            return f"Baudrate cambiado a {baudrate}"
        else:
            return "No se puede cambiar el baudrate con la conexión abierta"

    def desactivar_motor(self):
        if self.serial is None:
            self.sonido("Error")
            return "No hay conexión serial abierta"
        else:
            self.motor = False
            return ("INFO: Motores Desactivados" + self.enviar_comando('M18'))

    def activar_motor(self):
        if self.serial is None:
            self.sonido("Error")
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
