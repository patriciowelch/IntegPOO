import java.nio.file.Files;
import java.net.URL;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;

import java.io.*;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Scanner;

public class CLI {
    private String prompt = ">>> ";
    private String token = "";
    private String usuario;
    private String password;
    private String host;
    private int port;
    private XmlRpcClient client;
    private List<String> methods = new ArrayList<>();
    private Scanner scanner = new Scanner(System.in);

    public CLI() {
        System.out.println("Bienvenido Cliente");
    }

    public void iniciar() {
        String linea;
        while (true) {
            try {
                System.out.print(prompt);
                linea = scanner.nextLine();
                if (linea.length() >= 2 && linea.charAt(0) == ':' && linea.charAt(1) != ' ') {
                    linea = ":" + " " + linea.substring(1);
                }
                procesarComando(linea);
            } catch (XmlRpcException e) {
                System.out.println("Error: " + e.getMessage());
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }

    private void procesarComando(String linea) throws Exception {
        String[] tokens = linea.split(" ");
        String comando = tokens[0];
        List<String> args = new ArrayList<>();

        for (int i = 1; i < tokens.length; i++) {
            args.add(tokens[i]);
        }

        switch (comando) {
            case "quit":
                doQuit();
                break;
            case "conectar":
                doConectar();
                break;
            case "listarMetodos":
                try {
                    try {
                        doListarMetodos();
                    } catch (Exception e) {
                        System.out.println("Error: " + e.getMessage());
                    }
                } catch (Exception e) {
                    System.out.println("Error: " + e.getMessage());
                }
                break;
            case "help":
                doHelp(args);
                break;
            case "enviarArchivo":
                if (args.size() != 1) {
                    throw new IllegalArgumentException("Sintaxis: enviarArchivo <path>");
                }
                if (client == null) {
                    throw new IllegalStateException("No se ha conectado al servidor");
                }
                enviarArchivo(args.get(0));
                break;
            default:
                if (methods.contains(comando)) {
                    ejecutarMetodoServidor(comando, args);
                } else {
                    throw new IllegalArgumentException("Comando no reconocido");
                }
                break;
        }
    }

    private void doLogin() {
        System.out.print("Usuario: ");
        usuario = scanner.nextLine();
        System.out.print("Password: ");
        password = scanner.nextLine();
    }

    private void doSetServer() {
        System.out.print("Host: ");
        host = scanner.nextLine();
        System.out.print("Port: ");
        port = scanner.nextInt();
        scanner.nextLine(); // Consume the newline character
    }

    private void doConectar() throws Exception {
        doLogin();
        doSetServer();
        System.out.println("Conectando a " + host);
        
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://" + host + ":" + port + "/"));
        client = new XmlRpcClient();
        client.setConfig(config);

        List<Object> params = new ArrayList<>();
        params.add(usuario);
        params.add(password);
        
        try {
            token = (String) client.execute("iniciar_sesion", params);
            if (!token.startsWith("401:") && !token.isEmpty()) {
                System.out.println("Conexion exitosa");
                doListarMetodos();
            } else {
                token = "";
                throw new RuntimeException(token);
            }
        } catch (XmlRpcException e) {
            throw new RuntimeException("Error de Conexion: " + e.getMessage());
        }
    }

    private void doListarMetodos() throws Exception {
        if (client == null) {
            throw new IllegalStateException("No se ha conectado al servidor para obtener la lista de metodos");
        }

        List<Object> params = new ArrayList<>();
        params.add(token);

        methods.clear();
        List<String> nonListMethods = List.of("iniciar_sesion");
        
        try {
            Object[] result = (Object[]) client.execute("listarMetodos", params);
            System.out.println("\nMetodos: Use 'help [metodo]' para mas ayuda");
            int tammax = 0;
            for (Object method : result) {
                String methodName = (String) method;
                if (!nonListMethods.contains(methodName)) {
                    methods.add(methodName);
                    if(methodName.length() > tammax) {
                        tammax = methodName.length();
                    }
                }
            }
            tammax += 4;
            int a = 0;
            for (Object method : methods) {
                String methodName = (String) method;
                System.out.print(methodName);
                for (int i = 0; i < tammax - methodName.length(); i++) {
                    System.out.print(" ");
                }
                if(a%3 == 0 && a != 0) {
                    System.out.println();
                }
                a++;
            }
            System.out.println();
        } catch (XmlRpcException e) {
            throw new RuntimeException("Error de Conexion: " + e.getMessage());
        }
    }

    private void doHelp(List<String> args) {
        if (args.isEmpty()) {
            System.out.println("help <comando> para mas informacion\n");
            System.out.println("Comandos:");
            System.out.println("conectar\tlistarMetodos\tenviarArchivo\thelp\tquit");
            try {
                doListarMetodos();
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }
        } else if (args.size() == 1 && !methods.contains(args.get(0))) {
            switch (args.get(0)) {
                case "conectar":
                    System.out.println("Realizar la conexion con el servidor con usuario y contraseña\n\tSintaxis: conectar");
                    break;
                case "listarMetodos":
                    System.out.println("Listar los metodos disponibles en el servidor\n\tSintaxis: listarMetodos");
                    break;
                case "help":
                    System.out.println("Mostrar la ayuda de los comandos\n\tSintaxis:\thelp [comando]");
                    break;
                case "quit":
                    System.out.println("Salir del programa\n\tSintaxis: quit");
                    break;
                default:
                    System.out.println("Metodo no encontrado");
                    break;
            }
        }
    }

    private void enviarArchivo(String path) throws Exception {
        File file = new File(path);
        if (!file.exists()) {
            throw new RuntimeException("Error al abrir el archivo");
        }

        String fileName = file.getName();
        byte[] fileContent = Files.readAllBytes(file.toPath());
        String encoded = Base64.getEncoder().encodeToString(fileContent);

        List<Object> params = new ArrayList<>();
        params.add(token);
        params.add(fileName);
        params.add(encoded);

        try {
            String result = (String) client.execute("enviarArchivo", params);
            System.out.println(result);
        } catch (XmlRpcException e) {
            throw new RuntimeException("Error de Conexion: " + e.getMessage());
        }
    }

    private void ejecutarMetodoServidor(String comando, List<String> args) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(token);
        params.addAll(args);

        try {
            String result = (String) client.execute(comando, params.toArray());
            System.out.println(result);
        } catch (XmlRpcException e) {
            throw new RuntimeException("Error de Conexion: " + e.getMessage());
        }
    }

    private void doQuit() {
        System.exit(0);
    }

    public static void main(String[] args) {
        CLI cli = new CLI();
        cli.iniciar();
    }
}
