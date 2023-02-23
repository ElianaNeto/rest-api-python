# Flask-REST API 

## RODANDO 

1. Clone repository.
2. Inicie o servidor rodando o comando `python app.py`

## USO
### Endpoint do usuário

#### 1. Login
POST http://127.0.0.1:5000/login

REQUEST
```json
{
    "nome_user": "Jonh",
    "senha": "jonh1234"
}
```
RESPONSE
```json
{
    "utilizador": {
        "id": 1,
        "nome_completo": "Jonh Watson",
        "nome_user": "jonh",
        "email": "jonh@ocr.com",
        "idioma": "pt"
    },
    "mensagem": "Login efetuado com sucesso"
}
```

#### 2. Cadastro
POST http://127.0.0.1:5000/cadastro

REQUEST
```json
{
   "nome_user": "jonh",
    "senha": "jonh1234",
    "nome_completo": "Jonh Watson",
    "email": "jonh@ocr.com",
    "idioma": "en"
}
```
RESPONSE
```json
{
    "utilizador": {
        "id": 2,
        "nome_user": "jonh",
        "senha": "jonh1234",
        "nome_completo": "Jonh Watson",
        "email": "jonh@ocr.com",
        "idioma": "en"
    },
    "mensagem": "Utilizador criado com sucesso"
}
```

#### 3. Ver um usuario especifico
GET http://127.0.0.1:5000/utilizador/2

RESPONSE
```json
{
    "utilizador": {
        "id": 2,
        "nome_user": "jonh",
        "senha": "jonh1234",
        "nome_completo": "Jonh Watson",
        "email": "jonh@ocr.com",
        "idioma": "en"
    }
}
```
#### 4. Ver todos usuarios
GET http://127.0.0.1:5000/utilizadores

RESPONSE
```json
{
    "utilizadores": [
        {
            "id": 1,
            "nome_user": "teresa",
            "senha": "teresa",
            "nome_completo": "Teresa JORGE",
            "email": "teresa@hotmail.com",
            "idioma": "en"
        },
        {
            "id": 2,
            "nome_user": "jonh",
            "senha": "jonh1234",
            "nome_completo": "Jonh Watson",
            "email": "jonh@ocr.com",
            "idioma": "en"
        }
    ],
    "mensagem": "ok"
}
```
#### 5. Actulizar um utilizador
PUT http://127.0.0.1:5000/utilizador/2

OBS: Pode adicionar outros campos para serem alterados!

```json
{
    "nome_user": "eliana",
    "senha": "eliana123"
}
```

RESPONSE
```json
  {
    "utilizador": {
        "id": 1,
        "nome_user": "eliana",
        "senha": "eliana123",
        "nome_completo": "Milenia Neto",
        "email": "milenianeto@hotmail.com",
        "idioma": "en"
    },
    "mensagem": "Utilizador actualizado com sucesso"
}

```

#### 6. Deletar um utilizador
DELETE http://127.0.0.1:5000/utilizador/1

RESPONSE
```json
{
    "utilizador": {
        "id": 1,
        "nome_user": "eliana",
        "senha": "eliana123",
        "nome_completo": "Milenia Neto",
        "email": "milenianeto@hotmail.com",
        "idioma": "en"
    },
    "mensagem": "Utilizador deletado com sucesso"
}
```

### Endpoint para o historico de traducoes por usuario é similar ao endpoint do usuário.