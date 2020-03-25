import json
from channels import Group
# from channels.auth import channel_session_user, channel_session_user_from_http


# @channel_session_user_from_http
def ws_connect(message):
    Group('turnos').add(message.reply_channel)
    Group('turnos').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })


# @channel_session_user
def ws_disconnect(message):
    Group('turnos').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('turnos').discard(message.reply_channel)