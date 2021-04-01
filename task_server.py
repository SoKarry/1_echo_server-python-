import pickle
import socket

users_file = open("users", "rb")
try:
	users = pickle.load(users_file)
except EOFError:
	users={}

users_pswd_file = open("users.pswd", "rb")
try:
	users_pswd = pickle.load(users_pswd_file)
except EOFError:
	users_pswd={}


print("Запуск сервера", file=open("log.txt", "a"))
sock = socket.socket()
port = 9090
while True:
	try:
		sock.bind(('', port))
		print(f'Слушаю порт {port}', file=open("log.txt", "a"))
		break
	except:
		port+=1

print("Начало прослушивания порта", file=open("log.txt", "a"))
sock.listen(0)
msg = ''

while True:
	conn, addr = sock.accept()
	print("Подключение клиента", file=open("log.txt", "a"))
	print(addr, file=open("log.txt", "a"))
	user_name = users.get(addr[0])
	if user_name and users_pswd.get(addr[0]):
		conn.send(f'Привет, {user_name}\nВведите Ваш пароль: '.encode())
		print(f'Подключился {user_name}, запрашиваю пароль', file=open("log.txt", "a"))
		while True:
			data = conn.recv(1024).decode()
			if data == users_pswd.get(addr[0]):
				conn.send('<passwd_true>'.encode())
				print(f'Клиент {user_name} Успешно вошёл!', file=open("log.txt", "a"))
				break
			else:
				print(f'Клиент {user_name} ввёл неверный пароль!', file=open("log.txt", "a"))
				conn.send(f'Неверный пароль, попробуйте ещё раз!'.encode())
	else:
		print(f'Подключился новый клиент, запрашиваю имя', file=open("log.txt", "a"))
		conn.send(f'Введите своё имя: '.encode())
		data = conn.recv(1024)
		users.setdefault(addr[0], data.decode())
		users_file = open("users", "wb")
		pickle.dump(users, users_file)
		users_file.close()
		print(f'Запрашиваю пароль', file=open("log.txt", "a"))
		conn.send(f'Придумайте пароль: '.encode())
		data = conn.recv(1024)
		users_pswd.setdefault(addr[0], data.decode())
		users_pswd_file = open("users.pswd", "wb")
		pickle.dump(users_pswd, users_pswd_file)
		users_pswd_file.close()
		print(f'Клиент {users.get(addr[0])} успешно зарегистрирован!', file=open("log.txt", "a"))
		conn.send(f'Привет, {users.get(addr[0])}'.encode())
	while True:
		print("Прием данных от клиента", file=open("log.txt", "a"))
		data = conn.recv(1024)
		if not data:
			break
		msg += data.decode()
		print("Отправка данных клиенту", file=open("log.txt", "a"))
		conn.send(data)
	print(msg, file=open("log.txt", "a"))
	print("Отключение клиента", file=open("log.txt", "a"))
	conn.close()