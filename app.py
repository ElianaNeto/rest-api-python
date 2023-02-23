from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db = SQLAlchemy(app)

class Utilizador(db.Model):
  __tablename_ = 'utilizador'
  id = db.Column(db.Integer, primary_key=True)
  nome_completo = db.Column(db.String(50),nullable=False)
  nome_user = db.Column(db.String(50),nullable=False)
  senha = db.Column(db.String(50),nullable=False)
  email = db.Column(db.String(50),nullable=False)
  idioma = db.Column(db.String(50),nullable=False)
  

  def to_json(self):
    return {"id": self.id, "nome_user": self.nome_user, "senha": self.senha, "nome_completo": self.nome_completo,"email": self.email, "idioma": self.idioma}


class Historico(db.Model):
  __tablename_ = 'historico'
  id = db.Column(db.Integer, primary_key=True)
  texto_origem = db.Column(db.String(), nullable=False)
  texto_destino= db.Column(db.String(),nullable = False)
  idioma_origem= db.Column(db.String(), nullable = False)
  idioma_destino= db.Column(db.String(), nullable = False)
  id_utilizador = db.Column(db.Integer, db.ForeignKey('utilizador.id'))
  utilizador = db.relationship('Utilizador', backref=db.backref('historico', lazy=True))
 
  def to_json(self):
    return {"id": self.id, "texto_origem": self.texto_origem, "texto_destino": self.texto_destino, "idioma_origem": self.idioma_origem,"idioma_destino": self.idioma_destino, "id_utilizador": self.id_utilizador}



with app.app_context():
    db.create_all()

@app.route("/login", methods=["POST"])
def login():

  nome_user = request.json.get('nome_user')
  senha = request.json.get('senha')

  try: 
    utilizador = Utilizador.query.filter_by(nome_user=nome_user).first()

    if utilizador or utilizador.senha == senha :
      return gera_response( 200,"utilizador", {'id':utilizador.id,'nome_completo': utilizador.nome_completo,'nome_user': utilizador.nome_user,'email': utilizador.email,'idioma': utilizador.idioma,}, "Login efetuado com sucesso")

    return gera_response(401, "message", {'nome':nome_user,'senha':senha},"Email ou palavra-passe errada!")    

  
  except Exception as e:
    print('Erro',e)
    return gera_response(400, "utilizador", {'nome':nome_user,'senha':senha}, "Erro ao logar")


