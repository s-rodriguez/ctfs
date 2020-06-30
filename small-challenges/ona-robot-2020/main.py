from flask import Flask, session, render_template
import flask_session
import random
import os
import re
import sys

flag = os.getenv("FLAG", "THIS_IS_NOT_A_FLAG")

app = Flask(__name__, template_folder='.', static_folder='static', static_url_path='/')
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
flask_session.Session(app)

CHOICES = ['🍒', '🍍', '🍑', '🍇', '🍊', '🍓', '🍌']
VALUES = {
    '🍌3': 1,
    '🍍2': 1,
    '🍑2': 1,
    '🍇2': 2,
    '🍊2': 2,
    '🍓2': 3,
    '🍒2': 3,
    '🍍3': 5,
    '🍑3': 5,
    '🍇3': 5,
    '🍊3': 10,
    '🍓3': 10,
    '🍒3': 50,
}

def row():
    return [random.choice(CHOICES) for i in range(3)]

def payfor(row):
    for element in row:
        combination = element + str(row.count(element))
        if combination in VALUES:
            return VALUES[combination]
    return 0

def isnumber(n):
    return n == n

def isnegative(n):
    return -sys.float_info.max < n and n <= 0

@app.route('/')
def home():
    return render_template('home.html',
                           title="Tragamonedas",
                           description="Buena suerte, aunque \
                           tal vez vos no la necesites!")

@app.route('/start')
def start():
    money = 10
    session['money'] = money
    return 'Hey! Te presto ${0:.2f} para que comiences.\n'.format(money)

@app.route('/get')
def get():
    return 'Tienes ${0:.2f}\n'.format(session.get('money', 0))

@app.route('/bet/<bet_str>')
def bet(bet_str):
    try:
        bet = float(bet_str)
    except:
        return 'Tu apuesta tiene que ser un numero amigue!'

    regex = re.compile('[a-z]')
    if not isnumber(bet) or regex.findall(bet_str):
        return 'Nada de cosas raras.'

    if isnegative(bet):
        return 'Jaja! Buen intento pero sin negativos!'

    money = float(session.get('money', 0))
    if bet > money:
        return 'No tenés suficiente dinero para apostar eso.'

    row1 = row()
    row2 = row()
    row3 = row()
    won = bet * payfor(row2)
    money += won - bet

    res = '  {}  \n► {} ◄\n  {}  \n'.format(' | '.join(row1), ' | '.join(row2), ' | '.join(row3))
    res += 'Tienes ${0:.2f}\n'.format(money)

    if won > 0:
        res += 'Bien! Gastaste ${0:.2f} y recibiste ${0:.2f}\n'.format(bet, won)
    else:
        res += 'Lo siento, perdiste tu apuesta.\n'

    if money <= 0:
        res += 'Ya no tenés dinero, parece que no sabés apostar.'
        session['money'] = money
    elif money < 1000000000:
        res += 'Sigue así y ganarás!'
        session['money'] = money
    else:
        res += 'Bien!!! Claramente has ganado.\n'
        res += 'Tu flag es: {}'.format(flag)

    return res

app.run(debug=True)
