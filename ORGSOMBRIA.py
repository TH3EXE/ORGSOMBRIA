import os
import time
import sys
import random
from datetime import datetime
from colorama import Fore, Style, init
import textwrap

# Inicializa o colorama
init(autoreset=True)

# Cores e estilos do Batman
COR_PRINCIPAL = Fore.YELLOW
COR_FUNDO = Fore.BLACK + Style.BRIGHT
COR_STATUS_CONCLUIDA = Fore.GREEN
COR_STATUS_PENDENTE = Fore.RED

ARQUIVO_TAREFAS = "missao_rpg.txt"
ARQUIVO_LOG = "log_sombrio.log"
ARQUIVO_PERSONAGEM = "personagem.txt"

# Dificuldades e XP associado
DIFICULDADES = {
    "facil": 20,
    "medio": 50,
    "dificil": 100
}

# Classes e nomes dos níveis
CLASSES_RPG = {
    "Vigilante Noturno": ["Novato da Noite", "Vigilante das Ruas", "Guardião de Gotham", "Lobo Solitário",
                          "Cavaleiro das Trevas"],
    "Assassino das Sombras": ["Recruta Silencioso", "Sombra Veloz", "Lâmina Oculta", "Ceifador", "Senhor das Sombras"],
    "Mago das Trevas": ["Aprendiz Amaldiçoado", "Conjurador de Trovoadas", "Arcanista da Morte", "Feiticeiro",
                        "Lorde da Ruína"]
}


class Personagem:
    """Armazena os dados do personagem do jogador."""

    def __init__(self, nome, classe, xp=0, nivel=0):
        self.nome = nome
        self.classe = classe
        self.xp = xp
        self.nivel = nivel

    def ganhar_xp(self, valor_xp):
        self.xp += valor_xp
        self.verificar_nivel()

    def verificar_nivel(self):
        while self.xp >= 100:
            self.xp -= 100
            self.nivel += 1
            registrar_log(f"{self.nome} subiu para o Nível {self.nivel} como {self.nome_nivel()}")
            self.salvar()

    def nome_nivel(self):
        if self.nivel < len(CLASSES_RPG[self.classe]):
            return CLASSES_RPG[self.classe][self.nivel]
        else:
            return f"Lenda {self.classe}"

    def to_line(self):
        return f"{self.nome}|{self.classe}|{self.xp}|{self.nivel}\n"

    def salvar(self):
        with open(ARQUIVO_PERSONAGEM, "w", encoding="utf-8") as f:
            f.write(self.to_line())

    @staticmethod
    def carregar():
        if os.path.exists(ARQUIVO_PERSONAGEM):
            with open(ARQUIVO_PERSONAGEM, "r", encoding="utf-8") as f:
                linha = f.readline().strip().split("|")
                if len(linha) == 4:
                    return Personagem(linha[0], linha[1], int(linha[2]), int(linha[3]))
        return None


def criar_personagem():
    """Cria um novo personagem e salva os dados."""
    exibir_cabecalho("Criar Novo Personagem")
    print(COR_FUNDO + f"{COR_PRINCIPAL}Bem-vindo, novo aventureiro das sombras.")
    nome = input(COR_FUNDO + f"{COR_PRINCIPAL}Qual o seu nome de guerra?: " + Style.RESET_ALL)
    print("\nEscolha sua classe:")
    for i, classe in enumerate(CLASSES_RPG.keys()):
        print(f"  {i + 1}. {classe}")

    while True:
        try:
            escolha = int(input(COR_FUNDO + f"{COR_PRINCIPAL}Sua escolha: " + Style.RESET_ALL))
            classes = list(CLASSES_RPG.keys())
            if 0 < escolha <= len(classes):
                classe_escolhida = classes[escolha - 1]
                break
            else:
                print(COR_FUNDO + "Opção inválida.")
        except ValueError:
            print(COR_FUNDO + "Entrada inválida. Digite um número.")

    personagem = Personagem(nome, classe_escolhida)
    personagem.salvar()
    registrar_log(f"Personagem criado: {nome} da classe {classe_escolhida}")
    print(COR_FUNDO + COR_PRINCIPAL + "Personagem criado com sucesso!")
    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para iniciar sua jornada..." + Style.RESET_ALL)
    return personagem


