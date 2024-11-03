from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
from log import Log
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
        self.log = Log("LogServer")

        addr = ('127.0.0.1', self.puerto)

        try:
            super().__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate,
                             use_builtin_types)
            
        except socket.error as e:
            print(e)

        #aca se agregan los metodos que son accesibles al cliente
        self.register_function(self._iniciar_sesion, 'iniciar_sesion')
        self.register_function(self._listarMetodos, 'listarMetodos')
        self.register_function(self._guardar_cmd, 'guardarcmd')
        self.register_function(self._robot, 'robot')
        self.register_function(self._movlin, 'movlin')
        self.register_function(self._modo, 'modo')
        self.register_function(self._ejecutartarea, 'ejecutartarea')
        self.register_function(self._cargartarea, 'cargartarea')
        self.register_function(self._efectorfinal, 'efectorfinal')
        self.register_function(self._home, 'home')
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
        self.log.agregarLinea(f"Usuario: {usuario} intenta iniciar sesion","INFO")
        if self.clientes.validar_cliente(usuario, clave):
            self.log.agregarLinea(f"Sesion de {usuario} iniciada con exito","INFO")
            token = self.clientes.generar_token()
            self.tokensvalidos.append(token)
            return token
        else:
            return self.log.agregarLinea("Error 401: Usuario o clave incorrectos","ERROR")

    def _guardar_cmd(self, token, *a):
        args = list(a)
        if token in self.tokensvalidos:
            if len(args) == 1:
                return self.consola.do_guardarcmd(args[0])+"\nPara guardar un comando escriba ': [comando]' con espacio"
            elif len(args) == 0:
                return self.consola.do_guardarcmd("")
            else:
                return "Error Cantidad de Argumentos Inválido"
        else:
            return "Error 401: Token invalido"
        
    def _defguardar(self, token, *args):
        comando = " ".join(args)
        if token in self.tokensvalidos:
            return self.consola.onecmd(comando, True)
        else:
            return "Error 401: Token invalido"
        
    def _robot(self, token, *args):
        if token in self.tokensvalidos:
            if(len(args)==1):
                return self.consola.do_robot(args[0])
            else:
                return "Error Cantidad de Argumentos Inválido"
        else:
            return "Error 401: Token invalido"

    def _help(self, token, *args):
        if token in self.tokensvalidos:
            if len(args)==1:
                if args[0] == "guardarcmd":
                    return self.consola.do_guardarcmd.__doc__
                elif args[0] == "robot":
                    return self.consola.do_robot.__doc__
                elif args[0] == "listarMetodos":
                    return "Lista los metodos disponibles en el servidor"
                elif args[0] == ":":
                    return "Guarda el comando ingresado si se encuentra en modo guardado de comandos\n\t: [comando]"
                elif args[0] == "home":
                    return self.consola.do_home.__doc__
                elif args[0] == "movlin":
                    return self.consola.do_movlin.__doc__
                elif args[0] == "modo":
                    return self.consola.do_modo.__doc__
                elif args[0] == "ejecutartarea":
                    return self.consola.do_ejecutartarea.__doc__
                elif args[0] == "cargartarea":
                    return self.consola.do_cargartarea.__doc__
                elif args[0] == "efectorfinal":
                    return self.consola.do_efectorfinal.__doc__
                else:
                    return "Error No existe comando identificable"
            else:
                return "Error Cantidad de Argumentos Inválido"
        else:
            return "Error 401: Token invalido"
        
    def _home(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 0:
                return self.consola.do_home()
        else:
            return "Error 401: Token inválido"
        
        
    def _listarMetodos(self, token, *args):
        if token in self.tokensvalidos:
            if len(args)==0:
                resultado = list(super().system_listMethods())
                return resultado
            else:
                return "Error Cantidad de Argumentos Inválido"
        else:
            return "Error 401: Token inválido"
        
    def _movlin(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 3:
                return self.consola.do_movlin(f"{args[0]} {args[1]} {args[2]}")
            elif len(args) == 4:
                return self.consola.do_movlin(f"{args[0]} {args[1]} {args[2]} {args[3]}")
            else:
                return "Error: Cantidad de argumentos inválido"
        else:
            return "Error 401: Token inválido"

    def _modo(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                return self.consola.do_modo(args[0])
            else:
                return "Error: Cantidad de argumentos inválido"
        else:
            return "Error 401: Token inválido"

    def _ejecutartarea(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 0:
                return self.consola.do_ejecutartarea("")
            else:
                return "Error: Cantidad de argumentos inválido"
        else:
            return "Error 401: Token inválido"

    def _cargartarea(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                return self.consola.do_cargartarea(args[0])
            else:
                return "Error: Cantidad de argumentos inválido"
        else:
            return "Error 401: Token inválido"

    def _efectorfinal(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                return self.consola.do_efectorfinal(args[0])
            else:
                return "Error: Cantidad de argumentos inválido"
        else:
            return "Error 401: Token inválido"