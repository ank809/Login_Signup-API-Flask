from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import re
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/users'
app.config['SECRET_KEY']= "secret_key"
mongo= PyMongo(app).db
@app.route('/')
def hi():
    return "Hello"

def isPassword(password):
    if (
        len(password)>=8 
        and any(c.islower() for c in password ) 
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and re.search('[^a-zA-Z0-9]', password)
        and any(c.isalnum() for c in password )
        ):
        return True
    else:
        return False
    
@app.route('/register', methods=['POST'])
def register():
    if request.method=="POST":
        username= request.json['username']
        email= request.json['email']
        password= request.json['password']
        if mongo.users.find_one({"username":username}):
            return jsonify({"error": "this username is  already taken. Choose a new one"})
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Enter a valid email"})
        if not isPassword(password):
            return jsonify({"error": "Password should contain one uppercase, lowercase, digit and special character"})
        hashed_password= generate_password_hash(password)
        user= {
            "username":username,
            "email":email,
            "password":hashed_password
        }
        mongo.users.insert_one(user)
        return jsonify({"successfull":"Account Created" })

@app.route('/login', methods=['POST'])
def login():
    username= request.json['username']
    password= request.json['password']
    user= mongo.users.find_one({"username":username})
    if user and check_password_hash(user['password'], password):
        return jsonify({"success":"user logged in"}),200
    else:
        return jsonify({"error":"Invalid username or password"}),401

if __name__== "__main__":
    app.run(debug=True)