class Missao:
    """Representa uma missão do Cavaleiro das Trevas."""

    def __init__(self, descricao, dificuldade, status="pendente", comentario=""):
        self.descricao = descricao
        self.dificuldade = dificuldade
        self.status = status
        self.comentario = comentario

    def to_line(self):
        """Converte o objeto da missão para uma linha de texto para o arquivo."""
        return f"{self.descricao}|{self.dificuldade}|{self.status}|{self.comentario}\n"


def carregar_tarefas():
    """Carrega as tarefas do arquivo de texto, convertendo para objetos Missao."""
    tarefas = []
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            for linha in f.readlines():
                partes = linha.strip().split("|")
                if len(partes) >= 4:
                    tarefa = Missao(
                        descricao=partes[0],
                        dificuldade=partes[1],
                        status=partes[2],
                        comentario=partes[3]
                    )
                    tarefas.append(tarefa)
    return tarefas


def salvar_tarefas(tarefas):
    """Salva a lista de objetos Missao no arquivo de texto."""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        for t in tarefas:
            f.write(t.to_line())


def registrar_log(mensagem):
    """Registra uma mensagem no arquivo de log."""
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")


def exibir_cabecalho(titulo):
    """Exibe o cabeçalho do sistema."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + f"--- ORG SOMBRIA: {titulo} ---")
    print(COR_FUNDO + " " * 60)


def exibir_menu_principal(personagem):
    """Exibe o menu de navegação por abas com informações do personagem."""
    exibir_cabecalho("Sistema de Controle Tático")
    print(COR_FUNDO + Style.BRIGHT + f"--- Dados do Personagem ---")
    print(COR_FUNDO + f"Nome: {personagem.nome}")
    print(COR_FUNDO + f"Classe: {personagem.classe}")
    print(COR_FUNDO + f"Nível: {personagem.nivel} ({personagem.nome_nivel()})")
    print(COR_FUNDO + f"XP: {personagem.xp}/100")
    print(COR_FUNDO + "---------------------------")
    print(COR_FUNDO + f"{'1. Missões Pendentes':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'2. Missões Concluídas':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'3. Registro de Atividades (Logs)':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'4. Adicionar Nova Missão':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'5. Sair para as sombras':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + " " * 60)
    print(COR_FUNDO + "-----------------------------------------------------------------")


def visualizar_pendentes(personagem):
    """Exibe apenas as tarefas pendentes e permite interagir com elas."""
    exibir_cabecalho("Missões Pendentes")
    tarefas = carregar_tarefas()
    pendentes = [t for t in tarefas if t.status == 'pendente']

    if not pendentes:
        print(
            COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Todas as missões foram concluídas. Você é a vigilância de Gotham.")
    else:
        for i, t in enumerate(pendentes):
            comentario_texto = f"({t.comentario})" if t.comentario else ""
            print(
                f"{COR_FUNDO}{COR_PRINCIPAL}{Style.BRIGHT}{i + 1}. {COR_STATUS_PENDENTE}{Style.BRIGHT}[PENDENTE]{Style.RESET_ALL} ({t.dificuldade.upper()}) {COR_PRINCIPAL}{t.descricao}{comentario_texto}")

    print("\n--- Opções ---")
    print("1. Concluir uma missão")
    print("2. Adicionar anotação")
    print("3. Voltar ao menu principal")

    escolha = input(COR_FUNDO + f"{COR_PRINCIPAL}Escolha sua ação: " + Style.RESET_ALL)
    if escolha == '1':
        marcar_tarefa_concluida(pendentes, tarefas, personagem)
    elif escolha == '2':
        adicionar_comentario(pendentes, tarefas)
    elif escolha == '3':
        return
    else:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Opção inválida.")

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def visualizar_concluidas():
    """Exibe apenas as tarefas concluídas, formatadas em blocos limpos com espaçamento."""
    exibir_cabecalho("Missões Concluídas")
    tarefas = carregar_tarefas()
    concluidas = [t for t in tarefas if t.status == 'concluida']

    if not concluidas:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Ainda não há missões concluídas.")
    else:
        for i, t in enumerate(concluidas):
            wrapped_comentario = textwrap.wrap(t.comentario, width=70) if t.comentario else []
            max_len = 70

            print(f"{COR_FUNDO}{COR_PRINCIPAL}{'=' * (max_len + 4)}")
            print(f"{COR_FUNDO}{COR_PRINCIPAL}  {COR_STATUS_CONCLUIDA}{Style.BRIGHT}[CONCLUÍDA]{Style.RESET_ALL}")
            print(f"{COR_FUNDO}{COR_PRINCIPAL}  {Style.BRIGHT}Missão {i + 1}:{Style.RESET_ALL} {t.descricao}")
            print(f"{COR_FUNDO}{COR_PRINCIPAL}  {Style.BRIGHT}Dificuldade:{Style.RESET_ALL} {t.dificuldade.upper()}")

            if t.comentario:
                print(f"{COR_FUNDO}{COR_PRINCIPAL}  {Style.BRIGHT}Observação:{Style.RESET_ALL}")
                for line in wrapped_comentario:
                    print(f"{COR_FUNDO}    {line}")

            print(f"{COR_FUNDO}{COR_PRINCIPAL}{'=' * (max_len + 4)}")
            print()

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def exibir_log():
    """Exibe o log de atividades."""
    exibir_cabecalho("Registro de Atividades (Logs)")
    if os.path.exists(ARQUIVO_LOG):
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
            for linha in f.readlines():
                partes = linha.split("] ", 1)
                if len(partes) > 1:
                    data_hora = partes[0] + "]"
                    mensagem = partes[1]
                    print(f"{COR_FUNDO}{COR_PRINCIPAL}{Style.BRIGHT}{data_hora}{Style.RESET_ALL}{COR_FUNDO} {mensagem}")
                else:
                    print(COR_FUNDO + linha)
    else:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Nenhum registro de atividades encontrado.")

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def adicionar_tarefa():
    """Adiciona uma nova missão."""
    exibir_cabecalho("Adicionar Nova Missão")
    descricao = input(COR_FUNDO + f"{COR_PRINCIPAL}Digite a descrição da nova missão: " + Style.RESET_ALL)
    print("\nEscolha a dificuldade:")
    for i, dif in enumerate(DIFICULDADES.keys()):
        print(f"  {i + 1}. {dif.capitalize()}")

    while True:
        try:
            escolha = int(input(COR_FUNDO + f"{COR_PRINCIPAL}Sua escolha: " + Style.RESET_ALL))
            dificuldades = list(DIFICULDADES.keys())
            if 0 < escolha <= len(dificuldades):
                dificuldade_escolhida = dificuldades[escolha - 1]
                break
            else:
                print(COR_FUNDO + "Opção inválida.")
        except ValueError:
            print(COR_FUNDO + "Entrada inválida. Digite um número.")

    nova_tarefa = Missao(descricao, dificuldade_escolhida)
    tarefas = carregar_tarefas()
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    registrar_log(f"Nova missão adicionada: '{descricao}' ({dificuldade_escolhida})")
    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Missão adicionada com sucesso!")
    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def marcar_tarefa_concluida(lista_tarefas_pendentes, lista_completa_tarefas, personagem):
    """Marca uma missão como concluída e recompensa o jogador com XP."""
    if not lista_tarefas_pendentes:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Nenhuma missão para concluir.")
        return

    try:
        indice_visual = int(input(COR_FUNDO + f"{COR_PRINCIPAL}Digite o número da missão que deseja concluir: ")) - 1
        if 0 <= indice_visual < len(lista_tarefas_pendentes):
            tarefa_selecionada = lista_tarefas_pendentes[indice_visual]

            # Atualiza a tarefa na lista completa
            for t in lista_completa_tarefas:
                if t.descricao == tarefa_selecionada.descricao and t.status == 'pendente':
                    t.status = 'concluida'
                    comentario = input(
                        COR_FUNDO + f"{COR_PRINCIPAL}Deseja adicionar uma anotação? (Pressione Enter para pular): " + Style.RESET_ALL)
                    if comentario:
                        t.comentario = comentario

                    # Concede XP ao personagem
                    xp_ganho = DIFICULDADES[t.dificuldade]
                    personagem.ganhar_xp(xp_ganho)

                    salvar_tarefas(lista_completa_tarefas)
                    registrar_log(f"Missão concluída: '{t.descricao}'. XP ganho: {xp_ganho}. Anotação: '{comentario}'")

                    print(
                        COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + f"\nMissão concluída com sucesso! Você ganhou {xp_ganho} XP.")
                    print(
                        COR_FUNDO + f"Seu novo XP é {personagem.xp} e seu nível é {personagem.nivel} ({personagem.nome_nivel()}).")
                    return

            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Missão já concluída ou não encontrada.")
        else:
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Número de missão inválido.")
    except ValueError:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Entrada inválida. Por favor, digite um número.")


def adicionar_comentario(lista_tarefas_pendentes, lista_completa_tarefas):
    """Adiciona um comentário a uma missão."""
    if not lista_tarefas_pendentes:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Nenhuma missão para comentar.")
        return

    try:
        indice_visual = int(
            input(COR_FUNDO + f"{COR_PRINCIPAL}Digite o número da missão para adicionar uma anotação: ")) - 1
        if 0 <= indice_visual < len(lista_tarefas_pendentes):
            tarefa_selecionada = lista_tarefas_pendentes[indice_visual]
            comentario = input(COR_FUNDO + f"{COR_PRINCIPAL}Digite sua anotação sombria: " + Style.RESET_ALL)

            for t in lista_completa_tarefas:
                if t.descricao == tarefa_selecionada.descricao:
                    t.comentario = comentario
                    salvar_tarefas(lista_completa_tarefas)
                    registrar_log(f"Anotação adicionada à missão '{t.descricao}'")
                    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Anotação adicionada com sucesso!")
                    return
        else:
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Número de missão inválido.")
    except ValueError:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Entrada inválida. Por favor, digite um número.")


def loading_screen():
    """Exibe uma tela de carregamento animada com o tema do Batman."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "--- ORG SOMBRIA: INICIANDO O SISTEMA ---" + Style.RESET_ALL)

    total_steps = 20
    for i in range(total_steps + 1):
        progress_percent = int((i / total_steps) * 100)

        filled_chars = '█' * i
        empty_chars = ' ' * (total_steps - i)

        if progress_percent < 25:
            status_msg = "Sincronizando com a Batcaverna..."
        elif progress_percent < 50:
            status_msg = "Analisando dados de Gotham..."
        elif progress_percent < 75:
            status_msg = "Preparando traje tático..."
        else:
            status_msg = "Bat-Sistema online. Pronto para a ação."

        print(f"{COR_FUNDO}{COR_PRINCIPAL}\rCarregando: [{filled_chars}{empty_chars}] {progress_percent}% {status_msg}",
              end='')
        sys.stdout.flush()
        time.sleep(0.1)

    print()
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Função principal que executa o programa."""
    loading_screen()
    personagem = Personagem.carregar()
    if not personagem:
        personagem = criar_personagem()

    while True:
        exibir_menu_principal(personagem)
        escolha = input(COR_FUNDO + f"{COR_PRINCIPAL}Escolha sua ação, Cavaleiro das Trevas: " + Style.RESET_ALL)

        if escolha == '1':
            visualizar_pendentes(personagem)
        elif escolha == '2':
            visualizar_concluidas()
        elif escolha == '3':
            exibir_log()
        elif escolha == '4':
            adicionar_tarefa()
        elif escolha == '5':
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Você está entrando nas sombras. Missão completa.")
            break
        else:
            print(
                COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Opção inválida. A cidade precisa de você. Tente novamente.")
            input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()