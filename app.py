from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from method import methodCesar, decryptCesar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

#Llamada front 
@app.route('/')
def main():
    #Buscando archivo para renderizar  
    return render_template('main.html')

#---------------------------
#Función que se ejcutará 
@app.route('/chatOnline', methods=['POST'])
def chatOnline():
    #Accede a parámetros enviados
    #Mediante el valor del campo 
    nameUser = request.form['nameUser']
    #Asignación de la variable 
    typeEncryption = request.form['typeEncryption']
    
    #Almacena valores en el objeto session 
    session['nameUser'] = nameUser
    session['typeEncryption'] = typeEncryption
    #Futuras solicitudes
    
    return render_template('chat.html', nameUser=nameUser, typeEncryption=typeEncryption)

#---------------------------
@socketio.on('message')
def receive(data):
    nameUser = session.get('nameUser', 'Invitado')

    clave = int(session.get('typeEncryption', '0'))  # Obtener la clave del tipo de cifrado
    messageEncryption = methodCesar(data['message'], clave)

    print(f'Received message from {nameUser}: {data["message"]}')
    print(f'Mensaje cifrado: {messageEncryption}')

    # Emitir el mensaje cifrado y descifrado
    socketio.emit('message', {'cifrado': f'Cifrado: {messageEncryption}', 'descifrado': f'decifrada: {data["message"]}'})

#----------------------------
@socketio.on('descifrar')
def descifrar(data):
    nameUser = session.get('nameUser', 'Invitado')

    # Obtén el mensaje cifrado y la clave de descifrado
    mensaje_completo = data.get('mensajeCifrado', '')
    clave_descifrado = int(data.get('claveDescifrado', 0))

    # Extraer el mensaje cifrado de la parte "Usuario: Mensaje cifrado"
    _, mensaje_cifrado = mensaje_completo.split(': ', 1)  # Divide en dos partes, solo 1 vez

    try:
        # Descifrar el mensaje
        mensaje_descifrado = decryptCesar(mensaje_cifrado, clave_descifrado)
        mensaje_resultado = f'decifrada: {mensaje_descifrado}'
    except ValueError:
        # La clave es incorrecta, mostrar la palabra sin cambios
        mensaje_resultado = f'aun no decifrada: {mensaje_cifrado}'

    print(f'Descifrado del mensaje de {nameUser}: {mensaje_resultado}')

    # Emitir el mensaje descifrado
    socketio.emit('descifrado', {'descifrado': f'{mensaje_resultado}'})

if __name__ == '__main__':
    #Ejecutar la apliacion en el puerto predeterminado por Socketio
    socketio.run(app)
