from app import app
from unittest import TestCase
from flask import session, request

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTestCase(TestCase):

    def test_home(self):
        """Test if home page displays correctly"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(session['hi_score'], 0)
            self.assertEqual(session['num_plays'], 0)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button>Start Game!</button>', html)

 
    def test_new_game(self):
        """Test if game board page displays correctly"""
        with app.test_client() as client:
            res = client.get('/new-game')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('<label for="guess">Try a word:</label>', html)
            self.assertIsInstance(session['board'], list)


    def test_check_word(self):
        """Test if words are validated correctly"""
        with app.test_client() as client:
            client.get('/new-game')
            with client.session_transaction() as my_session:
                my_session['board'] = [ ['X', 'H', 'Y', 'K', 'W'],
                                        ['M', 'W', 'L', 'P', 'H'], 
                                        ['C', 'U', 'O', 'C', 'N'], 
                                        ['G', 'W', 'J', 'R', 'W'], 
                                        ['B', 'H', 'S', 'J', 'M']]
            res = client.get('/check-word?word=owl')
            self.assertEqual(res.json['response'], 'ok')

            res = client.get('/check-word?word=asdf')
            self.assertEqual(res.json['response'], 'not-word')

            res = client.get('/check-word?word=spaghetti')
            self.assertEqual(res.json['response'], 'not-on-board')


    def test_update_hi_score(self):
        with app.test_client() as client:

            with client.session_transaction() as session:
      
                session['hi_score'] = 10
                session['num_plays'] = 3

            client.post('/game-over', json = { 'score': 25 })

            self.assertEqual(request.json['score'], 25)
            self.assertEqual(session['hi_score'], 25)

    def test_update_num_plays(self):
        with app.test_client() as client:

            with client.session_transaction() as session:
      
                session['hi_score'] = 10
                session['num_plays'] = 3

            client.post('/game-over', json = { 'score': 25 })

            self.assertEqual(session['num_plays'], 4)

    def test_game_over(self):
        """Tests if game stats are displayed and user can start a new game"""
        with app.test_client() as client:

            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Your highest score', html)
            self.assertIn('Number of games played', html)