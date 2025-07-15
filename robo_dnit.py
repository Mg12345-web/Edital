import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from slack_alerta import enviar_mensagem_slack

URL = "https://servicos.dnit.gov.br/multas/informacoes/editais-publicacao-notificacao?ano=2025"
TIPOS_INTERESSANTES = ["Notificação da Autuação", "Notificação da Penalidade"]
DATA_HOJE = datetime.now().strftime("%d/%m/%Y")

async def verificar_editais_dnit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, timeout=60000)
        await page.wait_for_selector("tbody tr", timeout=60000)

        await page.wait_for_selector("tbody tr")

        linhas = await page.query_selector_all("tbody tr")
        achou_edital = False

        for linha in linhas:
            texto_linha = await linha.inner_text()
            if any(tipo in texto_linha for tipo in TIPOS_INTERESSANTES) and DATA_HOJE in texto_linha:
                achou_edital = True
                msg = f"\ud83d\udce2 Novo edital encontrado no DNIT ({DATA_HOJE}):\n{texto_linha}"
                enviar_mensagem_slack(msg)

        if not achou_edital:
            print("Nenhum edital novo encontrado hoje.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verificar_editais_dnit())
