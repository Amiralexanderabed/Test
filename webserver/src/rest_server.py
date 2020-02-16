from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import json
import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def get_students_method(req):
  # Connect to the database and retrieve the student
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select id, first_name, last_name, email, pid from TStudents;")
  records = cursor.fetchall()
  return json.dumps(records)

def get_student_method(req):
  # Retrieve the route argument (this is not GET/POST data!)
  the_id = req.matchdict['student_id']

  # Connect to the database and retrieve the student
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from TStudents where id='%s';" % the_id)
  record = cursor.fetchone()
  db.close()

  if record is None:
    return ""

  # Format the result as key-value pairs
  response = {
    'id':         record[0],
    'first_name': record[1],
    'last_name':  record[2],
    'email':      record[3],
    'pid':        record[4],
    'datetime':   record[5].isoformat()
  }
  return json.dumps(response)


#''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.add_route('get_students', '/students')
  config.add_view(get_students_method, route_name='get_students', renderer='json')

  config.add_route('get_student', '/student/{student_id}')
  config.add_view(get_student_method, route_name='get_student', renderer='json')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()