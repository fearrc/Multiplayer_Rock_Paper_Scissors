import socket
from _thread import *
import sys
from player import Player
import pickle
from game import Game


server = '192.168.1.3'
port = 9999

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	s.bind((server,port))
except socket.error as e:
	print(str(e))

try:
	s.listen(2) # Number of people connecting
	print("Waiting for a connection, Server Started")
except:
	pass


connected = set()
games = {}
idCount = 0




players = [Player(0,0,50,50,(255,0,0)),Player(100,100,50,50,(0,0,255))]
def threaded_client(conn,p,gameId): 

	global idCount
	conn.send(str.encode(str(p)))

	reply = ''
	while True:
		try:
			data = conn.recv(4096).decode()

			if gameId in games:
				game = games[gameId]

				if not data:
					break
				else:
					if data == "reset":
						game.resetWent()
					elif data != "get":
						game.play(p,data)

					reply = game
					conn.sendall(pickle.dumps(game))

			else:
				break
		except:
			break

	print("Lost Connection")
	try:
		del games[gameId]
		print("Closing Game ", gameId)
	except:
		pass

	idCount -= 1
	conn.close()

while True:
	try:
		conn,addr = s.accept()
		print("Connected to: ",addr)

		idCount += 1
		p = 0
		gameId = (idCount - 1) // 2
		if idCount % 2 == 1:
			games[gameId] = Game(gameId)
			print("Creating a new game...")
		else:
			games[gameId].ready = True
			p = 1		# player

		start_new_thread(threaded_client,(conn,p,gameId))
	except:
		break