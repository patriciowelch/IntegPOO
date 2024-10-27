from serial import Serial, SerialException

class Robot():
    def __init__(self, puerto, baudrate=115200, timeout=1, VLMAXIMA=100, DIMENSIONES=[0, 0, 0]):
        self.dimensiones = DIMENSIONES
        self.vel_lineal_maxima = VLMAXIMA
        self._puerto = puerto
        self._baudrate = baudrate
        self._timeout = timeout
        self.serial = None
        pass

    def conectar(self):
        try:
            self.serial = Serial(self._puerto, self._baudrate, timeout=self._timeout)
            self.serial.readline().decode('utf-8').strip()
            mensaje = ""
            while True:
                info = self.serial.readline().decode('utf-8').strip()
                if info != "":
                    mensaje += info
                else :
                    break
            return mensaje
        
        except SerialException as e:
            # Error específico de conexión serial
            print(f"No se pudo conectar al puerto {self._puerto}: {e}")
            return f"Error: No se pudo conectar al puerto {self._puerto}."

        except Exception as e:
            # Cualquier otro error no previsto
            print(f"Ocurrió un error inesperado: {e}")
            return f"Error inesperado: {e}"
        
    
    def desconectar(self):
        self.serial.close()
        pass
    def efector_final(self, arg):
        pass
    def enviar_comando(self, comando):
        pass
    def __del__(self):
        self.serial.close()


##BORRAR ESTO AL TERMINAR CON ROBOT
if __name__ == '__main__':
    try:
        robot = Robot('COM5')
        print(robot.conectar())
        raise SystemExit
    except KeyboardInterrupt:
        print('Saliendo disconforme...')
        exit(0)
    except SystemExit:
        print('Saliendo conforme....')