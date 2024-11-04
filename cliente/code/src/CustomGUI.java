import javax.swing.*;
import java.awt.*;

public class CustomGUI extends JFrame {

    public CustomGUI() {
        setTitle("Cliente GUI");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLayout(new BorderLayout());

        // Configuración de GridBagConstraints para controlar el tamaño y posición de los paneles
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5); // Margen entre componentes
        gbc.fill = GridBagConstraints.BOTH; // Expandir componentes para llenar celdas

        // Panel para conexión
        JPanel connectionPanel = new JPanel(new GridLayout(5, 2, 5, 5));
        connectionPanel.setBorder(BorderFactory.createTitledBorder("Conexión"));
        connectionPanel.add(new JLabel("IP:"));
        JTextField ipField = new JTextField();
        connectionPanel.add(ipField);

        connectionPanel.add(new JLabel("Puerto:"));
        JTextField portField = new JTextField();
        connectionPanel.add(portField);

        connectionPanel.add(new JLabel("Usuario:"));
        JTextField userField = new JTextField();
        connectionPanel.add(userField);

        connectionPanel.add(new JLabel("Contraseña:"));
        JPasswordField passwordField = new JPasswordField();
        connectionPanel.add(passwordField);
        connectionPanel.add(new JLabel());

        JButton connectButton = new JButton("Conectar");
        connectionPanel.add(connectButton);

        // Panel de control del robot
        JPanel robotPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        robotPanel.setBorder(BorderFactory.createTitledBorder("Robot"));
        JButton connectRobotBtn = new JButton("Conectar");
        JButton disconnectRobotBtn = new JButton("Desconectar");
        JButton motorsOnBtn = new JButton("Encender Motores");
        JButton motorsOffBtn = new JButton("Apagar Motores");
        JButton getStateBtn = new JButton("Obtener Estado");
        JButton doHomeButton = new JButton("Home");

        robotPanel.add(connectRobotBtn);
        robotPanel.add(disconnectRobotBtn);
        robotPanel.add(motorsOnBtn);
        robotPanel.add(motorsOffBtn);
        robotPanel.add(getStateBtn);
        robotPanel.add(doHomeButton);

        // Panel de movimientos
        JPanel movlinPanel = new JPanel(new FlowLayout());
        movlinPanel.setBorder(BorderFactory.createTitledBorder("MovLin"));
        movlinPanel.add(new JLabel("X:"));
        JTextField xField = new JTextField(5);
        movlinPanel.add(xField);

        movlinPanel.add(new JLabel("Y:"));
        JTextField yField = new JTextField(5);
        movlinPanel.add(yField);

        movlinPanel.add(new JLabel("Z:"));
        JTextField zField = new JTextField(5);
        movlinPanel.add(zField);

        movlinPanel.add(new JLabel("Vel:"));
        JTextField velField = new JTextField(5);
        movlinPanel.add(velField);

        JButton sendMoveBtn = new JButton("Enviar");
        movlinPanel.add(sendMoveBtn);

        // Panel de efector final
        JPanel efectorPanel = new JPanel(new GridLayout(1, 2, 5, 5));
        efectorPanel.setBorder(BorderFactory.createTitledBorder("Efector Final"));
        JButton openGripperBtn = new JButton("Abrir");
        JButton closeGripperBtn = new JButton("Cerrar");
        efectorPanel.add(openGripperBtn);
        efectorPanel.add(closeGripperBtn);

        // Panel para enviar archivos
        JPanel filePanel = new JPanel(new FlowLayout());
        filePanel.setBorder(BorderFactory.createTitledBorder("Enviar Archivo"));
        JTextField pathField = new JTextField(15);
        JButton selectFileBtn = new JButton("...");
        JButton sendFileBtn = new JButton("Enviar Archivo");
        filePanel.add(pathField);
        filePanel.add(selectFileBtn);
        filePanel.add(sendFileBtn);

        // Área de salida de texto
        JTextArea outputArea = new JTextArea(10, 50);
        outputArea.setEditable(false);
        JScrollPane outputScrollPane = new JScrollPane(outputArea);

        // Panel de seleccion de modo
        JPanel selectModePanel = new JPanel(new GridLayout(1, 2, 5, 5));
        selectModePanel.setBorder(BorderFactory.createTitledBorder("Seleccionar Modo"));
        JButton absoluteModeBtn = new JButton("Modo Absoluto");
        JButton relativeModeBtn = new JButton("Modo Relativo");
        selectModePanel.add(absoluteModeBtn);
        selectModePanel.add(relativeModeBtn);

        // Panel de ejecucion de archivos
        JPanel execModePanel = new JPanel(new FlowLayout());
        execModePanel.setBorder(BorderFactory.createTitledBorder("Cargar/Ejecutar Tarea"));
        //text input para nombre de archivo
        JTextField taskField = new JTextField(15);
        JButton loadTaskBtn = new JButton("Cargar");
        JButton execTaskBtn = new JButton("Ejecutar");
        execModePanel.add(taskField);
        execModePanel.add(loadTaskBtn);
        execModePanel.add(execTaskBtn);

        // Organizar los paneles en un layout de GridBagLayout
        JPanel mainPanel = new JPanel(new GridBagLayout());

        // Añadir el panel de conexión en 0,0 y 0,1
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridheight = 2; // Ocupa dos filas
        gbc.weightx = 1;
        gbc.weighty = 0.2;
        mainPanel.add(connectionPanel, gbc);

        // Añadir el panel MovLin en 0,2
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridheight = 1; // Ocupa una fila
        mainPanel.add(movlinPanel, gbc);

        // Añadir el panel de enviar archivo en 0,3
        gbc.gridx = 0;
        gbc.gridy = 3;
        mainPanel.add(filePanel, gbc);

        // Añadir el panel del robot en 1,0
        gbc.gridx = 1;
        gbc.gridy = 0;
        gbc.gridheight = 1; // Ocupa una fila
        mainPanel.add(robotPanel, gbc);

        // Añadir el panel Efector Final en 1,1
        gbc.gridx = 1;
        gbc.gridy = 1;
        mainPanel.add(efectorPanel, gbc);

        // Añadir el panel adicional 1 en 1,2
        gbc.gridx = 1;
        gbc.gridy = 2;
        mainPanel.add(selectModePanel, gbc);

        // Añadir el panel adicional 2 en 1,3
        gbc.gridx = 1;
        gbc.gridy = 3;
        mainPanel.add(execModePanel, gbc);

        // Añadir el área de salida de texto en la parte inferior
        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 2; // Ocupa dos columnas
        gbc.weighty = 0.4;
        mainPanel.add(outputScrollPane, gbc);

        add(mainPanel, BorderLayout.CENTER);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            CustomGUI gui = new CustomGUI();
            gui.setVisible(true);
        });
    }
}
