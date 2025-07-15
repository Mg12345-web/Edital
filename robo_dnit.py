import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from slack_alerta import enviar_mensagem_slack

URL = "https://servicos.dnit.gov.br/multas/informacoes/editais-publicacao-notificacao?ano=2025"
TIPOS_INTERESSANTES = ["Notificação da Autuação", "Notificação da Penalidade"]
DATA_HOJE = datetime.now().strftime("%d/%m/%Y")

async def verificar_editais_dnit():
    print("🔍 Iniciando verificação de editais do DNIT...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(URL, timeout=60000)
            await page.wait_for_selector("tbody tr", timeout=60000)

            linhas = await page.query_selector_all("tbody tr")
            achou_edital = False

            for linha in linhas:
                texto_linha = await linha.inner_text()
                if any(tipo in texto_linha for tipo in TIPOS_INTERESSANTES) and DATA_HOJE in texto_linha:
                    achou_edital = True
                    msg = f"📢 *Novo edital encontrado no DNIT* ({DATA_HOJE}):\n```\n{texto_linha}\n```"
                    print(msg)
                    enviar_mensagem_slack(msg)

            if not achou_edital:
                print(f"Nenhum edital novo encontrado para a data {DATA_HOJE}.")

            await browser.close()

    except Exception as e:
        print(f"❌ Erro ao executar o robô: {e}")

    print("✅ Verificação concluída.")

if __name__ == "__main__":
    asyncio.run(verificar_editais_dnit())
