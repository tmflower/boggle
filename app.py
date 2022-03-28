from flask import Flask, jsonify, render_template, session, request, json, redirect
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sadiebug'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def start_game():
    """Show home page with game stats and button to start new game"""
    hi_score = session.get('hi_score', 0)
    num_plays = session.get('num_plays', 0)
    session['num_plays'] = num_plays
    session['hi_score'] = hi_score
    return render_template('start-game.html', hi_score = hi_score, num_plays = num_plays)

@app.route('/new-game')
def show_board():
    """Display game board and form for user to enter a word"""
    board = boggle_game.make_board()
    session['board'] = board
    board = session.get('board')
    return render_template('new-game.html', board = board)

@app.route('/check-word')
def check_word():
    """Evaluate if word is 'ok', 'not-word', or 'not-on-board' and give user feedback"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'response': response})


@app.route('/game-over', methods = ["POST"])
def game_over():
    """Display game stats and enable user to play again"""
    update_hi_score()
    update_num_plays()
    return redirect('/new-game')


def update_hi_score():
    """Update user high score"""
    hi_score = session.get('hi_score')
    score = request.json['score']

    print("Score from json request:", score)
    print("hi score before:", session['hi_score'])

    if not hi_score:
        session['hi_score'] = score
    else:
        session['hi_score'] = max(score, hi_score)

    print("hi score after:", session['hi_score'])
    return session['hi_score']


def update_num_plays():
    """Update number of times user has played the game"""
    num_plays = session.get('num_plays')
    print("num plays before:", num_plays)

    session['num_plays'] = num_plays + 1
    print("num plays after:", session['num_plays'])
    return session['num_plays']