from cmd import Cmd
from servidor import Servidor
import subprocess
#from tarea import Tarea
from robot import Robot

class cli(Cmd):

    doc_header = 'Comandos documentados (help <comando>):'

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = 'Bienvenido'
        self.servidorRpc = None
        self.guardar_comandos = False
        self.robot = Robot('COM3')

    def precmd(self, linea):
        linea = linea.lower()
        return linea
    
    def onecmd(self, linea):
        try: 
            resultado = super().onecmd(linea)
            if resultado is not None:
                print(resultado)
                if self.guardar_comandos:
                    print("Comando guardado")
        except Exception as e:
            print(e)
        except SystemExit:
            print("Saliendo...")
            raise SystemExit
            
    def do_servidor(self,args):
        """
Inicia el servidor
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "on":
                if self.servidorRpc is None:
                    self.servidorRpc = Servidor(self)
            elif args[0] == "off":
                if self.servidorRpc is not None:
                    self.servidorRpc.detener()
                    self.servidorRpc = None
                    return "Servidor detenido"
            else:
                return "Error 1"
        else:
            return "Error 2"

    def estadoservidor(self, mensaje):
        print("")
        print(mensaje)
        #volver a mostrar el prompt
        print(self.prompt, end='', flush=True)

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
        self.do_servidor("off")
        raise SystemExit

    def do_robot(self, args):
        """
Comando para el robot
    (robot) [comando]
    comando:
        - conectar
        - desconectar
        - activar_motores
        - desactivar_motores
        - puerto [puerto]
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
            else:
                return "Error 1"
        elif len(args) == 2 and args[0] in ["puerto"]:
            return self.robot.cambiar_puerto(args[1])
        else:
            return "Error 2"

    def do_home(self, args):
        """
Realiza el movimiento home del efector final.
        """
        args = args.split()
        if len(args) == 0:
            return self.robot.enviar_comando('G28')
        else:
            return "Error 1"
            

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
            comando = "G1 X%s Y%s Z%s F%s" % (args[0], args[1], args[2], self.robot._velMax)
            return self.robot.enviar_comando(comando)
        elif len(args) == 4:
            comando = "G1 X%s Y%s Z%s F%s" % (args[0], args[1], args[2], args[3])
            return self.robot.enviar_comando(comando)
        else:
            return "Error 1"

    def do_efectorfinal(self, args):
        """
Controla el efector final del robot.
    efectorfinal [abrir|cerrar]
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abrir":
                return self.robot.efector_final('abrir')
            elif args[0] == "cerrar":
                print("Cerrando efector final")
                return self.robot.efector_final('cerrar')
            else:
                return "Error 1"
                
        else:
            return "Error 2"

    def do_modo(self, args):
        """
Cambia el modo de trabajo del robot entre absoluto y relativo.
    modo [abs|rel]
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abs":
                return self.robot.enviar_comando('G90')
            elif args[0] == "rel":
                return self.robot.enviar_comando('G91')
            else:
                return "Error 1"
        else:
            return "Error 2"

    def do_guardarcmd(self, args):
        """
Inicia o detiene el guardado de comandos
        """
        if self.guardar_comandos:
            self.guardar_comandos = False
            return "Guardado de comandos desactivado"
        else:
            self.guardar_comandos = True
            return "Guardado de comandos activado"
    
    def do_usuarios(self, args):
        """
Muestra los usuarios
        """
        args = args.split()
        if args[0] == "listar":
            print("Listando usuarios")
        elif args[0] == "agregar":
            if len(args) == 3:
                return self.servidorRpc.clientes.agregar_cliente(args[1], args[2])
            else:
                return "Error 1"
    

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