from flask_socketio import SocketIO, join_room, leave_room, emit

# Creamos el objeto SocketIO suelto para que cualquiera lo pueda importar sin causar bucles
socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('join_order_chat')
def handle_join_order_chat(data):
    order_id = data.get('order_id')
    if order_id:
        room = f"order_{order_id}"
        join_room(room)
        print(f"[SOCKETIO] User joined room: {room}")
        emit('chat_system_message', {'message': f'Conectado ao chat do pedido #{order_id}'}, room=room)

@socketio.on('send_order_message')
def handle_send_order_message(data):
    order_id = data.get('order_id')
    sender = data.get('sender')  # 'client' o 'courier'
    text = data.get('text')
    if order_id and sender and text:
        room = f"order_{order_id}"
        msg_data = {
            'order_id': order_id,
            'sender': sender,
            'text': text,
            'timestamp': data.get('timestamp')
        }
        # Emitir a todos en la sala del pedido
        emit('receive_order_message', msg_data, room=room)
        print(f"[SOCKETIO] Message in {room} from {sender}: {text}")

