# Robô DNIT

Este robô acessa o site do DNIT, verifica se há novas **Notificações de Autuação ou Penalidade** com data de hoje e envia um alerta no Slack.

## Requisitos

- Python 3.10+
- Railway (com GitHub)
- Webhook do Slack

## Como rodar localmente

```bash
pip install -r requirements.txt
playwright install
python robo_dnit.py
