# app/utils.py
import re

def formatar_cpf(cpf_raw):
    """
    Formata um número de CPF, mesmo que venha com menos de 11 dígitos.
    Ex: '2187146618' => '021.871.466-18'
    """
    cpf = re.sub(r'\D', '', cpf_raw)  # Remove tudo que não for número
    cpf = cpf.zfill(11)  # Adiciona zeros à esquerda
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