@app.route("/cadastro", methods=["POST"])
def cadastro():
  body = request.get_json()
  try:
    utilizador = Utilizador(nome_completo=body["nome_completo"],nome_user=body["nome_user"], senha=body["senha"],email=body["email"],idioma=body["idioma"])
    db.session.add(utilizador)
    db.session.commit()

    return gera_response(201, "utilizador", utilizador.to_json(), "Utilizador criado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    return gera_response(400, "utilizador", {}, "Erro ao cadastrar")




# Selecionar tudo
@app.route("/utilizadores", methods=["GET"])
def selecionar_utilizadores():
  utilizadores_objectos = Utilizador.query.all()
  utilizadores_json = [utilizador.to_json() for utilizador in utilizadores_objectos] #para cada user em ut_obj executa o to_json
  print( utilizadores_json)
  #return Response(json.dumps(utilizadores_json))
  return gera_response(200, "utilizadores", utilizadores_json,"ok")

# Selecionar um
@app.route("/utilizador/<id>", methods=["GET"])
def selecionar_utilizador(id):
  utilizador_objecto = Utilizador.query.filter_by(id=id).first()
  utilizador_json = utilizador_objecto.to_json()
  return gera_response(200, "utilizador", utilizador_json)


# Actualizar
@app.route("/utilizador/<id>", methods=["PUT"])
def atualizar_utlizador(id):
  #pegar user
  utilizador = Utilizador.query.filter_by(id=id).first()
  
  #pegar modificacoes
  body = request.get_json()

  try:
    if('nome_completo' in body):
      utilizador.nome_completo = body['nome_completo']
    if('nome_user' in body): #alterar so oo nome
      utilizador.nome_user = body['nome_user']
    if('senha' in body): #alterar so pass
      utilizador.senha = body['senha']
    if('email' in body): #alterar so pass
      utilizador.email=body["email"]
    if('idioma' in body): #alterar so pass
      utilizador.idioma=body["idioma"]
    
    db.session.add(utilizador)
    db.session.commit()
    return gera_response(200, "utilizador", utilizador.to_json(), "Utilizador actualizado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    gera_response(400, "utilizador", {}, "Erro ao actualizar")


#Deletar
@app.route("/utilizador/<id>", methods=["DELETE"])
def deletar_utilizador(id):
  utilizador = Utilizador.query.filter_by(id=id).first()

  try:
    db.session.delete(utilizador)
    db.session.commit()
    return gera_response(200, "utilizador", utilizador.to_json(), "Utilizador deletado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    gera_response(400, "utilizador", {}, "Erro ao deletar")


###########################
@app.route('/utilizador/<int:utilizador_id>/historico/', methods=['GET'])
def get_historico_by_user(utilizador_id):
    utilizador = Utilizador.query.get(utilizador_id)
    if not utilizador:
        return gera_response(400, 'Mensagem', 'Utilizador não encontrado')

    historicos = [historico.to_json() for historico in utilizador.historico]
    return gera_response(201, "Historicos", historicos)




#################### HISTORICO  
@app.route("/historicos", methods=["GET"])
def selecionar_historicos():
  historicos_objectos = Historico.query.all()
  historicos_json = [historico.to_json() for historico in historicos_objectos] #para cada hist em ut_obj executa o to_json
  print( historicos_json)
  #return Response(json.dumps(utilizadores_json))
  return gera_response(200, "historicos", historicos_json,"ok")

# Selecionar um
@app.route("/historico/<id>", methods=["GET"])
def selecionar_historico(id):
  historico_objectos = Historico.query.filter_by(id=id).first()
  historicos_json = historico_objectos.to_json()
  return gera_response(200, "historico", historicos_json)


@app.route("/historico_utilizador/<id_utilizador>", methods=["GET"])
def selecionar_historico_utilizar(id):
  #historico_objectos = Historico.query.filter_by(id_utilizador=id).first()
  historico_objectos = Historico.query.filter_by(id_utilizador=id).all()
  historicos_json = historico_objectos.to_json()
  return gera_response(200, "historico", historicos_json)


# Cadastrar
@app.route("/cadastro_historico", methods=["POST"])
def criar_historico():
  body = request.get_json()
  try:
    historico = Historico(texto_origem=body["texto_origem"], texto_destino=body["texto_destino"], idioma_origem=body["idioma_origem"], idioma_destino=body["idioma_destino"], id_utilizador=body["id_utilizador"])
    db.session.add(historico)
    db.session.commit()

    return gera_response(201, "historico", historico.to_json(), "historico criado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    return gera_response(400, "historico", {}, "Erro ao cadastrar")



# Actualizar
@app.route("/historico/<id>", methods=["PUT"])
def atualizar_historico(id):
  #pegar user
  historico = Historico.query.filter_by(id=id).first()
  
  #pegar modificacoes
  body = request.get_json()  

  try:
    if('texto_origem' in body):
      historico.texto_origem=body["texto_origem"]

    if('texto_destino' in body):
      historico.texto_destino=body["texto_destino"]

    if('idioma_origem' in body):
      historico.idioma_origem=body["idioma_origem"]

    if('idioma_destino' in body):
      historico.idioma_destino=body["idioma_destino"]

    if('id_utilizador' in body):
      historico.id_utilizador=body["id_utilizador"]
    
    db.session.add(utilizador)
    db.session.commit()
    return gera_response(200, "hsitorico", historico.to_json(), "Historico actualizado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    gera_response(400, "historico", {}, "Erro ao actualizar")


#Deletar
@app.route("/historico/<id>", methods=["DELETE"])
def deletar_historico(id):
  historico = Historico.query.filter_by(id=id).first()

  try:
    db.session.delete(historico)
    db.session.commit()
    return gera_response(200, "historico", historico.to_json(), "historico deletado com sucesso")
    
  except Exception as e:
    print('Erro',e)
    gera_response(400, "historico", {}, "Erro ao deletar")




################
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
  body = {}
  body[nome_do_conteudo] = conteudo

  if(mensagem):
    body["mensagem"] = mensagem

  return Response(json.dumps(body),status=status, mimetype="application/json")



app.run()
