from cmd import Cmd
from servidor import Servidor
import subprocess
from tarea import Tarea
from robot import Robot
from log import Log

class cli(Cmd):
    doc_header = 'Comandos documentados (help <comando>):'

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = 'Bienvenido'
        self.servidorRpc = None
        self.guardar_comandos = False
        self.robot = Robot()
        self.tarea = None
        self.modorobot = 'MAN'
        self.log = Log("LogServer")

    def precmd(self, linea):
        linea = linea.lower()
        return linea
    
    def onecmd(self, linea, retorno = False):
        try:
            if not retorno:
                self.log.agregarLinea("Comando Ingresado Local: "+linea,"INFO")
            resultado = super().onecmd(linea)
            if resultado is not None:
                if self.guardar_comandos and self.tarea is not None and not resultado.startswith("$"):
                    resultado = resultado.upper()
                    ultimalinea = self.tarea.agregarLinea(resultado)
                    if retorno:
                        return "Comando guardado %s" % ultimalinea
                    else:
                        print("Comando guardado %s" % ultimalinea)
                        self.log.agregarLinea("Comando Guardado: "+ultimalinea,"INFO")
                else:
                    if retorno:
                        return resultado
                    else:
                        print(resultado)
                        self.log.agregarLinea("Resultado: "+resultado,"INFO")
                    
        except Exception as e:
            if retorno:
                return str(e)
            else:
                print(e)
                self.log.agregarLinea(str(e),"ERROR")
        except SystemExit:
            print("Saliendo...")
            self.log.agregarLinea("Saliendo...","INFO")
            raise SystemExit
            
    def do_servidor(self,args):
        """
Inicia el servidor
   Sintaxis: servidor [comando]
        comando:
            - on [adminpassword]       Inicia el servidor
            - off [adminpassword]       Detiene el servidor
        """
        args = args.split()
        if len(args) == 2:
            if args[1] == "balhou":
                if args[0] == "on":
                    if self.servidorRpc is None:
                        self.servidorRpc = Servidor(self)
                        return "Servidor iniciado"
                elif args[0] == "off":
                    if self.servidorRpc is not None:
                        self.servidorRpc.detener()
                        self.servidorRpc = None
                        return "Servidor detenido"
                else:
                    raise Exception("Error: Argumento Invalido")
            else:
                raise Exception("Error: Contraseña de administrador incorrecta")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
    """
    def estadoservidor(self, mensaje):
        print("")
        print(mensaje)
        #volver a mostrar el prompt
        print(self.prompt, end='', flush=True)
    """

    def do_clc(self,args):
        """
Limpia la consola
        """
        subprocess.call('cls', shell = True)

    def do_quit(self, args):
        """
Salir del programa
        """
        self.do_clc("")
        self.do_servidor("off balhou")
        self.robot.desconectar()
        raise SystemExit

    def do_robot(self, args):
        """
Comando para el robot
    Sintaxis: robot [comando]
        comando:
            - conectar           Inicializa la conexion el robot al puerto serie
            - desconectar        Desconecta el robot del puesto serie actual
            - motores_on         Enciende los motores del robot
            - motores_off        Apaga los motores del robot
            - estado             Muestra el estado actual del robot
            - puerto [puerto] [adminpassword]   Cambia el puerto del robot |solo localmente|
            - baudrate [baudrate] [adminpassword]   Cambia el baudrate del robot |solo localmente|
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "conectar":
                return self.robot.conectar()
            elif args[0] == "desconectar":
                return self.robot.desconectar()
            elif args[0] == "motores_on":
                return self.robot.activar_motor()
            elif args[0] == "motores_off":
                return self.robot.desactivar_motor()
            elif args[0] == "estado":
                return self.robot.estadoActual()
            else:
                raise Exception("Error: Argumento Invalido")
        elif len(args) == 3 and args[0] in ["puerto","baudrate"]:
            if args[2] == "balhou":
                if args[0] == "puerto":
                    return self.robot.cambiar_puerto(args[1])
                elif args[0] == "baudrate":
                    return self.robot.cambiar_baudrate(args[1])
            else:
                raise Exception("Error: Contraseña de administrador incorrecta")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")

    def do_home(self, args):
        """
Realiza el movimiento home del efector final.
lleva a todas las articulaciones a la posición de origen.
        """
        args = args.split()
        if len(args) == 0:
            return self.robot.enviar_comando('G28')
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
            

    def do_movlin(self, args):
        """
Realiza el movimiento lineal del efector final.
    movlin <X> <Y> <Z> [V]
        Decimales con '.' (punto)
        X    Posicion final en eje x en mm.
        Y    Posición final en eje y en mm.
        Z    Posición final en eje z en mm.
        V    Velocidad del movimiento en mm/s.
        """
        args = args.split()
        if len(args) == 3:
            comando = "G1 X%s Y%s Z%s F%s" % (str(args[0]), str(args[1]), str(args[2]), self.robot._velMax)
            return self.robot.enviar_comando(comando)
        elif len(args) == 4:
            comando = "G1 X%s Y%s Z%s F%s" % (str(args[0]), str(args[1]), str(args[2]), str(args[3]))
            return self.robot.enviar_comando(comando)
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")

    def do_efectorfinal(self, args):
        """
