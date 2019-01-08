# Python Script To Control Garage Door

# Load libraries
import time
from bottle import route, run, template


# Handle http requests to the root address
@route('/')
def index():
 return 'Go away.'

# Handle http requests to /garagedoor
@route('/garagedoor/:doornum')
def garagedoor(doornum=0):
 if doornum == '0':
  return 'No door number specified'

 elif doornum == '1':
  return 'Door number 1 cycled.'

 elif doornum == '2':
  print("hiiiiiiiii")
  return 'Door number 2 cycled'

run(host='0.0.0.0', port=1234)
