import http.server
import socketserver
import webbrowser
import datetime

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def start_server():
    Handler.extensions_map['.css'] = 'text/css'
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servindo em http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

def inicio_interativo():
    nome = input("Olá! Qual é o seu nome? ")
    print(f"Olá, {nome}! Bem-vindo ao seu diário interativo.")
    start_server()

def exibir_calendario_e_horas():
    agora = datetime.datetime.now()
    print("Calendário e Horas em Tempo Real:")
    print(agora.strftime("Data: %Y-%m-%d"))
    print(agora.strftime("Horas: %H:%M:%S"))

def escrever_diario():
    data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"diario_{data_hoje}.txt", "a") as arquivo:
        entrada = input("Como foi o seu dia? Escreva aqui: ")
        arquivo.write(f"Data: {data_hoje}\n")
        arquivo.write(f"Entrada do dia: {entrada}\n\n")
    print("Seu diário foi atualizado com sucesso!")

def main():
    inicio_interativo()
    while True:
        exibir_calendario_e_horas()
        print("\nO que você gostaria de fazer?")
        print("1. Escrever no diário")
        print("2. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            escrever_diario()
        elif escolha == "2":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    main()

