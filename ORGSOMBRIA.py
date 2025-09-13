import os
import time
import sys
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

ARQUIVO_TAREFAS = "tarefas_sombrias.txt"
ARQUIVO_LOG = "log_sombrio.log"


def carregar_tarefas():
    """Carrega as tarefas do arquivo de texto."""
    tarefas = []
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            for linha in f.readlines():
                partes = linha.strip().split("|")
                if len(partes) >= 3:
                    tarefa = {
                        "descricao": partes[0],
                        "status": partes[1],
                        "comentario": partes[2] if len(partes) > 2 else ""
                    }
                    tarefas.append(tarefa)
    return tarefas


def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo de texto."""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        for t in tarefas:
            f.write(f"{t['descricao']}|{t['status']}|{t['comentario']}\n")


def registrar_log(mensagem):
    """Registra uma mensagem no arquivo de log."""
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")


def exibir_cabecalho(titulo):
    """Exibe o cabeçalho do sistema."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + f"--- ORG SOMBRIA: {titulo} ---")
    print(COR_FUNDO + " " * 60)


def exibir_menu_principal():
    """Exibe o menu de navegação por abas."""
    exibir_cabecalho("Sistema de Controle Tático")
    print(COR_FUNDO + f"{'1. Missões Pendentes':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'2. Missões Concluídas':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'3. Registro de Atividades (Logs)':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'4. Resumo Geral':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'5. Adicionar Nova Missão':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + f"{'6. Sair para as sombras':<40} {COR_PRINCIPAL}|")
    print(COR_FUNDO + " " * 60)
    print(COR_FUNDO + "-----------------------------------------------------------------")


def visualizar_pendentes():
    """Exibe apenas as tarefas pendentes e permite interagir com elas."""
    exibir_cabecalho("Missões Pendentes")
    tarefas = carregar_tarefas()
    pendentes = [t for t in tarefas if t['status'] == 'pendente']

    if not pendentes:
        print(
            COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Todas as missões foram concluídas. Você é a vigilância de Gotham.")
    else:
        for i, t in enumerate(pendentes):
            comentario_texto = f"({t['comentario']})" if t['comentario'] else ""
            print(
                f"{COR_FUNDO}{COR_PRINCIPAL}{Style.BRIGHT}{i + 1}. {COR_STATUS_PENDENTE}{Style.BRIGHT}[PENDENTE]{Style.RESET_ALL} {COR_PRINCIPAL}{t['descricao']}{comentario_texto}")

    print("\n--- Opções ---")
    print("1. Concluir uma missão")
    print("2. Adicionar anotação")
    print("3. Voltar ao menu principal")

    escolha = input(COR_FUNDO + f"{COR_PRINCIPAL}Escolha sua ação: " + Style.RESET_ALL)
    if escolha == '1':
        marcar_tarefa_concluida(pendentes)
    elif escolha == '2':
        adicionar_comentario(pendentes)
    elif escolha == '3':
        return
    else:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Opção inválida.")

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def visualizar_concluidas():
    """Exibe apenas as tarefas concluídas, formatadas em blocos limpos com espaçamento."""
    exibir_cabecalho("Missões Concluídas")
    tarefas = carregar_tarefas()
    concluidas = [t for t in tarefas if t['status'] == 'concluida']

    if not concluidas:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Ainda não há missões concluídas.")
    else:
        for i, t in enumerate(concluidas):
            # Envoltura de texto para o comentário para que ele se ajuste
            wrapped_comentario = textwrap.wrap(t['comentario'], width=70) if t['comentario'] else []

            # Determinando a largura máxima para o alinhamento
            max_len = 70  # Definindo uma largura fixa para o bloco

            # Exibição do bloco formatado
            print(f"{COR_FUNDO}{COR_PRINCIPAL}{'=' * (max_len + 4)}")
            print(f"{COR_FUNDO}{COR_PRINCIPAL}  {COR_STATUS_CONCLUIDA}{Style.BRIGHT}[CONCLUÍDA]{Style.RESET_ALL}")
            print(f"{COR_FUNDO}{COR_PRINCIPAL}  {Style.BRIGHT}Missão {i + 1}:{Style.RESET_ALL} {t['descricao']}")

            if t['comentario']:
                print(f"{COR_FUNDO}{COR_PRINCIPAL}  {Style.BRIGHT}Observação:{Style.RESET_ALL}")
                for line in wrapped_comentario:
                    print(f"{COR_FUNDO}    {line}")

            print(f"{COR_FUNDO}{COR_PRINCIPAL}{'=' * (max_len + 4)}")
            print()  # Pula uma linha entre os blocos

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def exibir_log():
    """Exibe o log de atividades."""
    exibir_cabecalho("Registro de Atividades (Logs)")
    if os.path.exists(ARQUIVO_LOG):
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
            for linha in f.readlines():
                # Separa a data/hora da mensagem
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


def resumo_tarefas():
    """Exibe um resumo das missões."""
    exibir_cabecalho("Resumo Geral")
    tarefas = carregar_tarefas()
    total_tarefas = len(tarefas)
    concluidas = sum(1 for t in tarefas if t['status'] == 'concluida')
    pendentes = total_tarefas - concluidas

    print(COR_FUNDO + f"Total de missões rastreadas: {COR_PRINCIPAL}{Style.BRIGHT}{total_tarefas}")
    print(COR_FUNDO + f"Missões concluídas: {COR_STATUS_CONCLUIDA}{Style.BRIGHT}{concluidas}")
    print(COR_FUNDO + f"Missões pendentes: {COR_STATUS_PENDENTE}{Style.BRIGHT}{pendentes}")

    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def adicionar_tarefa():
    """Adiciona uma nova missão."""
    exibir_cabecalho("Adicionar Nova Missão")
    descricao = input(COR_FUNDO + f"{COR_PRINCIPAL}Digite a descrição da nova missão: " + Style.RESET_ALL)
    nova_tarefa = {
        "descricao": descricao,
        "status": "pendente",
        "comentario": ""
    }
    tarefas = carregar_tarefas()
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    registrar_log(f"Nova missão adicionada: '{descricao}'")
    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Missão adicionada com sucesso!")
    input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


def marcar_tarefa_concluida(lista_tarefas):
    """Marca uma missão como concluída."""
    if not lista_tarefas:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Nenhuma missão para concluir.")
        return

    try:
        indice_visual = int(input(COR_FUNDO + f"{COR_PRINCIPAL}Digite o número da missão que deseja concluir: ")) - 1
        if 0 <= indice_visual < len(lista_tarefas):
            descricao_tarefa = lista_tarefas[indice_visual]['descricao']

            tarefas_completas = carregar_tarefas()

            for t in tarefas_completas:
                if t['descricao'] == descricao_tarefa and t['status'] == 'pendente':
                    t['status'] = 'concluida'
                    comentario = input(
                        COR_FUNDO + f"{COR_PRINCIPAL}Deseja adicionar uma anotação? (Pressione Enter para pular): " + Style.RESET_ALL)
                    if comentario:
                        t['comentario'] = comentario
                    salvar_tarefas(tarefas_completas)
                    registrar_log(f"Missão concluída: '{descricao_tarefa}'. Anotação: '{comentario}'")
                    print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Missão concluída com sucesso!")
                    return
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Missão já concluída ou não encontrada.")
        else:
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Número de missão inválido.")
    except ValueError:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Entrada inválida. Por favor, digite um número.")


def adicionar_comentario(lista_tarefas):
    """Adiciona um comentário a uma missão."""
    if not lista_tarefas:
        print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Nenhuma missão para comentar.")
        return

    try:
        indice_visual = int(
            input(COR_FUNDO + f"{COR_PRINCIPAL}Digite o número da missão para adicionar uma anotação: ")) - 1
        if 0 <= indice_visual < len(lista_tarefas):
            descricao_tarefa = lista_tarefas[indice_visual]['descricao']

            tarefas_completas = carregar_tarefas()

            for t in tarefas_completas:
                if t['descricao'] == descricao_tarefa:
                    comentario = input(COR_FUNDO + f"{COR_PRINCIPAL}Digite sua anotação sombria: " + Style.RESET_ALL)
                    t['comentario'] = comentario
                    salvar_tarefas(tarefas_completas)
                    registrar_log(f"Anotação adicionada à missão '{descricao_tarefa}'")
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

        # Cria a barra de carregamento
        filled_chars = '█' * i
        empty_chars = ' ' * (total_steps - i)

        # Mensagens temáticas
        if progress_percent < 25:
            status_msg = "Sincronizando com a Batcaverna..."
        elif progress_percent < 50:
            status_msg = "Analisando dados de Gotham..."
        elif progress_percent < 75:
            status_msg = "Preparando traje tático..."
        else:
            status_msg = "Bat-Sistema online. Pronto para a ação."

        # Imprime a barra de progresso na mesma linha
        print(f"{COR_FUNDO}{COR_PRINCIPAL}\rCarregando: [{filled_chars}{empty_chars}] {progress_percent}% {status_msg}",
              end='')
        sys.stdout.flush()
        time.sleep(0.1)

    print()  # Nova linha após a conclusão do carregamento
    time.sleep(1) # Pausa breve para o usuário ver o "100%"
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Função principal que executa o programa."""
    loading_screen()
    while True:
        exibir_menu_principal()
        escolha = input(COR_FUNDO + f"{COR_PRINCIPAL}Escolha sua ação, Cavaleiro das Trevas: " + Style.RESET_ALL)

        if escolha == '1':
            visualizar_pendentes()
        elif escolha == '2':
            visualizar_concluidas()
        elif escolha == '3':
            exibir_log()
        elif escolha == '4':
            resumo_tarefas()
        elif escolha == '5':
            adicionar_tarefa()
        elif escolha == '6':
            print(COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Você está entrando nas sombras. Missão completa.")
            break
        else:
            print(
                COR_FUNDO + COR_PRINCIPAL + Style.BRIGHT + "Opção inválida. A cidade precisa de você. Tente novamente.")
            input(COR_FUNDO + f"{COR_PRINCIPAL}Pressione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()