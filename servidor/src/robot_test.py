import unittest
from unittest.mock import patch, MagicMock
from robot import Robot  # Asegúrate de importar la clase desde el archivo correcto


class TestRobot(unittest.TestCase):

    def setUp(self):
        """Configura una instancia de Robot antes de cada prueba."""
        self.robot = Robot("COM5")

    @patch('robot.serial.Serial')
    def test_conectar(self, mock_serial):
        """Prueba que el robot se conecte correctamente."""
        self.robot.conectar()
        mock_serial.assert_called_with("COM5", baudrate=9600, timeout=1)
        self.assertTrue(self.robot.serial.is_open)

    @patch('robot.serial.Serial')
    def test_desconectar(self, mock_serial):
        """Prueba que el robot se desconecte correctamente."""
        self.robot.conectar()
        self.robot.desconectar()
        self.assertFalse(self.robot.serial.is_open)

    @patch('robot.serial.Serial')
    def test_activar_motor(self, mock_serial):
        """Prueba que el comando de activación de motores se envíe correctamente."""
        self.robot.conectar()
        self.robot.enviar_comando = MagicMock()
        self.robot.activar_motor()
        self.robot.enviar_comando.assert_called_with("M17")  # Ejemplo de comando para activar motores

    @patch('robot.serial.Serial')
    def test_desactivar_motor(self, mock_serial):
        """Prueba que el comando de desactivación de motores se envíe correctamente."""
        self.robot.conectar()
        self.robot.enviar_comando = MagicMock()
        self.robot.desactivar_motor()
        self.robot.enviar_comando.assert_called_with("M18")  # Ejemplo de comando para desactivar motores

    def test_cambiar_puerto(self):
        """Prueba que el puerto del robot se pueda cambiar correctamente."""
        nuevo_puerto = "COM6"
        self.robot.cambiar_puerto(nuevo_puerto)
        self.assertEqual(self.robot.puerto, nuevo_puerto)

    @patch('robot.serial.Serial')
    def test_enviar_comando(self, mock_serial):
        """Prueba que se envíe correctamente un comando G-code al robot."""
        self.robot.conectar()
        self.robot.serial.write = MagicMock()
        comando = "G1 X10 Y10 Z10"
        self.robot.enviar_comando(comando)
        self.robot.serial.write.assert_called_with(f"{comando}\n".encode())

    def test_estadoActual(self):
        """Prueba que el método estadoActual devuelva el estado correcto de la conexión."""
        with patch('robot.serial.Serial') as mock_serial:
            mock_serial.is_open = True
            self.assertTrue(self.robot.estadoActual())
            mock_serial.is_open = False
            self.assertFalse(self.robot.estadoActual())

    def tearDown(self):
        """Limpia después de cada prueba."""
        self.robot = None


if __name__ == '__main__':
    unittest.main()