Controla el efector final del robot.
    Sintaxis: efectorfinal [comando]
        comando:
            - abrir     Abre el efector final
            - cerrar    Cierra el efector final
 """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abrir":
                return self.robot.efector_final('abrir')
            elif args[0] == "cerrar":
                print("Cerrando efector final")
                return self.robot.efector_final('cerrar')
            else:
                raise Exception("Error: Argumento Invalido")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
        
    def do_cargartarea(self, args):
        """
Carga un archivo de tarea previamente guardado.
    Sintaxis: cargartarea [nombre]
        -nombre: nombre del archivo de tarea a cargar
        """
        args = args.split()
        if len(args) == 1:
            self.tarea = Tarea(args[0])
            return "Tarea %s cargada" % args[0]
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
        
    def do_ejecutartarea(self, args):
        """
Inicializa la ejecucion de la tarea cargada 
        """
        args = args.split()
        if len(args) == 0:
            if self.tarea is not None and self.robot.serial is not None:
                linea = self.tarea.proximaLinea()
                while linea != "EOF":
                    #si la linea inicia con ; es un comentario y no se envia
                    if not linea.startswith(";"):
                        resultado = self.robot.enviar_comando(linea)
                        print(resultado)
                    linea = self.tarea.proximaLinea()
                return "Tarea ejecutada"
            else:
                if self.tarea is None:
                    raise Exception("Error: No hay ninguna tarea cargada")
                elif self.robot.serial is None:
                    raise Exception("Error: El puerto serie no esta conectado")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")

    def do_modo(self, args):
        """
Cambia el modo de trabajo del robot entre absoluto y relativo.
    Sintaxis: modo [comando]
        comando:
            - abs    Cambia el modo de trabajo a absoluto
            - rel    Cambia el modo de trabajo a relativo
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abs":
                return self.robot.enviar_comando('G90')
            elif args[0] == "rel":
                return self.robot.enviar_comando('G91')
            else:
                raise Exception("Error: Argumento Invalido")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")

    def do_guardarcmd(self, args):
        """
Inicia o detiene el guardado de comandos
    guardarcmd [nombre] : inicia el guardado de comandos en el archivo de tarea de nombre "nombre"
    guardarcmd : detiene el guardado de comandos

    ATENCION: Si se inicia el guardado de comandos, todos los comandos ingresados se guardaran en el archivo de tarea especificado hasta que se detenga el guardado mediante guardarcmd.
        """
        args = args.split()
        if len(args)==0 or len(args)==1:
            if args == []:
                self.guardar_comandos = False
                self.tarea = None
                return "Guardado de comandos desactivado"
            elif args[0] != "":
                if not self.guardar_comandos:
                    self.guardar_comandos = True
                    self.tarea = Tarea(args[0])
                    return "$Guardado de comandos activado en %s" % self.tarea._nombre
            else:
                raise Exception("Error: Comando invalido inesperado")
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
            
    def do_usuarios(self, args):
        """
Muestra los usuarios conectados al servidor o agrega un nuevo usuario
    Sintaxis: usuarios [comando]
        comando:
            - listar                               Muestra los usuarios validos
            - agregar [nombre] [contraseña]        Agrega un nuevo usuario bajo el nombre y contraseña especificados
        """
        args = args.split()
        if self.servidorRpc is not None:
            if args[0] == "listar" and len(args)==1:
                print("Listando usuarios")
                for usuario in self.servidorRpc.clientes.clientes:
                    print(usuario)
            elif args[0] == "agregar" and len(args)==3:
                return self.servidorRpc.clientes.agregar_cliente(args[1], args[2])
            else:
                if args[0] in ["listar","agregar"]:
                    raise Exception("Error: Cantidad de Argumentos Incorrecta")
                else:
                    raise Exception("Error: Argumento Invalido")
        else:
            raise Exception("Error: El servidor no esta iniciado")
        
    def do_log(self, args):
        """
Muestra el log del servidor con las conexiones, los usuarios y los comandos ejecutados por ellos
    Sintaxis: log [Lineas]
        Lineas: mostrar ultimas "Lineas" lineas del log
        """
        args = args.split()
        if len(args) == 1:
            return self.log.leerLog(args[0])
        else:
            raise Exception("Error: Cantidad de Argumentos Incorrecta")
            
    
    def default(self, linea):
        if self.guardar_comandos:
            return linea
        else:
            raise Exception("Error: Comando no reconocido")
    

if __name__ == '__main__':
    try:
        cli = cli()
        cli.cmdloop()
        raise SystemExit
    except KeyboardInterrupt:
        print('Saliendo disconforme...')
        exit(0)
    except SystemExit:
        print('Saliendo conforme....')