from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
from clientes import Clientes, Cliente

class Handler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        server.ip_cliente=client_address[0]
        super().__init__(request, client_address, server)

class Servidor(SimpleXMLRPCServer):
    def __init__(self, consola, puertoRPC = 8000, addr = None, requestHandler= Handler,
                     logRequests=False, allow_none=False, encoding=None,
                     bind_and_activate=True, use_builtin_types=False):
        self.consola = consola
        self.puerto = puertoRPC
        self.idActual = ''
        self.ipCliente = None
        self.clientes = Clientes()
        self.clientes.cargar_clientes()
        self.tokensvalidos = []

        addr = ('127.0.0.1', self.puerto)

        try:
            super().__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate,
                             use_builtin_types)
            
        except socket.error as e:
            print(e)

        #aca se agregan los metodos que son accesibles al cliente
        self.register_function(self._iniciar_sesion, 'iniciar_sesion')
        self.register_function(self._robot, 'robot')
        self.register_function(self._listarMetodos, 'listarMetodos')
        self.register_function(self._guardar_cmd, 'guardarcmd')
        self.register_function(self._defguardar, ':')
        self.register_function(self._help, 'help')

        self.hiloRPC = Thread(target = self.correrServidor, daemon = True)
        self.hiloRPC.start()
        
        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address))

    def detener(self):
        super().shutdown()
        super().server_close()
        self.hiloRPC.join()
    
    def correrServidor(self):
        self.serve_forever()

    #aca va la ejecucion de los metodos que puede ejecutar el cliente
    def _iniciar_sesion(self, usuario, clave):
        if self.clientes.validar_cliente(usuario, clave):
            token = self.clientes.generar_token()
            self.tokensvalidos.append(token)
            return token
        else:
            return "Error 401: Usuario o clave incorrectos"
        
    def _robot(self, token, args):
        pass

    def _guardar_cmd(self, token, *a):
        args = list(a)
        if token in self.tokensvalidos:
            if len(args) == 1:
                return self.consola.do_guardarcmd(args[0])+"\nPara guardar un comando escriba ': [comando]' con espacio"
            elif len(args) == 0:
                return self.consola.do_guardarcmd("")
        else:
            return "Error 401: Token invalido"
        
    def _defguardar(self, token, *args):
        comando = " ".join(args)
        if token in self.tokensvalidos:
            return self.consola.onecmd(comando, True)
        else:
            return "Error 401: Token invalido"
        
    def _help(self, token, *args):
        if token in self.tokensvalidos:
            if args[0] == "guardarcmd":
                return (self.consola.do_guardarcmd.__doc__)
            elif args[0] == "robot":
                return self.consola.do_robot.__doc__
            elif args[0] == "listarMetodos":
                return "Lista los metodos disponibles en el servidor"
            elif args[0] == ":":
                return "Guarda el comando ingresado si se encuentra en modo guardado de comandos\n\t: [comando]"
                
        
    def _listarMetodos(self):
        resultado = list(super().system_listMethods())
        return resultado