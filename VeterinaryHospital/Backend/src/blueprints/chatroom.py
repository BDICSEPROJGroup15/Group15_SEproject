from flask import Blueprint, render_template, session, flash, redirect,request
from flask_socketio import emit
from src.extension import socketio
from src.Models.Messages import Message
from src.Models.Users import User
from src.Utility.utilize import current_user,registeredAdmin
from src.extension import db


chatroom=Blueprint('chat',__name__)

online_users=[]



@chatroom.route("/chatroom", methods=['GET', 'POST'])
def admin():
    if not session.get("USERNAME") is None:
        number = registeredAdmin()
        return render_template('chatroom.html',adminnumber = number)
    else:
        flash("User needs to either login or sign up first")
        return redirect('auth.login')

@socketio.on("new message")
def new_message(message_body):
    message=Message(user=current_user(),body=message_body)
    db.session.add(message)
    print(message)
    db.session.commit()
    emit('new message',
             {'message_back':'{}'.format(message.body),
              'user_name':'{}'.format(message.user)},boardcast=True)


@socketio.on('connect')
def connect():
    global online_users
    user = current_user()
    if user.confirmed and user.id not in online_users:
        online_users.append(user.id)
    emit({'user count':len(online_users)},broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global online_users
    user = current_user()
    if user.confirmed and user.id in online_users:
        online_users.remove(user.id)
    emit('user count',{'count':len(online_users)},broadcast=True)