import http.se import datetime

class User:
    def __init__(self):
        self.level = 0
        self.experience = 0
        self.physical = 0
        self.intelligence = 0
        self.music = 0
        self.daily_quests = {
            "Estudar 2 horas": {"experience": 50, "attribute": "intelligence"},
            "Treinar 1 hora": {"experience": 30, "attribute": "physical"},
            "Ler por 15 minutos": {"experience": 20, "attribute": "intelligence"},
            "Tocar o instrumento": {"experience": 40, "attribute": "music"}
        }
        self.monthly_goals = {
            "Bater a meta de ter pelo menos produtividade de 60% do mês": {"attribute": "intelligence", "target": 60},
            "Ter conseguido ficar satisfeito comigo mesmo": {"attribute": "physical", "target": 1},
            "Voltar a estudar e tocar o trombone": {"attribute": "intelligence", "target": 1},
            "Ser feliz": {"attribute": "music", "target": 1}
        }
        self.start_date = datetime.datetime.now()

    def complete_quest(self, quest):
        quest_data = self.daily_quests.get(quest)
        if quest_data:
            self.experience += quest_data["experience"]
            setattr(self, quest_data["attribute"], getattr(self, quest_data["attribute"]) + 1)
            self.level = self.experience // 100

    def calculate_daily_progress(self):
        total_quests = len(self.daily_quests)
        completed_quests = sum(1 for quest in self.daily_quests if getattr(self, quest["attribute"]) > 0)
        return (completed_quests / total_quests) * 100 if total_quests > 0 else 0

    def check_monthly_goals(self):
        for goal, data in self.monthly_goals.items():
            if getattr(self, data["attribute"]) >= data["target"]:
                print(f"Você alcançou a meta do mês: {goal}")

# Exemplo de uso:
user = User()
user.complete_quest("Estudar 2 horas")
user.complete_quest("Treinar 1 hora")
user.complete_quest("Ler por 15 minutos")
user.complete_quest("Tocar o instrumento")

daily_progress = user.calculate_daily_progress()
print(f"Porcentagem de conclusão das quests diárias: {daily_progress}%")
user.check_monthly_goals()

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

