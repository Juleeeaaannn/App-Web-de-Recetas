import hashlib
if __name__ == "__main__": 
    # cifrado de la clave utilizando md5  	    
    clave = 'julia459' 
    result = hashlib.md5(bytes(clave, encoding='ansi')) 
    # muestra la clave cifrada en hexadecimal, esta es la que se guarda en base de datos 
    print(result.hexdigest()) 
