from serial import Serial

class Robot():
    def __init__(self, puerto, baudrate=115200, timeout=1, VLMAXIMA=100, DIMENSIONES=[0, 0, 0]):
        self.dimensiones = DIMENSIONES
        self.vel_lineal_maxima = VLMAXIMA
        self._puerto = puerto
        self._baudrate = baudrate
        self._timeout = timeout
        self.serial = None
        self.conectar()
        pass
    def conectar(self):
        self.serial = Serial(self._puerto, self._baudrate, timeout=self._timeout)
        self.serial.readline().decode('utf-8').strip()
        while True:
            info=self.serial.readline().decode('utf-8').strip()
            if info == "":
                break
            #Luego no hay que imprimirlo, solo es para saber que se esta recibiendo
            print(info)
        pass
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
        raise SystemExit
    except KeyboardInterrupt:
        print('Saliendo disconforme...')
        exit(0)
    except SystemExit:
        print('Saliendo conforme....')