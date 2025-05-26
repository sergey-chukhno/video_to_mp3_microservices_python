import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

server = Flask(__name__)
mysql = MySQL(server)

#config 
server.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST") 
server.config["MYSQL_USER"] = os.getenv("MYSQL_USER") 
server.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD") 
server.config["MYSQL_DB"] = os.getenv("MYSQL_DB") 
server.config["MYSQL_PORT"] = os.getenv("MYSQL_PORT") 

@server.route("/login", methods = ["POST"])
def login(): 
  auth = request.authorization
  if not auth: 
    return "Missing credentials", 401
  
  # Check db for username and password 
  cur = mysql.connection.cursor()
  res = cur.execute(
    'SELECT email, password FROM user WHERE email = %s', (auth.username,)
  )

  if res > 0: 
    user_row = cur.fetchone()
    email = user_row[0]
    password = user_row[1]

    if auth.username != email or auth.password != password: 
      return "Invalid credentials", 401
    else: 
      return create_JWT(auth.username, os.environ.get("JWT_SECRET_KEY"), True)
  else:
    return 'User not found', 401

@server.route("/validate", methods=["POST"])
def validate(): 
  encoded_jwt = request.headers["Authorization"]
  if not encoded_jwt:
    return "Missing credentials", 401 
  
  encoded_jwt = encoded_jwt.split(" ")[1]

  try: 
    decoded = jwt.decode(
      encoded_jwt, os.environ.get("JWT_SECRET"), algorithms = ["HS256"]
    )
  except: 
    return "Unauthorized", 403
  
  return decoded, 200
  


def create_JWT(username, secret, authz):
  return jwt.encode(
    {
      "username": username, 
      "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
      "iat": datetime.date.now(tz=datetime.timezone.utc), 
      "admin": authz
    }, 
    secret, 
    algorithm="HS256"
  )
if __name__ == "__main__": 
  server.run(host="0.0.0.0", port=5000, debug=True)