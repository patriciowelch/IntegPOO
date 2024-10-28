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
                    print("Servidor Apagado")
                    self.servidorRpc = None
            else:
                print("Error 1")
        else:
            print("Error 2")

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
                print("Conectando...")
                print(self.robot.conectar())
            elif args[0] == "desconectar":
                print("Desconectando...")
                print(self.robot.desconectar())
            elif args[0] == "motores_on":
                print("Activando motores...")
                print(self.robot.activar_motor())
            elif args[0] == "motores_off":
                print("Desactivando motores...")
                print(self.robot.desactivar_motor())
            else:
                print("Error 1")
        elif len(args) == 2 and args[0] in ["puerto"]:
            print("Cambiando %s a %s" % (args[0], args[1]))
            self.robot.cambiar_puerto(args[1])
        else:
            print("Error 2")

    def do_home(self, args):
        """
Realiza el movimiento home del efector final.
        """
        args = args.split()
        if len(args) == 0:
            print("Realizando movimiento home")
            resultado = self.robot.enviar_comando('G28')
        else:
            print("Error 1")
            return
        print(resultado)

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
            resultado = self.robot.enviar_comando(comando)
        elif len(args) == 4:
            comando = "G1 X%s Y%s Z%s F%s" % (args[0], args[1], args[2], args[3])
            resultado = self.robot.enviar_comando(comando)
        else:
            print("Error 1")
            return
        print(resultado)

    def do_efectorfinal(self, args):
        """
Controla el efector final del robot.
    efectorfinal [abrir|cerrar]
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abrir":
                print("Abriendo efector final")
                resultado = self.robot.efector_final('abrir')
            elif args[0] == "cerrar":
                print("Cerrando efector final")
                resultado = self.robot.efector_final('cerrar')
            else:
                print("Error 1")
                return
        else:
            print("Error 2")
            return
        print(resultado)

    def do_modo(self, args):
        """
Cambia el modo de trabajo del robot entre absoluto y relativo.
    modo [abs|rel]
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "abs":
                print("Cambiando a modo absoluto")
                resultado = self.robot.enviar_comando('G90')
            elif args[0] == "rel":
                print("Cambiando a modo relativo")
                resultado = self.robot.enviar_comando('G91')
            else:
                print("Error 1")
                return
        else:
            print("Error 2")
            return
        print(resultado)

    def do_guardarcmd(self, args):
        """
Inicia o detiene el guardado de comandos
        """
        if self.guardar_comandos:
            self.guardar_comandos = False
            print("Guardado de comandos desactivado")
        else:
            self.guardar_comandos = True
            print("Guardado de comandos activado")
    
    def do_usuarios(self, args):
        """
Muestra los usuarios
        """
        args = args.split()
        if args[0] == "listar":
            print("Listando usuarios")
        elif args[0] == "agregar":
            if len(args) == 3:
                print("Agregando usuario %s" % args[1])
                print(self.servidorRpc.clientes.agregar_cliente(args[1], args[2]))
            else:
                print("Error 1")
        

    def default(self, line):
        if self.guardar_comandos:
            print("Comando guardado, %s" % line)
        else:
            print("Comando no reconocido: %s" % line)
    

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