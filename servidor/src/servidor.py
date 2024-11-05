from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
from log import Log
import socket
from clientes import Clientes
import base64

class Handler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        server.ipCliente=client_address[0]
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
            print(self.consola.log.agregarLinea(e,"ERROR"))

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
        self.register_function(self._enviarArchivo, 'enviarArchivo')
        self.register_function(self._log, 'log')

        self.hiloRPC = Thread(target = self.correrServidor, daemon = True)
        self.hiloRPC.start()
        
        print(self.consola.log.agregarLinea("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address),"INFO"))


    def detener(self):
        super().shutdown()
        super().server_close()
        self.hiloRPC.join()
        self.consola.log.agregarLinea("Servidor detenido","INFO")
    
    def correrServidor(self):
        self.serve_forever()

    #aca va la ejecucion de los metodos que puede ejecutar el cliente
    def _iniciar_sesion(self, usuario, clave):
        #obtener la ip de la solicitud
        self.consola.log.agregarLinea(f"Usuario: {usuario} intenta iniciar sesion","INFO",usuario,self.ipCliente)
        usuarioValido = self.clientes.validar_cliente(usuario, clave)
        if usuarioValido is not None:
            self.consola.log.agregarLinea(f"Sesion de {usuarioValido.nick} iniciada con exito","INFO",usuarioValido.nick,self.ipCliente)
            token = self.clientes.generar_token()
            usuarioValido.token = token
            usuarioValido.ipActual = self.ipCliente
            self.tokensvalidos.append(token)
            return token
        else:
            return self.consola.log.agregarLinea("Usuario o contraseña invalidos","ERROR 401")

    def _guardar_cmd(self, token, *a):
        args = list(a)
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 1:
                self.consola.log.agregarLinea(f"Usuario solicita guardar comando en el archivo {args[0]}","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("guardarcmd "+args[0],True)+"\nPara guardar un comando escriba ':[comando]'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
            elif len(args) == 0:
                self.consola.log.agregarLinea("Usuario solicita desactivar guardado de comando","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("guardarcmd",True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR GUARDARCMD",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _defguardar(self, token, *args):
        comando = " ".join(args)
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            return self.consola.log.agregarLinea(self.consola.onecmd(comando, True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _robot(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if(len(args)==1):
                self.consola.log.agregarLinea(f"Usuario solicita enviar el comando '{args[0]}' al robot","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("robot "+args[0],True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR ROBOT",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _help(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args)==1:
                if args[0] == "guardarcmd":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'guardarcmd'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_guardarcmd.__doc__, "INFO")
                elif args[0] == "robot":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'robot'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_robot.__doc__, "INFO")
                elif args[0] == "listarMetodos":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'listarMetodos'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea("Lista los metodos disponibles en el servidor", "INFO")
                elif args[0] == ":":
                    self.consola.log.agregarLinea("El usuario solicita informacion de ':'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea("Guarda el comando ingresado si se encuentra en modo guardado de comandos\n\t:[comando]", "INFO")
                elif args[0] == "enviarArchivo":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'enviarArchivo'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea("Envia al servidor el archivo en el 'path' descripto\n\tenviarArchivo <path>", "INFO")
                elif args[0] == "home":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'home'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_home.__doc__, "INFO")
                elif args[0] == "movlin":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'movlin'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_movlin.__doc__, "INFO")
                elif args[0] == "modo":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'modo'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_modo.__doc__, "INFO")
                elif args[0] == "ejecutartarea":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'ejecutartarea'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_ejecutartarea.__doc__, "INFO")
                elif args[0] == "cargartarea":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'cargartarea'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_cargartarea.__doc__, "INFO")
                elif args[0] == "efectorfinal":
                    self.consola.log.agregarLinea("El usuario solicita informacion de 'efectorfinal'", "INFO",usuarioValido.nick,usuarioValido.ipActual)
                    return self.consola.log.agregarLinea(self.consola.do_efectorfinal.__doc__, "INFO")
                else:
                    return self.consola.log.agregarLinea("Comando help no identificable","ERROR HELP",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR HELP",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _home(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 0:
                self.consola.log.agregarLinea("Usuario solicita ir a la posicion home","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("home",True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
        
    def _listarMetodos(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args)==0:
                self.consola.log.agregarLinea("Usuario solicita listar los metodos disponibles","INFO",usuarioValido.nick,usuarioValido.ipActual)
                resultado = list(super().system_listMethods())
                return resultado
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR LISTARMETODOS")
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _movlin(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 3:
                self.consola.log.agregarLinea(f"Usuario solicita moverse a la posicion '{args[0]}' '{args[1]}' '{args[2]}'","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("movlin "+f"{args[0]} {args[1]} {args[2]}",True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            elif len(args) == 4:
                self.consola.log.agregarLinea(f"Usuario solicita moverse a la posicion '{args[0]}' '{args[1]}' '{args[2]}' '{args[3]}'","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("movlin "+f"{args[0]} {args[1]} {args[2]} {args[3]}",True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR MOVLIN",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _modo(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 1:
                self.consola.log.agregarLinea(f"Usuario solicita cambiar el modo a '{args[0]}'","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("modo "+args[0],True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR MODO",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _ejecutartarea(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 0:
                self.consola.log.agregarLinea("Usuario solicita ejecutar tarea","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("ejecutartarea",True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR EJECUTARTAREA",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _cargartarea(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 1:
                self.consola.log.agregarLinea(f"Usuario solicita cargar la tarea '{args[0]}'","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("cargartarea "+args[0],True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR CARGARTAREA",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")

    def _efectorfinal(self, token, *args):
        usuarioValido = self.clientes.get_usuario_ip_con_token(token)
        if token in self.tokensvalidos:
            if len(args) == 1:
                self.consola.log.agregarLinea(f"Usuario solicita mover el efector final a la posicion '{args[0]}'","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.log.agregarLinea(self.consola.onecmd("efectorfinal "+args[0],True), "INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR EFECTORFINAL",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _enviarArchivo(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            self.consola.log.agregarLinea(f"Usuario solicita enviar archivo","INFO",usuarioValido.nick,usuarioValido.ipActual)
            if len(args) == 2:
                gcode_content = base64.b64decode(args[1])
                with open(f"servidor/anexo/Task_Files/{args[0]}", "wb") as f:
                    f.write(gcode_content)
                return self.consola.log.agregarLinea(f"Archivo con nombre {args[0]} recibido con exito","INFO",usuarioValido.nick,usuarioValido.ipActual)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR ENVIARARCHIVO",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")
        
    def _log(self, token, *args):
        if token in self.tokensvalidos:
            usuarioValido = self.clientes.get_usuario_ip_con_token(token)
            if len(args) == 0:
                self.consola.log.agregarLinea("Usuario solicita ver el log","INFO",usuarioValido.nick,usuarioValido.ipActual)
                return self.consola.onecmd("log 20",True)
            else:
                return self.consola.log.agregarLinea("Cantidad de argumentos invalido","ERROR LOG",usuarioValido.nick,usuarioValido.ipActual)
        else:
            return self.consola.log.agregarLinea("Token invalido o expirado","ERROR 401")