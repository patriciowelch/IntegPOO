package cliente.code.headers;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.text.AbstractDocument;
import javax.swing.filechooser.FileNameExtensionFilter;

import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.*;
import java.awt.event.FocusListener;
import java.awt.event.FocusEvent;

public class CustomGUI extends JFrame {

    private JTextArea outputArea;
    private Process cliProcess;
    private BufferedWriter cliWriter;
    private JTextField xField, yField, zField, velField;
    private JTextField pathField;
    private JTextField commandToSave;
    private JTextField nameFile;

    // Colores personalizados
    private Color textColor = Color.WHITE;
    private Color darkBackground = Color.DARK_GRAY;
    private Process mainProcess;

    public CustomGUI() {
        iniciarComponentes();
        iniciarCLI();
    }

    public void iniciarComponentes() {
        setTitle("Cliente GUI");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLayout(new BorderLayout());

        // Configuración de GridBagConstraints para controlar el tamaño y posición de
        // los paneles
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5); // Margen entre componentes
        gbc.fill = GridBagConstraints.BOTH; // Expandir componentes para llenar celdas

        // Panel para conexión
        JPanel connectionPanel = new JPanel(new GridLayout(5, 2, 5, 5));
        connectionPanel.setBorder(createTitledBorder("Conexión"));
        connectionPanel.setBackground(darkBackground);

        JLabel ipLabel = new JLabel("IP:");
        ipLabel.setForeground(textColor);
        connectionPanel.add(ipLabel);
        JTextField ipField = new JTextField();
        connectionPanel.add(ipField);

        JLabel portLabel = new JLabel("Puerto:");
        portLabel.setForeground(textColor);
        connectionPanel.add(portLabel);
        JTextField portField = new JTextField();
        connectionPanel.add(portField);

        JLabel userLabel = new JLabel("Usuario:");
        userLabel.setForeground(textColor);
        connectionPanel.add(userLabel);
        JTextField userField = new JTextField();
        connectionPanel.add(userField);

        JLabel passwordLabel = new JLabel("Contraseña:");
        passwordLabel.setForeground(textColor);
        connectionPanel.add(passwordLabel);
        JPasswordField passwordField = new JPasswordField();
        connectionPanel.add(passwordField);
        connectionPanel.add(new JLabel());

        JButton connectButton = new JButton("Conectar");
        connectButton.addActionListener(_ -> conectar(ipField.getText(), portField.getText(), userField.getText(),
                new String(passwordField.getPassword())));
        connectionPanel.add(connectButton);

        // Panel de control del robot
        JPanel robotPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        robotPanel.setBorder(createTitledBorder("Robot"));
        robotPanel.setBackground(darkBackground);

        JButton connectRobotBtn = new JButton("Conectar");
        connectRobotBtn.addActionListener(_ -> conectarRobot());
        JButton disconnectRobotBtn = new JButton("Desconectar");
        disconnectRobotBtn.addActionListener(_ -> desconectarRobot());
        JButton motorsOnBtn = new JButton("Encender Motores");
        motorsOnBtn.addActionListener(_ -> encenderMotores());
        JButton motorsOffBtn = new JButton("Apagar Motores");
        motorsOffBtn.addActionListener(_ -> apagarMotores());
        JButton getStateBtn = new JButton("Obtener Estado");
        getStateBtn.addActionListener(_ -> obtenerEstado());
        JButton doHomeButton = new JButton("Home");
        doHomeButton.addActionListener(_ -> moverHome());

        robotPanel.add(connectRobotBtn);
        robotPanel.add(disconnectRobotBtn);
        robotPanel.add(motorsOnBtn);
        robotPanel.add(motorsOffBtn);
        robotPanel.add(getStateBtn);
        robotPanel.add(doHomeButton);

        // Panel de movimientos
        JPanel movlinPanel = new JPanel(new GridLayout(2, 5, 5, 5));
        movlinPanel.setBorder(createTitledBorder("MovLin"));
        movlinPanel.setBackground(darkBackground);

        JLabel xLabel = new JLabel("X:");
        xLabel.setForeground(textColor);
        movlinPanel.add(xLabel);

        JLabel yLabel = new JLabel("Y:");
        yLabel.setForeground(textColor);
        movlinPanel.add(yLabel);

