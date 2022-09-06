from flask import Flask, render_template

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console



app = Flask(__name__)

@app.route('/')
def ola():
    jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
    jogo2 = Jogo('Skyrim', 'Aventura', 'PC')
    jogo3 = Jogo('Pokemon', 'Aventura/Fantasia', 'Nintendo')
    jogo4 = Jogo('Mario', 'Aventura', 'Nintendo')
    jogos = [jogo1, jogo2, jogo3, jogo4]
    return render_template('lista.html', titulo='Jogos', jogos=jogos)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo='Cadastro de jogos')

app.run()