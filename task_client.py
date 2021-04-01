import hashlib
import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)

while True:
    try:
        port = int(input('Введите номер порта: '))
        host = input('Введите хост: ')
        print("Соединение с сервером", file=open("log.txt", "a"))
        sock.connect((host, port))
        break
    except socket.gaierror:
        host='10.38.201.235'
        port=9090
        print(f'Введены неверные данные, использую настройки по умолчанию:\nhost: {host} \nport: {port}')
        try:
            sock.connect((host, port))
            break
        except ConnectionRefusedError:
            print('Подключение c настройками по умолчанию не установлено, попробуйте ещё раз с другими настройками.')
    except ValueError:
        print('Вводите корректные данные! Порт должен быть числом')
    except ConnectionRefusedError:
        print('Подключение не установлено, попробуйте ещё раз.')
    except TimeoutError:
        print('Подключение не установлено, от другого компьютера за требуемое время не получен отклик, попробуйте ещё раз.')

data = sock.recv(1024).decode()
if 'Введите своё имя:' in data:
    print(data)
    name = input('Имя: ')
    sock.send(name.encode())
    print(sock.recv(1024).decode())
    pswd = input('Пароль: ')
    md5_pswd=hashlib.md5(pswd.encode()).hexdigest()
    sock.send(md5_pswd.encode())
    print(sock.recv(1024).decode())
else:
    print(data)
    while True:
        pswd = input('Пароль: ')
        md5_pswd=hashlib.md5(pswd.encode()).hexdigest()
        sock.send(md5_pswd.encode())
        data = sock.recv(1024).decode()
        if '<passwd_true>' in data:
            break
        else:
            print(data)
while True:
    msg = input('Введиты строку для передачи или exit для выхода: ')
    if msg == 'exit':
        break
    print("Отправка данных серверу", file=open("log.txt", "a"))
    sock.send(msg.encode())

    print("Прием данных от сервера", file=open("log.txt", "a"))
    data = sock.recv(1024)
    print(data.decode())

print("Разрыв соединения с сервером", file=open("log.txt", "a"))