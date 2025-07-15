import requests
from bs4 import BeautifulSoup
from datetime import datetime
from slack_alerta import enviar_mensagem_slack

URL = "https://servicos.dnit.gov.br/multas/informacoes/editais-publicacao-notificacao?ano=2025"
TIPOS_INTERESSANTES = ["Notificação da Autuação", "Notificação da Penalidade"]
DATA_HOJE = datetime.now().strftime("%d/%m/%Y")

def verificar_editais_dnit():
    print("🔍 Iniciando verificação de editais do DNIT...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=60)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        linhas = soup.select("tbody tr")
        achou_edital = False

        for linha in linhas:
            colunas = linha.find_all("td")
            if len(colunas) < 3:
                continue

            numero_edital = colunas[0].get_text(strip=True)
            tipo = colunas[1].get_text(strip=True)
            data = colunas[2].get_text(strip=True)

            if tipo in TIPOS_INTERESSANTES and data == DATA_HOJE:
                achou_edital = True
                msg = f"📢 *Novo edital encontrado no DNIT* ({DATA_HOJE}):\n- Nº: {numero_edital}\n- Tipo: {tipo}\n- Data: {data}"
                print(msg)
                enviar_mensagem_slack(msg)

        if not achou_edital:
            print(f"Nenhum edital novo encontrado para a data {DATA_HOJE}.")

    except Exception as e:
        print(f"❌ Erro ao executar o robô: {e}")

    print("✅ Verificação concluída.")

if __name__ == "__main__":
    verificar_editais_dnit()
