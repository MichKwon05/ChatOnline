abecedario = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def methodCesar(palabra, clave):
    palabra = palabra.lower()
    palabra_encriptada = ""
    for letra in palabra:
        if letra.isalpha():
            if letra in abecedario:
                indice_original = abecedario.index(letra)
                nueva_letra = abecedario[(indice_original + clave) % len(abecedario)]
                palabra_encriptada += nueva_letra
            else:
                palabra_encriptada += letra
        else:
            palabra_encriptada += letra
    return palabra_encriptada

def decryptCesar(palabra_encriptada, clave):
    palabra_descifrada = ""
    for letra in palabra_encriptada:
        if letra.isalpha():
            if letra in abecedario:
                indice_encriptado = abecedario.index(letra)
                nueva_letra = abecedario[(indice_encriptado - clave) % len(abecedario)]
                palabra_descifrada += nueva_letra
            else:
                palabra_descifrada += letra
        else:
            palabra_descifrada += letra
    return palabra_descifrada