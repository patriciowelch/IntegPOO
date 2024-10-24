from cmd import Cmd
from servidor import Servidor
import subprocess

class cli(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = 'Bienvenido'
        self.servidorRpc = None
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
    def estadoServidor(self, mensaje):
        print(mensaje)
    def do_clc(self,args):
        """
Limpia la consola
        """
        subprocess.call('cls', shell = True)
    def do_agregarUsuario(self, args):
        """
Agrega un usuario
        """
        args = args.split(" ")
        print("Agregando usuario: %s" % args[0])
    def do_quit(self, args):
        """
Salir del programa
        """
        self.do_clc("")
        self.do_servidor("off")
        return True
    def do_robot(self, args):
        """
Comando para el robot
    (robot) [comando]
    comando:
        - conectar
        - desconectar
        - activar_motores
        - desactivar_motores
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "conectar":
                print("Conectando...")
            elif args[0] == "desconectar":
                print("Desconectando...")
            elif args[0] == "activar_motores":
                print("Activando motores...")
            elif args[0] == "desactivar_motores":
                print("Desactivando motores...")
            else:
                print("Error 1")
        else:
            print("Error 2")
    

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