import unittest
from unittest.mock import patch, MagicMock
from cli import cli

class TestCLI(unittest.TestCase):
    
    def setUp(self):
        # Crear una instancia de la clase `cli` para cada prueba
        self.cli_instance = cli()
    
    @patch('cli.Servidor')  # Simula la clase Servidor
    def test_do_servidor_on(self, MockServidor):
        # Simular la creación del servidor
        self.cli_instance.do_servidor("on balhou")
        self.assertIsNotNone(self.cli_instance.servidorRpc)  # Asegurarse de que el servidor esté inicializado
    
    @patch('cli.Servidor')
    def test_do_servidor_off(self, MockServidor):
        # Iniciar el servidor primero
        self.cli_instance.servidorRpc = MockServidor()
        result = self.cli_instance.do_servidor("off balhou")
        self.assertIsNone(self.cli_instance.servidorRpc)  # El servidor debe estar detenido
        self.assertEqual(result, "Servidor detenido")

    @patch('cli.Robot')  # Simula la clase Robot
    def test_do_robot_conectar(self, MockRobot):
        # Simular el método conectar del robot
        self.cli_instance.robot.conectar = MagicMock(return_value="Robot conectado")
        self.cli_instance.robot.serial = "12345"  # Mock the serial attribute
        result = self.cli_instance.do_robot("conectar")
        self.assertEqual(result, "Robot conectado")
        self.assertIsNotNone(self.cli_instance.robot.serial)  # Asegurarse de que el robot esté inicializado
    
    @patch('cli.Robot')
    def test_do_robot_desconectar(self, MockRobot):
        # Simular el método desconectar del robot
        self.cli_instance.robot.desconectar = MagicMock(return_value="Robot desconectado")
        result = self.cli_instance.do_robot("desconectar")
        self.assertEqual(result, "Robot desconectado")
    
    @patch('cli.Robot')
    def test_do_home(self, MockRobot):
        # Simular el comando 'G28' para el movimiento home
        self.cli_instance.robot.enviar_comando = MagicMock(return_value="Comando G28 enviado")
        result = self.cli_instance.do_home("")
        self.assertEqual(result, "Comando G28 enviado")

    @patch('cli.Robot')
    def test_do_movlin(self, MockRobot):
        # Simular el comando de movimiento lineal
        self.cli_instance.robot.enviar_comando = MagicMock(return_value="Comando G1 enviado")
        result = self.cli_instance.do_movlin("10 20 30")
        self.assertEqual(result, "Comando G1 enviado")
    
    def tearDown(self):
        # Limpiar después de cada prueba si es n
        pass

if __name__ == "__main__":
    unittest.main()