        JLabel zLabel = new JLabel("Z:");
        zLabel.setForeground(textColor);
        movlinPanel.add(zLabel);

        JLabel velLabel = new JLabel("Velocidad:");
        velLabel.setForeground(textColor);
        movlinPanel.add(velLabel);

        JLabel emptyLabel = new JLabel();
        movlinPanel.add(emptyLabel);
        movlinPanel.add(emptyLabel);

        xField = new JTextField(5);
        ((AbstractDocument) xField.getDocument()).setDocumentFilter(new NumericTextFieldFilter());
        movlinPanel.add(xField);

        yField = new JTextField(5);
        ((AbstractDocument) yField.getDocument()).setDocumentFilter(new NumericTextFieldFilter());
        movlinPanel.add(yField);

        zField = new JTextField(5);
        ((AbstractDocument) zField.getDocument()).setDocumentFilter(new NumericTextFieldFilter());
        movlinPanel.add(zField);

        velField = new JTextField(5);
        ((AbstractDocument) velField.getDocument()).setDocumentFilter(new NumericTextFieldFilter());
        movlinPanel.add(velField);

        JButton sendMoveBtn = new JButton("Enviar");
        sendMoveBtn.addActionListener(
                _ -> enviarMovimiento(xField.getText(), yField.getText(), zField.getText(), velField.getText()));
        movlinPanel.add(sendMoveBtn);

        // Panel de efector final
        JPanel efectorPanel = new JPanel(new GridLayout(1, 2, 5, 5));
        efectorPanel.setBorder(createTitledBorder("Efector Final"));
        efectorPanel.setBackground(darkBackground);

        JButton openGripperBtn = new JButton("Abrir");
        openGripperBtn.addActionListener(_ -> abrirEfector());
        JButton closeGripperBtn = new JButton("Cerrar");
        closeGripperBtn.addActionListener(_ -> cerrarEfector());
        efectorPanel.add(openGripperBtn);
        efectorPanel.add(closeGripperBtn);

        // Panel para enviar archivos
        JPanel filePanel = new JPanel(new FlowLayout());
        filePanel.setBorder(createTitledBorder("Enviar Archivo"));
        filePanel.setBackground(darkBackground);

