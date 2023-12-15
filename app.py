# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from method import methodCesar, decryptCesar

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Clave secreta para manejar sesiones de usuario
socketio = SocketIO(app)

# Definir la ruta principal que renderiza el archivo 'main.html'
@app.route('/')
def main():
    return render_template('main.html')

# Ruta para gestionar la entrada al chat
@app.route('/chatOnline', methods=['POST'])
def chatOnline():
    nameUser = request.form['nameUser']
    typeEncryption = request.form['typeEncryption']
    
    # Almacenar valores en el objeto de sesión para mantener la información del usuario
    session['nameUser'] = nameUser
    session['typeEncryption'] = typeEncryption
    
    # Renderizar la plantilla 'chat.html' con la información del usuario
    return render_template('chat.html', nameUser=nameUser, typeEncryption=typeEncryption)

# En el servidor, en la función receive
@socketio.on('message')
def receive(data):
    nameUser = session.get('nameUser', 'Invitado')
    clave = int(session.get('typeEncryption', '0'))

    # Aplicar cifrado César al mensaje recibido
    messageEncryption = methodCesar(data['message'], clave)

    print(f'Received message from {nameUser}: {data["message"]}')
    print(f'Mensaje cifrado: {messageEncryption}')

    # Emitir el mensaje cifrado y descifrado al destinatario correcto
    destination_chat = 2 if data['chatNumber'] == 1 else 1

    socketio.emit('message', {
        'cifrado': f'Cifrado: {messageEncryption}',
        'descifrado': f'Descifrado: {data["message"]}',
        'chatNumber': destination_chat
    })


# En el servidor, en la función descifrar
@socketio.on('descifrar')
def descifrar(data):
    nameUser = session.get('nameUser', 'Invitado')

    mensaje_cifrado = data.get('mensajeCifrado', '')
    clave_descifrado = int(data.get('claveDescifrado', 0))
    chatNumber = data.get('chatNumber', 0)

    try:
        mensaje_descifrado = decryptCesar(mensaje_cifrado, clave_descifrado)
        mensaje_resultado = f'Descifrado: {mensaje_descifrado}'
    except ValueError:
        mensaje_resultado = f'Aun no descifrada: {mensaje_cifrado}'

    print(f'Descifrado del mensaje de {nameUser}: {mensaje_resultado}')

    # Emitir el mensaje descifrado al destinatario correcto
    socketio.emit('descifrado', {
        'descifrado': mensaje_resultado,
        'chatNumber': chatNumber
    })

# Ejecutar la aplicación con SocketIO en el puerto predeterminado
if __name__ == '__main__':
    socketio.run(app)