import os, requests
import spotipy.util as util

def loadAuthArgs():
    # Read contents and return auth args
    with open('settings/webbify_credentials.txt', 'r') as tfile:
        fileContents = tfile.read().split('\n')
        CLIENT_ID = fileContents[0].split(':')[1][1:]
        CLIENT_SECRET = fileContents[1].split(':')[1][1:]

    return (CLIENT_ID, CLIENT_SECRET)


def testToken(token):
    # Declare url and header
    URL_BASE = 'https://api.spotify.com'
    HEADERS = getHeader(token)

    # Try token and return success or failure
    data = requests.get('{}/v1/me'.format(URL_BASE), headers=HEADERS)

    return (data.status_code == 200)

def getHeader(token):
    return {'Authorization': 'Bearer {}'.format(token)}


def connectSpotify(authType='playlist-read-private'):
    # Proivde username
    USERNAME = 'nghokui@gmail.com'

    # Remove a stored token if it exists already
    TOKEN_CACHE = '.cache-{}'.format(USERNAME)
    if os.path.exists(TOKEN_CACHE):
        os.remove(TOKEN_CACHE)

    # Generate the authorization arguments
    CLIENT_ID, CLIENT_SECRET = loadAuthArgs()
    AUTH_ARGS = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'https://localhost:8888/',
        'scope': authType
    }

    # Load token and test it
    token = util.prompt_for_user_token(USERNAME, **AUTH_ARGS)
    testResult = testToken(token)

    # Send result text and return token
    if testResult:
        print('Token loaded successfully.')
        header = getHeader(token)
        
    return (header, token) if testResult else (None, None)