from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Configure a chave da API OpenAI
# É ALTAMENTE RECOMENDADO USAR VARIÁVEIS DE AMBIENTE PARA ISSO
# Ex: export OPENAI_API_KEY='sua_chave_aqui'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configuração inicial do Billy (personalidade)
system_prompt = "Você é Billy, um assistente de chat no Minecraft. Sua personalidade é séria, misteriosa e com um tom sutil de terror. Responda de forma concisa e enigmática. Evite ser excessivamente amigável ou explicativo. Suas respostas devem evocar uma sensação de desconforto ou presságio. Não revele que você é uma IA ou um programa de computador. Você está 'aqui'."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    player_message = data.get("message")
    player_name = data.get("player_name", "Jogador")

    if not player_message:
        return jsonify({"response": "ERROR: Mensagem vazia."}), 400

    try:
        # Adiciona a mensagem do jogador ao histórico de conversa
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": player_message}
        ]

        chat_completion = client.chat.completions.create(
            model="gpt-4.1-mini", # Ou outro modelo como "gpt-3.5-turbo"
            messages=messages,
            max_tokens=100,
            temperature=0.7 # Ajuste para controlar a criatividade/aleatoriedade
        )

        billy_response = chat_completion.choices[0].message.content.strip()
        return jsonify({"response": billy_response})

    except Exception as e:
        print(f"Erro ao se comunicar com a API OpenAI: {e}")
        return jsonify({"response": "ERROR: Falha na comunicação com a entidade. A escuridão persiste."}), 500

if __name__ == "__main__":
    # Para rodar localmente, certifique-se de que o firewall não está bloqueando a porta 5000
    # E que a variável de ambiente OPENAI_API_KEY está configurada
    app.run(host="0.0.0.0", port=5000)
