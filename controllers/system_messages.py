from jinja2 import Template
from flask import Blueprint, g

system_messages_blueprint = Blueprint('system_messages_blueprint', __name__)

@system_messages_blueprint.route("/system_messages", methods=['GET'])
def index():
    from models import System_message
    from consts import severity, severities
    from datetime import datetime

    messages = g._db.query(System_message).filter(System_message.user_id == g._user.id).all()
    unmodified = []
    for message in messages:
        if message.severity >= severity:
            unmodified.append(System_message(message.user_id, message.message, message.read, message.severity, message.timestamp, message.long_message, message.id))
        message.read = 1
        
    g._db.commit()
    template = g._env.get_template('system_messages.html')
    return template.render(user=g._user, count=len(messages), messages=unmodified, severities=severities, date_converter=datetime.fromtimestamp, listing_type=1)

@system_messages_blueprint.route("/system_messages/", methods=['COUNT'])
def total_count():
    from models import System_message
    from consts import severity 

    total_count = g._db.query(System_message).filter(System_message.user_id == g._user.id).filter(System_message.severity >= severity).count()
    return str(total_count)


@system_messages_blueprint.route("/system_messages/<int:id>", methods=['GET'])
def get(id):
    from models import System_message
    message = g._db.query(System_message).filter(System_message.user_id == g._user.id).filter(System_message.id == id).first()
    if message is not None:
        return message.long_message
    return 'Not Found', 404


@system_messages_blueprint.route("/system_messages/", methods=['DELETE'])
def delete_all():
    from models import System_message
    messages = g._db.query(System_message).filter(System_message.user_id == g._user.id).all()
    if messages is not None:
        for message in messages:
            g._db.delete(message)
        g._db.commit()
        return 'OK'
    return 'Not Found', 404



@system_messages_blueprint.route("/system_messages/<int:id>", methods=['DELETE'])
def delete(id):
    from models import System_message
    message = g._db.query(System_message).filter(System_message.user_id == g._user.id).filter(System_message.id == id).first()
    if message is not None:
        g._db.delete(message)
        g._db.commit()
        return 'OK'
    return 'Not Found', 404

    