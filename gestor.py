from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import date
import dbo as db

app = Flask(__name__)
app.secret_key = 'flask'

class Pokemon: 
    def __init__(self, nome, especie, tipo):
        self.nome = nome
        self.especie = especie
        self.tipo = tipo

class Treinadora:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

#criação das terindoras
treinadora1 = Treinadora('Mary', 'Mary Jackson ', '1234')
treinadora2 = Treinadora('Ada', 'Ada Lovelace', '1234')
treinadora3 = Treinadora('Katherine', 'Katherine Johnson', '1234')

treinadoras = {treinadora1.id: treinadora1,
            treinadora2.id: treinadora2,
            treinadora3.id: treinadora3}

#configuração da rota index.
@app.route('/')
def index():
    proxima = url_for('listag')
    return render_template('login.html', proxima=proxima) 

@app.route('/lista')
def listag():

    query = "SELECT * FROM listas GROUP BY `codlista`"
    values = db.selectdb(query)

    return render_template('lista.html', titulo='Minhas Listas', listas=values)   

@app.route('/detalha', methods=['GET',])
def detlista():

    lista = request.args.get('lista')
    titulo = 'Detalhes da Lista'

    query = "SELECT `codlista`, `desc_lista`, `item`, `produto`, `qtde`, `valor` FROM listas WHERE codlista = '"+lista+"' AND produto not in ('RL')"
    values = db.selectdb(query)
    
    return render_template('detalhalista.html', titulo=titulo , listas=values)   

@app.route('/carrinho')
def carrinho():
    
    data = date.today()

    #Busca ultima lista valida e ativa para o usuario logado
    query = "SELECT * FROM `listas` WHERE usuario = '"+session['usuario_logado']+"' AND lista_ativa = 'S';"
    result = db.selectdb(query)


    #Se existir exibe produtos ja existentes na lista
    if len(result) > 0:
        codlista = result[0][9]

        query = "SELECT * FROM `listas` WHERE codlista = '"+str(codlista)+"' AND produto not in ('RL')"
        result = db.selectdb(query)
    
    #Se não reservar nova numeração de lista de carrinho
    else:
        #Busca a ultima lista inclusa na base
        query = "SELECT MAX(codlista) as max FROM `listas` WHERE 1;"
        result = db.selectdb(query)
        max = result[0]
        cod_lista = int(max[0])+1    

        query  = "INSERT INTO listas (usuario, item, produto, qtde, valor, data_compra, desc_lista, lista_ativa, codlista) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (session['usuario_logado'],'00','RL',0,0.00,data,'Reserva de Lista','S',cod_lista)
        db.insertdb(query,values)

    return render_template('carrinho.html', titulo='Carrinho de Compras', lista=result)    

@app.route('/calculadora')
def calculadora():
    return render_template('calculadora.html', titulo='Calculadora', pokemons=lista)    

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
        return render_template('novo.html', titulo='Novo Pokemon')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    especie = request. form['especie']
    tipo = request. form['tipo']
    pokemon = Pokemon(nome, especie, tipo)
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['treinadora'] in treinadoras:
        treinadora = treinadoras[request.form['treinadora']]
        if treinadora.senha == request.form['senha']:
            session['usuario_logado'] = treinadora.id
            flash('Seja Bem Vindo(a), ' + treinadora.nome )
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:        
        flash('Acesso negado, digite novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Acesse novamente para utilizar o App')
    return redirect(url_for('index'))


app.run()

