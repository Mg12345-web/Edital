# app/processador.py
import pandas as pd
import asyncio
import os
import re
import fitz  # pymupdf
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
            with page.expect_download(timeout=10000) as download_info:
                await page.locator('button:below(:text("Consultar"))').nth(0).click()
            download = await download_info.value
            nome_pdf = f"{placa}_{ait}.pdf"
            caminho_pdf = os.path.join("static", nome_pdf)
            await download.save_as(caminho_pdf)
            cpf = extrair_cpf_pdf(caminho_pdf)
            return cpf
        except:
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
        print("Erro ao ler PDF:", e)
    return "CPF não encontrado"

async def processar_planilha(caminho_planilha):
    df = pd.read_excel(caminho_planilha)
    resultados = []

    for index, row in df.iterrows():
        placa = str(row['placa']).strip()
        ait = str(row['ait']).strip()
        print(f"🔍 Processando: {placa} / {ait}")
        cpf = await consultar_e_extrair_cpf(placa, ait)
        resultados.append({
            "placa": placa,
            "ait": ait,
            "cpf": cpf
        })

    df_resultado = pd.DataFrame(resultados)
    nome_saida = "resultado.xlsx"
    caminho_saida = os.path.join("static", nome_saida)
    df_resultado.to_excel(caminho_saida, index=False)

    return nome_saida
