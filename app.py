from flask import Flask, request, jsonify
import pickle
import os
import datetime

app = Flask(__name__)

MODEL_FILE = 'model.pkl'
CODE_VERSION = "v1.1"

# Variável global para armazenar as regras
model_rules = []
model_date = "unknown"

def load_model():
    """Carrega o modelo do disco para a memória"""
    global model_rules, model_date
    if os.path.exists(MODEL_FILE):
        print(f"Carregando modelo de {MODEL_FILE}...")
        try:
            with open(MODEL_FILE, 'rb') as f:
                model_rules = pickle.load(f)
            
            # Pega a data de modificação do arquivo para retornar na API
            timestamp = os.path.getmtime(MODEL_FILE)
            model_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Modelo carregado! {len(model_rules)} regras encontradas. Data: {model_date}")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            model_rules = []
    else:
        print(f"AVISO: Arquivo {MODEL_FILE} não encontrado. A API iniciará sem recomendações.")
        model_rules = []

# Carrega o modelo assim que o app inicia
load_model()

@app.route('/api/recommend', methods=['POST'])
def recommend():
    # 1. Pega os dados da requisição
    data = request.get_json(force=True)
    if not data or 'songs' not in data:
        return jsonify({"error": "Formato inválido. Esperado: {'songs': ['Musica A', ...]}"}), 400

    user_songs = data['songs']
    recommendations = set()

    # 2. Lógica de Recomendação
    # As regras do fpgrowth-py vêm no formato: [{Antecedente}, {Consequente}, Confiança]
    # Exemplo: [{'Yesterday'}, {'Let It Be'}, 0.85]
    
    print(f"Recebido pedido para músicas: {user_songs}")

    for rule in model_rules:
        antecedent = rule[0]
        consequent = rule[1]
        confidence = rule[2]

        # Se o usuário curte TODAS as músicas do antecedente, recomendamos o consequente
        if antecedent.issubset(set(user_songs)):
            recommendations.update(consequent)

    # Remove as músicas que o usuário já ouviu das recomendações
    recommendations = recommendations - set(user_songs)

    # 3. Monta a resposta
    response = {
        "songs": list(recommendations),
        "version": CODE_VERSION,
        "model_date": model_date
    }
    
    return jsonify(response)

