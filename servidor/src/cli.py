from cmd import Cmd

class cli(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro = 'Bienvenido'
    def do_iniciar_servidor(self,args):
        """
    Inicia el servidor
        """
        pass
    def do_quit(self,args):
        return True
    

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