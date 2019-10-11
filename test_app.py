from unittest import TestCase, main as unittest_main, mock
import bcrypt
from app import app


class MuzicaTestss(TestCase):
    def setUp(self):
        # Gets the Flask test client
        self.client = app.test_client()

        # Displays Flask errors that happen
        app.config['TESTING'] = True

    '''
    Tests to see if the page was loaded.
    '''

    def test_home(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'title', result.data, 'Page did not load')

    '''
    Tests to see if the page doesn;'t load because creating a listing
    requires a login/account
    '''

    def test_market_create(self):
        result = self.client.get('/market/create')
        self.assertNotEqual(result.status, '200 OK')
        self.assertFalse(b'Create' in result.data, 'Create page reached')

    '''
    Tests to see if the login page was loaded
    '''

    def test_login(self):
        result = self.client.get('/login')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Login', result.data, 'Login page not accessed')

    '''
    Tests to see if the logout route was accessed
    '''

    def test_logout(self):
        result = self.client.get('/logout')
        self.assertEqual(result.status, '200 OK')

    '''
    Tests to see if the register page can be accessed.
    '''

    def test_register(self):
        result = self.client.get('/register')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Register', result.data, 'Register page not accessed')


if __name__ == '__main__':
    unittest_main()
