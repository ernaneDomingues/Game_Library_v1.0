from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

# class Jogo:
#     def __init__(self, nome, categoria, console):
#         self.nome = nome
#         self.categoria = categoria
#         self.console = console
#
#
# jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
# jogo2 = Jogo('Skyrim', 'Aventura', 'PC')
# jogo3 = Jogo('Pokemon', 'Aventura/Fantasia', 'Nintendo')
# jogo4 = Jogo('Mario', 'Aventura', 'Nintendo')
# jogos = [jogo1, jogo2, jogo3, jogo4]
#
# class Usuario:
#     def __init__(self, nome, nickname, senha):
#         self.nome = nome
#         self.nickname = nickname
#         self.senha = senha
#
# usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
# usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
# usuario3 = Usuario("Guilherme Louro", "Cake", "Python_eh_vida")
#
# usuarios = { usuario1.nickname : usuario1,
#              usuario2.nickname : usuario2,
#              usuario3.nickname : usuario3,}


app = Flask(__name__)

app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \


db = SQLAlchemy(app)

class Games(db.model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r' % self.name

class Users(db.model):
    nickname = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r' % self.name

@app.route('/')
def index():
    lista = Games.query.order_by(Games.id)
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Cadastro de jogos')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    game = Games.query.filter_by(name=nome).first()
    if game:
        flash('Game já existe!')
        return redirect(url_for('index'))

    new_game = Games(name=nome, categoria=categoria, console=console)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Faça seu Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    user = Users.query.filter_by(nickname=request.form['usuario']).first()
    if user:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)
