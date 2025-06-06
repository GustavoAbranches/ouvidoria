from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

sentimento = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

@app.route('/analisar_sentimento', methods=['POST'])
def analisar_sentimento():
    dados = request.get_json()

    if 'texto' not in dados:
        return jsonify({"erro": "Texto não fornecido"}), 400

    texto = dados['texto']

    resultado = sentimento(texto)

    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True)
