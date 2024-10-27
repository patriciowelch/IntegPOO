import serial

class Robot():
    def __init__(self, puerto, baudrate=115200, timeout=1,velMax=100):
        self._puerto = puerto
        self._baudrate = baudrate
        self._timeout = timeout
        self._velMax = velMax
        self.serial = None
        pass

    def conectar(self):
        try:
            self.serial = serial.Serial(self._puerto, self._baudrate, timeout=self._timeout)
            self.serial.readline().decode().strip()
            mensaje = ""
            while True:
                info = self.serial.readline().decode().strip()
                if info != "":
                    mensaje += info
                else :
                    break
            return mensaje
        
        except serial.SerialException as e:
            # Error específico de conexión serial
            print(f"No se pudo conectar al puerto {self._puerto}: {e}")
            return f"Error: No se pudo conectar al puerto {self._puerto}."

        except Exception as e:
            # Cualquier otro error no previsto
            print(f"Ocurrió un error inesperado: {e}")
            return f"Error inesperado: {e}"
        
    
    def desconectar(self):
        try:
            self.serial.close()
            return "Desconectado"
        except serial.SerialException as e:
            print(f"No se pudo desconectar del puerto {self._puerto}: {e}")
            return f"Error: No se pudo desconectar del puerto {self._puerto}."
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return f"Error inesperado: {e}"

    def efector_final(self, arg):
        if arg == 'abrir':
            return (self.enviar_comando('M5'))
        elif arg == 'cerrar':
            return (self.enviar_comando('M3'))
            
        
    def enviar_comando(self, comando):
        try:
            comando += '\r'
            self.serial.write(comando.encode())
        
        except serial.SerialException as e:
            print(f"Error al enviar comando: {e}")
            return f"Error al enviar comando: {e}"
        except Exception as e:
            print(f"Error inesperado al enviar comando: {e}")
            return f"Error inesperado al enviar comando: {e}"

        try:
            mensaje = ""
            while True:
                info = self.serial.readline()
                print(info)
                info = info.decode().strip()
                if info != "":
                    mensaje += info
                else :
                    break
            return mensaje
        except serial.SerialException as e:
            print(f"Error al recibir respuesta: {e}")
            return f"Error al recibir respuesta: {e}"
        except Exception as e:
            print(f"Error inesperado al recibir respuesta: {e}")
            return f"Error inesperado al recibir respuesta: {e}"

    def cambiar_puerto(self, puerto):
        self._puerto = puerto
        if self.serial is not None:
            self.serial.port = puerto
            return f"Puerto cambiado a {puerto}"
        else:
            return ("El puerto no pudo ser Cambiado")

    def __del__(self):
        self.serial.close()


##BORRAR ESTO AL TERMINAR CON ROBOT
if __name__ == '__main__':
    try:
        robot = Robot('COM3')
        print(robot.conectar())
        print(robot.efector_final('abrir'))
        print(robot.efector_final('cerrar'))
        print(robot.enviar_comando('M114'))
        
        raise SystemExit
    except KeyboardInterrupt:
        print('Saliendo disconforme...')
        exit(0)
    except SystemExit:
        print('Saliendo conforme....')