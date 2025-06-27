from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_cors import CORS
from transformers import pipeline

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # <-- ESSENCIAL

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# analise de sentimento
sentimento_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

#MODELOS

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.String(180))
    sentimento = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

#ROTAS USUARIO

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    novo_usuario = Usuario(tipo=data['tipo'], email=data['email'], senha=data['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"id": novo_usuario.id}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "tipo": u.tipo, "email": u.email} for u in usuarios])

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get_or_404(id)
    usuario.tipo = data.get('tipo', usuario.tipo)
    usuario.email = data.get('email', usuario.email)
    usuario.senha = data.get('senha', usuario.senha)
    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso"})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário deletado com sucesso"})

#ROTAS COMENTARIO

@app.route('/comentarios', methods=['POST'])
def criar_comentario():
    data = request.get_json()
    texto = data['texto']
    usuario_id = data['usuario_id']

    resultado = sentimento_pipeline(texto)[0]
    nota = int(resultado['label'][0])  

    novo_comentario = Comentario(texto=texto, sentimento=nota, usuario_id=usuario_id)
    db.session.add(novo_comentario)
    db.session.commit()
    return jsonify({"id": novo_comentario.id, "sentimento": nota}), 201

@app.route('/comentarios', methods=['GET'])
def listar_comentarios():
    comentarios = Comentario.query.all()
    return jsonify([
        {"id": c.id, "texto": c.texto, "sentimento": c.sentimento, "usuario_id": c.usuario_id}
        for c in comentarios
    ])

@app.route('/comentarios/<int:id>', methods=['DELETE'])
def deletar_comentario(id):
    comentario = Comentario.query.get_or_404(id)
    db.session.delete(comentario)
    db.session.commit()
    return jsonify({"mensagem": "Comentário deletado"})

#ROTAS EXTRAS

@app.route('/analisar_sentimento', methods=['POST'])
def analisar_sentimento():
    data = request.get_json()
    if 'texto' not in data:
        return jsonify({"erro": "Texto não fornecido"}), 400

    resultado = sentimento_pipeline(data['texto'])
    return jsonify(resultado), 200

# MAIN

if __name__ == '__main__':
    with app.app_context():
        print(">> Criando banco e tabelas...")
        db.create_all()
        print(">> Tabelas criadas.")

        # FORÇA CRIAÇÃO com um INSERT fake (opcional)
        if not Usuario.query.first():
            user = Usuario(tipo='teste', email='teste@teste.com', senha='123')
            db.session.add(user)
            db.session.commit()
            print(">> Usuário dummy criado.")
    app.run(debug=True)

print("Banco configurado em:", app.config['SQLALCHEMY_DATABASE_URI'])

