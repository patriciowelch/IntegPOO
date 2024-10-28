import pickle

class Clientes:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, usuario, clave):
        self.clientes.append(Cliente(usuario, clave))
        self.guardar_clientes()
        return 'Cliente agregado'

    def guardar_clientes(self):
        with open('servidor/anexo/clientes.pkl', 'wb') as archivo:
            pickle.dump(self.clientes, archivo)
    
    def validar_cliente(self, usuario, clave):
        for cliente in self.clientes:
            if cliente.usuario == usuario and cliente.clave == clave:
                return True
        return False

    def cargar_clientes(self):
        try:
            with open('servidor/anexo/clientes.pkl', 'rb') as archivo:
                self.clientes = pickle.load(archivo)
        except FileNotFoundError:
            print('No existe el archivo de clientes')

class Cliente:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave
    def __str__(self):
        return f'{self.usuario}'
    def mostrar_clave(self):
        return self.clave
    
    
if __name__ == '__main__':
    try:
        raise SystemExit
    except KeyboardInterrupt:
        print('Saliendo disconforme...')
        exit(0)
    except SystemExit:
        print('Saliendo conforme....')