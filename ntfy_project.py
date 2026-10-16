
import requests
import time
import json
import subprocess
import logging

from pathlib import Path


# CONFIGURAÇÕES


PASTA_BASE = Path.home() / "Documents" / "VSCode"
PASTA_ARQUIVOS = PASTA_BASE / "Novos_Arquivos"

ARQUIVO_LOG = PASTA_BASE / "programa.log"
ARQUIVO_TEXTO = PASTA_ARQUIVOS / "Arquivo_de_Texto.txt"

# Configure estas variáveis antes de executar.
# Não publique credenciais reais no GitHub.
TOPICO_NTFY = "SEU_TOPICO_NOVO"
SENHA = "ALTERE_ESTA_SENHA"

URL_LEITURA = f"https://ntfy.sh/{TOPICO_NTFY}/json"
URL_RESPOSTA = f"https://ntfy.sh/{TOPICO_NTFY}"

INTERVALO = 900  # 15 minutos

PROGRAMAS = {
    "calculadora": Path(
        r"C:\Windows\System32\calc.exe"
    ),
    "paint": Path(
        r"C:\Windows\System32\mspaint.exe"
    ),
}


# CONFIGURAÇÃO INICIAL


def configurar_logging():
    """Configura os registros e cria as pastas necessárias."""

    PASTA_BASE.mkdir(parents=True, exist_ok=True)
    PASTA_ARQUIVOS.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=ARQUIVO_LOG,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logging.info("Programa iniciado!")


# COMUNICAÇÃO COM O NTFY


def buscar_notificacoes():
    """Consulta o ntfy e retorna as notificações recebidas."""

    try:
        resposta = requests.get(
            URL_LEITURA,
            params={
                "poll": "1",
                "since": "15m"
            },
            timeout=10
        )

        resposta.raise_for_status()

    except requests.exceptions.RequestException as erro:
        logging.error("Erro ao consultar o ntfy: %s", erro)
        return []

    notificacoes = []

    for linha in resposta.text.splitlines():
        try:
            notificacao = json.loads(linha)

            # Ignora notificações sem o campo esperado.
            if isinstance(notificacao, dict):
                if isinstance(notificacao.get("message"), str):
                    notificacoes.append(notificacao)

        except json.JSONDecodeError as erro:
            logging.error("Erro ao interpretar JSON: %s", erro)

    return notificacoes


def enviar_resposta(mensagem):
    """Envia uma mensagem de resposta pelo ntfy."""

    try:
        resposta = requests.post(
            URL_RESPOSTA,
            data=mensagem.encode("utf-8"),
            timeout=10
        )

        resposta.raise_for_status()

    except requests.exceptions.RequestException as erro:
        logging.error("Erro ao enviar resposta ao ntfy: %s", erro)


# VALIDAÇÃO DAS MENSAGENS

def validar_comando(notificacoes):
    """
    Espera duas mensagens:
    1. Uma mensagem contendo a senha após ':'
    2. Uma mensagem contendo o nome do programa.

    Retorna o nome do programa autorizado ou None.
    """

    mensagens = [
        notificacao["message"]
        for notificacao in notificacoes
    ]

    if len(mensagens) < 2:
        logging.warning("Quantidade insuficiente de mensagens.")
        return None

    mensagem_senha = mensagens[-2]
    mensagem_programa = mensagens[-1].strip().lower()

    if ":" not in mensagem_senha:
        logging.warning("Formato inválido para a mensagem de senha.")
        return None

    senha_recebida = mensagem_senha.split(":", 1)[1].strip()

    if senha_recebida != SENHA:
        logging.warning("Senha incorreta.")
        enviar_resposta("Senha incorreta.")
        return None

    logging.info(
        "Mensagens recebidas: %s",
        mensagens[-2:]
    )

    return mensagem_programa


# MANIPULAÇÃO DE ARQUIVOS

def salvar_mensagens(notificacoes):
    """Salva as mensagens recebidas em um arquivo de texto."""

    mensagens = [
        notificacao["message"]
        for notificacao in notificacoes
    ]

    try:
        with ARQUIVO_TEXTO.open("w", encoding="utf-8") as arquivo:
            for mensagem in mensagens:
                arquivo.write(mensagem + "\n")

        logging.info("Mensagens salvas em arquivo.")

    except OSError as erro:
        logging.error("Erro ao salvar as mensagens: %s", erro)


# EXECUÇÃO DE PROGRAMAS


def executar_programa(nome_programa):
    """Executa somente os programas definidos na lista permitida."""

    programa = PROGRAMAS.get(nome_programa)

    if programa is None:
        logging.warning("Programa não autorizado ou inexistente: %s",
                        nome_programa)

        enviar_resposta(
            "Nome de aplicativo inválido ou função inexistente."
        )
        return

    try:
        logging.info("Executando programa: %s", nome_programa)

        subprocess.Popen([str(programa)])

        enviar_resposta(
            f"Comando recebido. Abrindo {nome_programa}."
        )

    except OSError as erro:
        logging.error("Erro ao abrir o programa: %s", erro)
        enviar_resposta("Não foi possível abrir o aplicativo.")


# FLUXO PRINCIPAL


def main():
    """Coordena o funcionamento da automação."""

    configurar_logging()

    while True:
        logging.info("Verificando novas mensagens.")

        notificacoes = buscar_notificacoes()

        if len(notificacoes) < 2:
            logging.warning("Entradas não suficientes.")

        else:
            salvar_mensagens(notificacoes)

            programa = validar_comando(notificacoes)

            if programa is not None:
                executar_programa(programa)

        time.sleep(INTERVALO)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        logging.info("Programa encerrado pelo usuário.")
        print("Programa encerrado.")
