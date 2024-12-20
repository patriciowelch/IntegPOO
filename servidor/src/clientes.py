import pickle
import random
import string

class Clientes:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, usuario, clave):
        self.clientes.append(Cliente(usuario, clave))
        self.guardar_clientes()
        return 'Cliente \'%s\' agregado' % usuario

    def guardar_clientes(self):
        with open('servidor/anexo/clientes.pkl', 'wb') as archivo:
            pickle.dump(self.clientes, archivo)
    
    def validar_cliente(self, usuario, clave):
        for cliente in self.clientes:
            if cliente.nick == usuario and cliente.clave == clave:
                return cliente
        return None
    
    def generar_token(self):
        #genera un token aleatorio alfanumerico de 10 caracteres
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def cargar_clientes(self):
        try:
            with open('servidor/anexo/clientes.pkl', 'rb') as archivo:
                self.clientes = pickle.load(archivo)
        except FileNotFoundError:
            print('No existe el archivo de clientes')

    def get_usuario_ip_con_token(self, token):
        for cliente in self.clientes:
            if cliente.token == token:
                return cliente
        return None

class Cliente:
    def __init__(self, usuario, clave):
        self.nick = usuario
        self.clave = clave
        self.token = None
        self.ipActual = None
    def __str__(self):
        return f'user:{self.nick} pass:{self.clave}'