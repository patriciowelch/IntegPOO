#cliente xmlrpc para testear el servidor
from xmlrpc.client import ServerProxy

ip = '127.0.0.1'
puerto = 8000

proxy = ServerProxy(f'http://{ip}:{puerto}')
proxy.robot('pato', '1234')