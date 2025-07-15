# slack_alerta.py
import requests

def enviar_mensagem_slack(mensagem):
    webhook_url = "https://hooks.slack.com/services/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"  # Substitua com seu webhook se mudar
    payload = {
        "text": mensagem
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("✅ Alerta enviado para o Slack!")
    else:
        print(f"❌ Erro ao enviar alerta para o Slack: {response.status_code} - {response.text}")
