import pickle

class Clientes:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def guardar_clientes(self):
        with open('clientes.pkl', 'wb') as archivo:
            pickle.dump(self.clientes, archivo)

    def cargar_clientes(self):
        try:
            with open('clientes.pkl', 'rb') as archivo:
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