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

        addr = ('127.0.0.1', self.puerto)

        try:
            super().__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate,
                             use_builtin_types)
            
        except socket.error as e:
            print(self.log.agregarLinea(e,"ERROR"))

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
        
        print(self.log.agregarLinea("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address),"INFO"))


    def detener(self):
        super().shutdown()
        super().server_close()
        self.hiloRPC.join()
        self.log.agregarLinea("Servidor detenido","INFO")
    
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
            return self.log.agregarLinea("Usuario o contraseña invalidos","ERROR 401")

    def _guardar_cmd(self, token, *a):
        args = list(a)
        if token in self.tokensvalidos:
            if len(args) == 1:
                self.log.agregarLinea(f"Usuario solicita guardar comando en el archivo {args[0]}","INFO")
                return self.log.agregarLinea(self.consola.do_guardarcmd(args[0])+"\nPara guardar un comando escriba ': [comando]' con espacio", "INFO")
            elif len(args) == 0:
                self.log.agregarLinea("Usuario solicita desactivar guardado de comando","INFO")
                return self.log.agregarLinea(self.consola.do_guardarcmd(""), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR GUARDARCMD")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _defguardar(self, token, *args):
        comando = " ".join(args)
        if token in self.tokensvalidos:
            return self.consola.onecmd(comando, True)
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _robot(self, token, *args):
        if token in self.tokensvalidos:
            if(len(args)==1):
                self.log.agregarLinea(f"Usuario solicita enviar el comando '{args[0]}' al robot","INFO")
                return self.log.agregarLinea(self.consola.do_robot(args[0]), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR ROBOT")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _help(self, token, *args):
        if token in self.tokensvalidos:
            if len(args)==1:
                if args[0] == "guardarcmd":
                    self.log.agregarLinea("El usuario solicita informacion de 'guardarcmd'", "INFO")
                    return self.log.agregarLinea(self.consola.do_guardarcmd.__doc__, "INFO")
                elif args[0] == "robot":
                    self.log.agregarLinea("El usuario solicita informacion de 'robot'", "INFO")
                    return self.log.agregarLinea(self.consola.do_robot.__doc__, "INFO")
                elif args[0] == "listarMetodos":
                    self.log.agregarLinea("El usuario solicita informacion de 'listarMetodos'", "INFO")
                    return self.log.agregarLinea("Lista los metodos disponibles en el servidor", "INFO")
                elif args[0] == ":":
                    self.log.agregarLinea("El usuario solicita informacion de ':'", "INFO")
                    return self.log.agregarLinea("Guarda el comando ingresado si se encuentra en modo guardado de comandos\n\t: [comando]", "INFO")
                elif args[0] == "home":
                    self.log.agregarLinea("El usuario solicita informacion de 'home'", "INFO")
                    return self.log.agregarLinea(self.consola.do_home.__doc__, "INFO")
                elif args[0] == "movlin":
                    self.log.agregarLinea("El usuario solicita informacion de 'movlin'", "INFO")
                    return self.log.agregarLinea(self.consola.do_movlin.__doc__, "INFO")
                elif args[0] == "modo":
                    self.log.agregarLinea("El usuario solicita informacion de 'modo'", "INFO")
                    return self.log.agregarLinea(self.consola.do_modo.__doc__, "INFO")
                elif args[0] == "ejecutartarea":
                    self.log.agregarLinea("El usuario solicita informacion de 'ejecutartarea'", "INFO")
                    return self.log.agregarLinea(self.consola.do_ejecutartarea.__doc__, "INFO")
                elif args[0] == "cargartarea":
                    self.log.agregarLinea("El usuario solicita informacion de 'cargartarea'", "INFO")
                    return self.log.agregarLinea(self.consola.do_cargartarea.__doc__, "INFO")
                elif args[0] == "efectorfinal":
                    self.log.agregarLinea("El usuario solicita informacion de 'efectorfinal'", "INFO")
                    return self.log.agregarLinea(self.consola.do_efectorfinal.__doc__, "INFO")
                else:
                    return self.log.agregarLinea("Comando help no identificable","ERROR HELP")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR HELP")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _home(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 0:
                self.log.agregarLinea("Usuario solicita ir a la posicion home","INFO")
                return self.log.agregarLinea(self.consola.do_home(), "INFO")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
        
    def _listarMetodos(self, token, *args):
        if token in self.tokensvalidos:
            if len(args)==0:
                self.log.agregarLinea("Usuario solicita listar los metodos disponibles","INFO")
                resultado = list(super().system_listMethods())
                return resultado
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR LISTARMETODOS")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _movlin(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 3:
                self.log.agregarLinea(f"Usuario solicita moverse a la posicion '{args[0]}' '{args[1]}' '{args[2]}'","INFO")
                return self.log.agregarLinea(self.consola.do_movlin(f"{args[0]} {args[1]} {args[2]}"), "INFO")
            elif len(args) == 4:
                self.log.agregarLinea(f"Usuario solicita moverse a la posicion '{args[0]}' '{args[1]}' '{args[2]}' '{args[3]}'","INFO")
                return self.log.agregarLinea(self.consola.do_movlin(f"{args[0]} {args[1]} {args[2]} {args[3]}"), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR MOVLIN")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _modo(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                self.log.agregarLinea(f"Usuario solicita cambiar el modo a '{args[0]}'","INFO")
                return self.log.agregarLinea(self.consola.do_modo(args[0]), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR MODO")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _ejecutartarea(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 0:
                self.log.agregarLinea("Usuario solicita ejecutar tarea","INFO")
                return self.log.agregarLinea(self.consola.do_ejecutartarea(""), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR EJECTARTAREA")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _cargartarea(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                self.log.agregarLinea(f"Usuario solicita cargar la tarea '{args[0]}'","INFO")
                return self.log.agregarLinea(self.consola.do_cargartarea(args[0]), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR CARGARTAREA")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _efectorfinal(self, token, *args):
        if token in self.tokensvalidos:
            if len(args) == 1:
                self.log.agregarLinea(f"Usuario solicita mover el efector final a la posicion '{args[0]}'","INFO")
                return self.log.agregarLinea(self.consola.do_efectorfinal(args[0]), "INFO")
            else:
                return self.log.agregarLinea("Cantidad de argumentos invalido","ERROR EFECTORFINAL")
        else:
            return self.log.agregarLinea("Token invalido o expirado","ERROR 401")