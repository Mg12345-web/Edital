# app/processador.py
import pandas as pd
import asyncio
import os
import re
import fitz  # PyMuPDF
from playwright.async_api import async_playwright
from app.utils import formatar_cpf


async def consultar_e_extrair_cpf(placa, ait):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto("https://portal.der.mg.gov.br/obras-multas-frontend/#/consulta-autos")
        await page.wait_for_timeout(2000)

        await page.locator('input[name="placa"]').fill(placa)
        await page.locator('input[name="nrAuto"]').fill(ait)
        await page.get_by_role("button", name="Consultar").click()
        await page.wait_for_timeout(5000)

        try:
            async with page.expect_download(timeout=20000) as download_info:
            await page.get_by_role("button", name="").click()
            download = await download_info.value
            nome_pdf = f"{placa}_{ait}.pdf"
            caminho_pdf = os.path.join("app", "static", nome_pdf)
            await download.save_as(caminho_pdf)
            cpf = extrair_cpf_pdf(caminho_pdf)
            return cpf
        except Exception as e:
            print(f"⚠️ Erro ao baixar PDF para {placa}/{ait}: {e}")
            return "PDF não encontrado"


def extrair_cpf_pdf(caminho):
    try:
        with fitz.open(caminho) as doc:
            for pagina in doc:
                texto = pagina.get_text()
                numeros = re.findall(r'\b\d{8,11}\b', texto)
                for n in numeros:
                    if len(n) <= 11:
                        return formatar_cpf(n)
    except Exception as e:
        print("⚠️ Erro ao ler PDF:", e)
    return "CPF não encontrado"


async def processar_planilha(caminho_planilha):
    df = pd.read_excel(caminho_planilha)

    # Flexibiliza nomes de colunas
    colunas = [c.strip().lower() for c in df.columns]
    mapa_colunas = {
        'placa': ['placa', 'placa do veículo', 'nº da placa', 'placa veiculo'],
        'ait': ['ait', 'auto', 'auto de infração', 'nº do auto']
    }

    def encontrar_coluna(possibilidades):
        for nome in possibilidades:
            for col in colunas:
                if nome in col:
                    return df.columns[colunas.index(col)]
        return None

    col_placa = encontrar_coluna(mapa_colunas['placa'])
    col_ait = encontrar_coluna(mapa_colunas['ait'])

    if not col_placa or not col_ait:
        raise Exception("❌ Não foi possível identificar as colunas de PLACA e/ou AIT.")

    resultados = []

    for _, row in df.iterrows():
        placa = str(row[col_placa]).strip()
        ait = str(row[col_ait]).strip()
        print(f"🔍 Processando: {placa} / {ait}")
        cpf = await consultar_e_extrair_cpf(placa, ait)
        resultados.append({
            "placa": placa,
            "ait": ait,
            "cpf": cpf
        })

    df_resultado = pd.DataFrame(resultados)
    nome_saida = "resultado.xlsx"
    caminho_saida = os.path.join("app", "static", nome_saida)
    df_resultado.to_excel(caminho_saida, index=False)

    return nome_saida
