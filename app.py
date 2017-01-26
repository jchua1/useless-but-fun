from flask import Flask, session, request, url_for, redirect, render_template
from flask_socketio import SocketIO, send, emit
from utils import level, users, upgrades
import json

app = Flask(__name__)
socketio = SocketIO(app)

def run():
  app.secret_key = 'hi'
  socketio.run(app, debug = True)

@app.route('/game/')
def game():
  return render_template('game.html',
                         healthOldSkill = upgrades.health(0),
                         healthCost=upgrades.cost(0),
                         healthNewSkill= upgrades.health(0+1),
                         speedOldSkill = upgrades.speed(0),
                         speedCost=upgradesspeed.cost(0),
                         speedNewSkill= upgrades.speed(0+1),
                         atkspdOldSkill = upgrades.shootSpeed(0),
                         atkspdCost=upgrades.cost(0),
                         atkspdNewSkill= upgrades.shootSpeed(0+1),
                         shootdmgOldSkill = upgrades.health(0),
                         shootdmgCost=upgrades.cost(0),
                         shootdmgNewSkill= upgrades.shootDamage(0+1),
                         meleedmgOldSkill = upgrades.meleeDamage(0),
                         meleedmgCost=upgrades.cost(0),
                         meleedmgNewSkill= upgrades.meleeDamage(0+1),
                         meleesizeOldSkill = upgrades.meleeRange(0),
                         meleeSizeCost=upgrades.cost(0),
                         meleesizeNewSkill= upgrades.meleeRange(+1)
                         )

@socketio.on('get_room')
def sendRoom():
  room = level.Room().asDict()
  emit('new_room', room)

@socketio.on('upgradePlayers')
def upgrades(data):
  skills = data['upgrades']
  print skills
  
@socketio.on('save_room')
def saveRoom(data):
  player = data['player']
  room = data['room']
  room = json.dumps(room)
  xcor = player['x']
  ycor = player['y']
  if xcor < 100 and ycor > 300 and ycor < 400:
    door = 1
  elif xcor > 580 and ycor > 300 and ycor < 400:
    door = 3
  elif ycor < 100 and xcor > 300 and xcor < 400:
    door = 2
  else:
    door = 4
  print room
  print session['username']
  print door
  print player
  #save.door(player, room, session['username'])
  #save.leaveroom(session['username'], room) #this is 'current lvl', update its room in the db
  #enterroom = save.checkdoor(session['username'], room, door)
  #if enterroom != -1: check if the exit door has been used
  #if so load level the level and set the current level to that id
  #oldroomstuff = enterOld(session['username'], enterroom)
  #otherwise generate a new level and id, store them in the db
  #getLevel(newlevel), and update currentroom
  
#login
@app.route('/')
def root():
  if 'username' in session.keys():
    return redirect(url_for('game'))
  
  return redirect(url_for('login'))

@app.route('/login/')
def login():
  if 'username' in session:
    return redirect(url_for('game'))
    
  return render_template('login.html')

@app.route('/authenticate/', methods = ['POST'])
def authenticate():
  pw = request.form['pass']
  un = request.form['user']
  text = users.login(un,pw)#error message
  
  if text == '':#if no error message, succesful go back home
    session['username'] = un
    return redirect(url_for('game'))
    
  return render_template('login.html', message = text)

@app.route('/register/', methods=['POST'])
def register():
  pw = request.form['pass']
  un = request.form['user']
  pw2 = request.form['passconf']
  
  if pw2 == pw:
    regRet = users.register(un,pw)#returns an error/success message
    return render_template('login.html', message = regRet)

  return render_template('login.html', message = 'Passwords don\'t match')
    
@app.route('/logout/')
def logout():
  session.pop('username')
  return redirect(url_for('root'))
  
if __name__ == '__main__':
  run()
