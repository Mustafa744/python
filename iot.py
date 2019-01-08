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
  print ("No door number specified")
  return 'No door number specified'

 elif doornum == '1':
  print ("Door number 1 cycled")
  return 'Door number 1 cycled.'
  
  
 elif doornum == '2':
  print("Door number 2 cycled")
  return 'Door number 2 cycled'

 elif doornum == '3':
  print("Door number 3 cycled")
  return 'Door number 3 cycled'

run(host='0.0.0.0', port=1234)

