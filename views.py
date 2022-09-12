from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time
@app.route('/')
def index():
    jogos = Jogos.query.order_by(Jogos.id)
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

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{uploads_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editar jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atulizar', methods=['POST', ])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    uploads_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(id)
    arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Jogo deletado!')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Faça seu Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


