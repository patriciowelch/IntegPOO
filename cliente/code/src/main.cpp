#include <iostream>
#include <string>
#include <sstream>

using namespace std;

class CLI {
public:
    CLI(){
        cout << "Hola mundo\n";
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
    std::string prompt;

    void procesarComando(const string &linea) {
        istringstream stream(linea);
        string comando;
        stream >> comando;
        if (comando == "quit") {
            do_quit();
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