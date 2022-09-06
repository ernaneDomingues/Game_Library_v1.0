from flask import Flask, render_template, request, redirect


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Skyrim', 'Aventura', 'PC')
jogo3 = Jogo('Pokemon', 'Aventura/Fantasia', 'Nintendo')
jogo4 = Jogo('Mario', 'Aventura', 'Nintendo')
jogos = [jogo1, jogo2, jogo3, jogo4]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo='Cadastro de jogos')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogos.append(jogo)
    return redirect('/')


app.run(debug=True)