        pathField = new JTextField(15);
        //agregar hint al campo de texto
        pathField.addFocusListener(new FocusListener() {
            @Override
            public void focusGained(FocusEvent e) {
                if (pathField.getText().equals("Ruta del archivo")) {
                    pathField.setText("");
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (pathField.getText().isEmpty()) {
                    pathField.setText("Ruta del archivo");
                }
            }
        });
        pathField.setText("Ruta del archivo");
        JButton selectFileBtn = new JButton("...");
        selectFileBtn.addActionListener(_ -> seleccionarArchivo());
        JButton sendFileBtn = new JButton("Enviar Archivo");
        sendFileBtn.addActionListener(_ -> enviarArchivo(pathField.getText()));
        filePanel.add(pathField);
        filePanel.add(selectFileBtn);
        filePanel.add(sendFileBtn);

        // Área de salida de texto
        outputArea = new JTextArea(10, 50);
        outputArea.setEditable(false);
        outputArea.setBackground(darkBackground);
        outputArea.setForeground(textColor);
        JScrollPane outputScrollPane = new JScrollPane(outputArea);
        outputArea.getDocument().addDocumentListener(new javax.swing.event.DocumentListener() {
            @Override
            public void insertUpdate(javax.swing.event.DocumentEvent e) {
                scrollToBottom();
            }

            @Override
            public void removeUpdate(javax.swing.event.DocumentEvent e) {
                scrollToBottom();
            }

            @Override
            public void changedUpdate(javax.swing.event.DocumentEvent e) {
                scrollToBottom();
            }

            private void scrollToBottom() {
                outputArea.setCaretPosition(outputArea.getDocument().getLength());
            }
        });

        // Panel de selección de modo
        JPanel selectModePanel = new JPanel(new GridLayout(1, 2, 5, 5));
        selectModePanel.setBorder(createTitledBorder("Seleccionar Modo"));
        selectModePanel.setBackground(darkBackground);

        JButton absoluteModeBtn = new JButton("Modo Absoluto");
        absoluteModeBtn.addActionListener(_ -> cambiarAModoAbsoluto());
        JButton relativeModeBtn = new JButton("Modo Relativo");
        relativeModeBtn.addActionListener(_ -> cambiarAModoRelativo());
        selectModePanel.add(absoluteModeBtn);
        selectModePanel.add(relativeModeBtn);

        // Panel de ejecución de archivos
        JPanel execModePanel = new JPanel(new FlowLayout());
        execModePanel.setBorder(createTitledBorder("Cargar/Ejecutar Tarea"));
        execModePanel.setBackground(darkBackground);

        JTextField taskField = new JTextField(15);
        taskField.addFocusListener(new FocusListener() {
            @Override
            public void focusGained(FocusEvent e) {
                if (taskField.getText().equals("Nombre del archivo")) {
                    taskField.setText("");
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (taskField.getText().isEmpty()) {
                    taskField.setText("Nombre del archivo");
                }
            }
        });
        taskField.setText("Nombre del archivo");
        JButton loadTaskBtn = new JButton("Cargar");
        loadTaskBtn.addActionListener(_ -> cargarArchivo(taskField.getText()));
        JButton execTaskBtn = new JButton("Ejecutar");
        execTaskBtn.addActionListener(_ -> ejecutarArchivo());
        execModePanel.add(taskField);
        execModePanel.add(loadTaskBtn);
        execModePanel.add(execTaskBtn);

        // Panel para guardar comandos en un archivo
        JPanel saveAndLog = new JPanel(new GridLayout(2, 3, 5, 5));
        saveAndLog.setBorder(createTitledBorder("Guardar Comandos"));
        saveAndLog.setBackground(darkBackground);

        nameFile = new JTextField(15);
        nameFile.addFocusListener(new FocusListener() {
            @Override
            public void focusGained(FocusEvent e) {
                if (nameFile.getText().equals("Nombre del archivo")) {
                    nameFile.setText("");
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (nameFile.getText().isEmpty()) {
                    nameFile.setText("Nombre del archivo");
                }
            }
        });
        nameFile.setText("Nombre del archivo");
        commandToSave = new JTextField(15);
        commandToSave.addFocusListener(new FocusListener() {
            @Override
            public void focusGained(FocusEvent e) {
                if (commandToSave.getText().equals("Comando a guardar")) {
                    commandToSave.setText("");
                }
            }

            @Override
            public void focusLost(FocusEvent e) {
                if (commandToSave.getText().isEmpty()) {
                    commandToSave.setText("Comando a guardar");
                }
            }
        });
        commandToSave.setText("Comando a guardar");
        JButton saveCommandsBtn = new JButton("Iniciar Guardado");
        JButton stopSaveCommandsBtn = new JButton("Detener Guardado");
        JButton logCommandsBtn = new JButton("Log Comandos");
        JButton enviarComandosBtn = new JButton("Enviar Comandos");
        saveAndLog.add(nameFile);
        saveAndLog.add(saveCommandsBtn);
        saveAndLog.add(stopSaveCommandsBtn);
        saveAndLog.add(commandToSave);
        saveAndLog.add(enviarComandosBtn);
        saveAndLog.add(logCommandsBtn);
        saveCommandsBtn.addActionListener(_ -> iniciarGuardarCMD(nameFile.getText()));
        stopSaveCommandsBtn.addActionListener(_ -> detenerGuardarCMD());
        logCommandsBtn.addActionListener(_ -> logComandos());
        enviarComandosBtn.addActionListener(_ -> enviarComandos(commandToSave.getText()));

        // Organizar los paneles en un layout de GridBagLayout
        JPanel mainPanel = new JPanel(new GridBagLayout());
        mainPanel.setBackground(darkBackground);

        // Añadir el panel de conexión en 0,0 y 0,1
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridheight = 3; // Ocupa dos filas
        gbc.weightx = 1;
        gbc.weighty = 0.15;
        mainPanel.add(connectionPanel, gbc);

        // Añadir el panel MovLin en 0,2
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridheight = 1; // Ocupa una fila
        mainPanel.add(movlinPanel, gbc);

        // Añadir el panel de enviar archivo en 0,3
        gbc.gridx = 0;
        gbc.gridy = 4;
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

        // Añadir el panel adicional 3 en 1,4
        gbc.gridx = 1;
        gbc.gridy = 4;
        mainPanel.add(saveAndLog, gbc);

        // Añadir el área de salida de texto en la parte inferior
        gbc.gridx = 0;
        gbc.gridy = 5;
        gbc.gridwidth = 2; // Ocupa dos columnas
        gbc.weighty = 0.6;
        mainPanel.add(outputScrollPane, gbc);

        add(mainPanel, BorderLayout.CENTER);

        // Aplicar color de fondo general a la ventana principal
        getContentPane().setBackground(darkBackground);

        // Añadir un WindowListener para cerrar el proceso main.exe cuando se cierre la ventana
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                if (mainProcess != null) {
                    mainProcess.destroy();
                }
            }
        });
    }

    private void iniciarCLI() {
        try {
            // Reemplaza "ruta/a/tu/archivo.exe" con la ruta del archivo .exe de la CLI
            ProcessBuilder processBuilder = new ProcessBuilder(
                    new File(".").getCanonicalPath() + File.separator + "src/main.exe");
            processBuilder.redirectErrorStream(true); // Redirige errores al flujo de salida

            // Inicia el proceso
            cliProcess = processBuilder.start();

            // Configura los streams para leer y escribir en la CLI
            cliWriter = new BufferedWriter(new OutputStreamWriter(cliProcess.getOutputStream()));
            BufferedReader cliReader = new BufferedReader(new InputStreamReader(cliProcess.getInputStream()));

            // Hilo para leer la salida de la CLI y mostrarla en la interfaz
            new Thread(() -> {
                String line;
                try {
                    while ((line = cliReader.readLine()) != null) {
                        outputArea.append(line + "\n");
                    }
                } catch (IOException e) {
                    outputArea.append("Error leyendo salida de la CLI.\n");
                }
            }).start();

            outputArea.append("CLI iniciada exitosamente.\n");
        } catch (IOException e) {
            outputArea.append("Error al iniciar la CLI.\n");
        }
    }

    /**
     * Método para enviar comandos a la CLI
     */
    private void enviarComandoCLI(String comando) {
        try {
            if (cliWriter != null) {
                cliWriter.write(comando);
                cliWriter.newLine();
                cliWriter.flush();
            } else {
                outputArea.append("CLI no está disponible.\n");
            }
        } catch (IOException e) {
            outputArea.append("Error al enviar comando a la CLI.\n");
        }
    }

    private void conectar(String ip, String port, String user, String password) {
        if (ip.isEmpty() || port.isEmpty() || user.isEmpty() || password.isEmpty()) {
            outputArea.append("Por favor, complete todos los campos.\n");
            return;
        } else {
            outputArea.append("Conectando a " + ip + ":" + port + " como " + user + "\n");
            enviarComandoCLI("conectar");
            enviarComandoCLI(user);
            enviarComandoCLI(password);
            enviarComandoCLI(ip);
            enviarComandoCLI(port);
        }
    }

    private void conectarRobot() {
        outputArea.append("Conectando al robot...\n");
        enviarComandoCLI("robot conectar");
    }

    private void desconectarRobot() {
        outputArea.append("Desconectando del robot...\n");
        enviarComandoCLI("robot desconectar");
    }

    private void encenderMotores() {
        outputArea.append("Encendiendo motores...\n");
        enviarComandoCLI("robot motores_on");
    }

    private void apagarMotores() {
        outputArea.append("Apagando motores...\n");
        enviarComandoCLI("robot motores_off");
    }

    private void obtenerEstado() {
        outputArea.append("Obteniendo estado del robot...\n");
        enviarComandoCLI("robot estado");
    }

    private void moverHome() {
        outputArea.append("Moviendo a posición home...\n");
        enviarComandoCLI("home");
    }

    private void enviarMovimiento(String x, String y, String z, String vel) {
        if (x.isEmpty() || y.isEmpty() || z.isEmpty()) {
            outputArea.append("Por favor, complete todos los campos, al menos x y z.\n");
            return;
        } else if (vel.isEmpty()) {
            outputArea.append("Moviendo a X: " + x + ", Y: " + y + ", Z: " + z + "\n");
            enviarComandoCLI("movlin " + x + " " + y + " " + z);
        } else {
            outputArea.append("Moviendo a X: " + x + ", Y: " + y + ", Z: " + z + " con velocidad: " + vel + "\n");
            enviarComandoCLI("movlin " + x + " " + y + " " + z + " " + vel);
        }
        xField.setText("");
        yField.setText("");
        zField.setText("");
        velField.setText("");
    }

    private void abrirEfector() {
        outputArea.append("Abriendo efector final...\n");
        enviarComandoCLI("efectorfinal abrir");
    }

    private void cerrarEfector() {
        outputArea.append("Cerrando efector final...\n");
        enviarComandoCLI("efectorfinal cerrar");
    }

    private void cambiarAModoAbsoluto() {
        outputArea.append("Cambiando a modo absoluto...\n");
        enviarComandoCLI("modo abs");
    }

    private void cambiarAModoRelativo() {
        outputArea.append("Cambiando a modo relativo...\n");
        enviarComandoCLI("modo rel");
    }

    private void seleccionarArchivo() {
        JFileChooser fileChooser = new JFileChooser();
    
        // Filtra los tipos de archivo, por ejemplo, solo archivos .txt y .csv
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Archivos GCODE", "gcode");
        fileChooser.setFileFilter(filter);
        
        // Abre el diálogo de selección de archivos
        int result = fileChooser.showOpenDialog(this);
        
        if (result == JFileChooser.APPROVE_OPTION) {
            // Obtiene el archivo seleccionado
            java.io.File selectedFile = fileChooser.getSelectedFile();
            String filePath = selectedFile.getAbsolutePath();
            
            // Muestra la ruta del archivo en el área de salida
            outputArea.append("Archivo seleccionado: " + filePath + "\n");
            pathField.setText(filePath);
        } else {
            outputArea.append("Selección de archivo cancelada.\n");
        }
    }

    private void enviarArchivo(String path) {
        if(path.isEmpty() || path.equals("Ruta del archivo")) {
            outputArea.append("Por favor, seleccione un archivo.\n");
            return;
        } else {
            outputArea.append("Enviando archivo: " + path + "\n");
            enviarComandoCLI("enviarArchivo " + path);
        }
    }

    private void cargarArchivo(String path) {
        if(path.isEmpty() || path.equals("Nombre del archivo")) {
            outputArea.append("Por favor, seleccione un archivo.\n");
            return;
        } else {
            outputArea.append("Cargando archivo: " + path + "\n");
            enviarComandoCLI("cargartarea " + path);
        }
    }

    private void ejecutarArchivo() {
        outputArea.append("Ejecutando tarea...\n");
        enviarComandoCLI("ejecutartarea");
    }

    private void iniciarGuardarCMD(String nombreArchivo) {
        if(nombreArchivo.isEmpty() || nombreArchivo.equals("Nombre del archivo")) {
            outputArea.append("Por favor, ingrese un nombre de archivo.\n");
            return;
        } else {
            outputArea.append("Iniciando guardado de comandos en " + nombreArchivo + ".gcode\n");
            enviarComandoCLI("guardarcmd " + nombreArchivo);
        }
    }

    private void detenerGuardarCMD() {
        outputArea.append("Deteniendo guardado de comandos...\n");
        enviarComandoCLI("guardarcmd");
    }

    private void logComandos() {
        outputArea.append("Solicitando log de comandos...\n");
        enviarComandoCLI("log");
    }

    private void enviarComandos(String comandos) {
        if(comandos.isEmpty() || comandos.equals("Comando a guardar")) {
            outputArea.append("Por favor, ingrese un comando.\n");
            return;
        } else {
            outputArea.append("Enviando comando "+ comandos +"\n");
            enviarComandoCLI(":"+comandos);
            commandToSave.setText("Comando a guardar");
        }
    }

    // Método para crear un borde con título en color blanco
    private TitledBorder createTitledBorder(String title) {
        TitledBorder border = BorderFactory.createTitledBorder(title);
        border.setTitleColor(textColor); // Establece el color del título a blanco
        return border;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            CustomGUI gui = new CustomGUI();
            gui.setVisible(true);
        });
    }
}
