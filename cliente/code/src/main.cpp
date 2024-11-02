#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include "XmlRpc.h"

using namespace XmlRpc;
using namespace std;

class CLI {
public:
    CLI(){
        cout << "Bienvenido Cliente\n";
        prompt = ">>> ";
    }

    void iniciar() {
        string linea;
        while (true) {
            cout << prompt;
            getline(cin, linea);
            procesarComando(linea);
        }
    }

private:
    string prompt;
    string token = "";
    string usuario;
    string password;
    string host;
    int port;
    XmlRpcClient client = XmlRpcClient("localhost", 8080);
    vector<string> methods;

    void procesarComando(const string &linea) {
        istringstream stream(linea);
        string comando;
        stream >> comando;
        vector<string> args= {};
        string arg;
        while (stream >> arg) {
            args.push_back(arg);
        }
        if (comando == "quit") {
            do_quit();
        } else if(comando == "conectar"){
            do_conectar();
        } else if(comando == "listarMetodos"){
            do_listarMetodos();
        } else if(find(methods.begin(), methods.end(), comando) != methods.end()){
            XmlRpcValue Args, result;
            Args[0] = token;
            for (int i = 0; i < args.size(); i++) {
                Args[i + 1] = args[i];
            }
            try {
                client.execute(comando.c_str(), Args, result);
                cout << static_cast<string>(result) << endl;
            } catch (XmlRpcException &e) {
                cout << "Error: " << e.getMessage() << endl;
            }        
        } else {
            cout << "Comando no reconocido" << endl;
        }
    }

    void do_login(){
        cout << "Usuario: ";
        getline(cin, usuario);
        cout << "Password: ";
        getline(cin, password);
    }

    void do_setServer(){
        cout << "Host: ";
        getline(cin, host);
        cout << "Port: ";
        cin >> port;
        cin.ignore();
    }

    void do_conectar() {
        do_login();
        do_setServer();
        client = XmlRpcClient(host.c_str(), port);
        XmlRpcValue Args, result;
        cout << "Connected to " << host << endl;
        // args deberia contener el usuario y la contraseña
        Args[0] = usuario;
        Args[1] = password;

        // Ejecutar el método listarMetodos
        try {
            client.execute("iniciar_sesion", Args, result);
            token = static_cast<string>(result);
            //si token no contiene '401:' entonces se ha logrado la conexión
            if(token.find("401:") == string::npos){
                cout << "Conexion exitosa" << endl;
                do_listarMetodos();
            } else {
                cout << token << endl;
                token = "";
            }
        } catch (XmlRpcException &e) {
            cout << "Error: " << e.getMessage() << endl;
        }
    }

    void do_listarMetodos() {
        XmlRpcValue result;
        XmlRpcValue args;
        args[0]=this->token;
        methods.clear();
        vector<string> non_listmethods;
        non_listmethods.push_back("iniciar_sesion");
        try {
            // Ejecutar el método "listarMetodos" sin argumentos
            client.execute("listarMetodos", args, result);
            // Convertir el resultado a vector de XmlRpcValue y mostrar cada método
            if (result.getType() == XmlRpcValue::TypeArray) {
                cout << "\nMethods:\n";
                for (int i = 0; i < result.size(); i++) {
                    methods.push_back(static_cast<string>(result[i]));
                }
                for (int i = 0; i < methods.size(); i++) {
                    if(find(non_listmethods.begin(), non_listmethods.end(), methods[i]) != non_listmethods.end()){
                        methods.erase(methods.begin() + i);
                    }
                }
                for (int i = 0; i < methods.size(); i++) {
                    cout << methods[i] << endl;
                }
            } else {
                cout << "Error: el resultado no es un array." << endl;
            }
        } catch (XmlRpcException &e) {
            cout << "Error: " << e.getMessage() << endl;
        }
    }

    void do_quit() {
        exit(0);
    }
};

int main() {
    CLI cli;
    cli.iniciar();
    return 0;
}