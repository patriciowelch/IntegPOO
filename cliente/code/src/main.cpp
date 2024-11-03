#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include "XmlRpc.h"
#include "base64.h"

using namespace XmlRpc;
using namespace std;

class CLI
{
public:
    CLI()
    {
        cout << "Bienvenido Cliente\n";
        prompt = ">>> ";
    }

    void iniciar()
    {
        string linea;
        while (true)
        {
            try
            {
                cout << prompt;
                getline(cin, linea);
                if (linea.length() >= 2)
                {
                    if (linea[0] == ':' && linea[1] != ' ')
                    {
                        linea.insert(1, " ");
                    }
                }
                procesarComando(linea);
            }
            catch (XmlRpcException &e)
            {
                cout << "Error: " << e.getMessage() << endl;
            }
            catch (const std::exception &e)
            {
                cout << e.what() << endl;
            }
            catch (...)
            {
                cout << "Se produjo un error desconocido" << endl;
            }
        }
    }

private:
    string prompt;
    string token = "";
    string usuario;
    string password;
    string host;
    int port;
    // XmlRpcClient client = XmlRpcClient("localhost", 8080);
    XmlRpcClient *client = nullptr;
    vector<string> methods;

    void procesarComando(const string &linea)
    {
        istringstream stream(linea);
        string comando;
        stream >> comando;
        vector<string> args = {};
        string arg;
        while (stream >> arg)
        {
            args.push_back(arg);
        }
        if (comando == "quit")
        {
            do_quit();
        }
        else if (comando == "conectar")
        {
            do_conectar();
        }
        else if (comando == "listarMetodos")
        {
            do_listarMetodos();
        }
        else if (comando == "enviarArchivo")
        {
            string path = args[0];
            enviarArchivo(path);
        }
        else if (find(methods.begin(), methods.end(), comando) != methods.end())
        {
            XmlRpcValue Args, result;
            Args[0] = token;
            for (int i = 0; i < args.size(); i++)
            {
                Args[i + 1] = args[i];
            }
            if (client->execute(comando.c_str(), Args, result))
            {
                cout << static_cast<string>(result) << endl;
            }
            else
            {
                throw runtime_error("Error de Conexion");
            }
        }
        else
        {
            throw runtime_error("Comando no reconocido");
        }
    }

    void do_login()
    {
        cout << "Usuario: ";
        getline(cin, usuario);
        cout << "Password: ";
        getline(cin, password);
    }

    void do_setServer()
    {
        cout << "Host: ";
        getline(cin, host);
        cout << "Port: ";
        cin >> port;
        cin.ignore();
    }

    void do_conectar()
    {
        do_login();
        do_setServer();
        cout << "Conectando a " << host << endl;
        // Intentar construir el cliente
        client = new XmlRpcClient(host.c_str(), port);
        XmlRpcValue Args, result;
        // args deberia contener el usuario y la contraseña
        Args[0] = usuario;
        Args[1] = password;
        // Ejecutar el método listarMetodos
        if (client->execute("iniciar_sesion", Args, result))
        {
            token = static_cast<string>(result);
            // si token no contiene '401:' entonces se ha logrado la conexión
            if (token.find("401:") == string::npos && token != "")
            {
                cout << "Conexion exitosa" << endl;
                do_listarMetodos();
            }
            else
            {
                string drop = token;
                token = "";
                throw runtime_error(drop);
            }
        }
        else
        {
            throw runtime_error("Error de Conexion");
        }
    }

    void do_listarMetodos()
    {
        XmlRpcValue result;
        XmlRpcValue args;
        args[0] = this->token;
        methods.clear();
        vector<string> non_listmethods;
        non_listmethods.push_back("iniciar_sesion");
        // Ejecutar el método "listarMetodos" sin argumentos
        client->execute("listarMetodos", args, result);
        // Convertir el resultado a vector de XmlRpcValue y mostrar cada método
        if (result.getType() == XmlRpcValue::TypeArray)
        {
            cout << "\nMetodos: Use '<help> [metodo]' para mas ayuda\n";
            for (int i = 0; i < result.size(); i++)
            {
                methods.push_back(static_cast<string>(result[i]));
            }
            for (int i = 0; i < methods.size(); i++)
            {
                if (find(non_listmethods.begin(), non_listmethods.end(), methods[i]) != non_listmethods.end())
                {
                    methods.erase(methods.begin() + i);
                }
            }
            for (int i = 0; i < methods.size(); i++)
            {
                cout << methods[i] << "    ";
                if(i%6==0 && i!=0){
                    cout << endl;
                }
                cout << endl;
            }
        }
        else
        {
            throw runtime_error("Error: el resultado no es un array.");
        }
    }

    void enviarArchivo(string path)
    {
        std::ifstream file(path, std::ios::binary);
        if (!file.is_open())
        {
            throw std::runtime_error("Error al abrir el archivo");
        }

        // Leer el archivo en un string
        std::ostringstream oss;
        oss << file.rdbuf();
        std::string fileContents = oss.str();

        // Crear un string para almacenar el resultado de la codificación
        std::string encoded;

        // Instanciar el codificador base64
        base64<> b64_encoder;

        // Usar "noline" para evitar saltos de línea en el resultado
        base64<>::noline noline;

        // Definir un estado (puedes definirlo como `int` e inicializarlo en 0)
        int state = 0;

        // Llamar al método `put` para realizar la codificación en base64
        b64_encoder.put(fileContents.begin(), fileContents.end(), std::back_inserter(encoded), state, noline);

        XmlRpcValue Args, result;
        Args[0] = token;
        Args[1] = encoded;
        if (client->execute("enviarArchivo", Args, result))
        {
            cout << static_cast<string>(result) << endl;
        }
        else
        {
            throw runtime_error("Error de Conexion");
        }
    }

    void do_quit()
    {
        exit(0);
    }
};

int main()
{
    CLI cli;
    cli.iniciar();
    return 0;
}