import configparser
import getpass
import os
import platform
import subprocess
import time
from pathlib import Path
from colorama import Fore
from threading import BoundedSemaphore, Lock, RLock
from interface import ICommand
import fcntl


if platform.system() == "Windows":
    PLATFORM = True
    ROOT = "C:\\"
else:
    PLATFORM = False
    ROOT = "/"


class CommandInterpreter(ICommand):

    def __init__(self):
        print("Welcome {0}".format(getpass.getuser()))
        parser = configparser.RawConfigParser()
        parser.read('shell/shell_setting.ini', encoding='utf-8')
        for k, v in parser['banner'].items():
            print(Fore.LIGHTBLUE_EX + v)
            time.sleep(0.1)

    def dir(self, *args):
        global semaphore
        semaphore.acquire()
        command = args[0].split(' ')
        if len(command) <= 1:
            print("\tDiretório {0}\n".format(os.path.abspath('.')))
            print("\tName: \n")
            for file in os.listdir(os.path.abspath('.')):
                print("\t", file)
        else:
            print("\tDiretório {0}\n".format(os.path.abspath(command[1])))
            print("\tName: \n")
            for file in os.listdir(os.path.abspath(command[1])):
                print("\t", file)
        semaphore.release()

    def cat(self, *args):
        with open(args[0].split(' ')[1], 'r', encoding='utf-8') as file:
            for line in file.readlines():
                print(line)

    def edit(self, *args):
        global semaphore
        semaphore.acquire()
        file = open(os.path.join(os.getcwd(), args[0].split(' ')[1]), 'r+', encoding='utf-8')
        try:
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            os.system("mousepad {0}".format(os.path.join(os.getcwd(), args[0].split(' ')[1])))
        except Exception as e:
            print('O arquivo está sendo editado por outro processo.')
        finally:
            fcntl.flock(file, fcntl.LOCK_UN)
            file.close()
            semaphore.release()
            time.sleep(1)

    def exit(self, *args):
        exit(0)

    def clear(self):
        if PLATFORM:
            os.system("cls")
        else:
            os.system("clear")

    def cd(self, *args):
        global semaphore
        base = args[0].split(' ')
        if Path(base[1]).is_dir():
            semaphore.acquire()
            if base[1] == '/':
                os.chroot(os.path.abspath(ROOT))
                return ROOT
            os.chdir(os.path.abspath(base[1]))
            semaphore.release()
            return os.path.abspath(os.getcwd()).replace('\\', '/')
        return os.path.abspath(os.getcwd()).replace('\\', '/')

    def mkdir(self, *args):
        for arg in args[0].split(' ')[1:]:
            os.mkdir(arg)

    def rm_d(self, *args):
        if PLATFORM:
            if len(args[0].split(' ')) >= 2:
                for arg in args[0].split(' ')[2:]:
                    os.system("del {0}".format(arg))
        else:
            if len(args[0].split(' ')) >= 2:
                for arg in args[0].split(' ')[2:]:
                    os.system("rm -r {0}".format(arg))

    def mv(self, *args):
        if len(args[0].split(' ')) >= 2:
            if PLATFORM:
                print(args[0].split(' ')[1], args[0].split(' ')[2])
                os.system("move {0} {1}".format(args[0].split(' ')[1],
                                                args[0].split(' ')[2]))
            else:
                os.system("mv {0} {1}".format(args[0].split(' ')[1],
                                                args[0].split(' ')[2]))

    def cp(self, *args):
        raise NotImplementedError

    def rm_a(self, *args):
        if PLATFORM:
            if len(args[0].split(' ')) >= 2:
                for arg in args[0].split(' ')[2:]:
                    os.system("del {0}".format(arg))
        else:
            if len(args[0].split(' ')) >= 2:
                for arg in args[0].split(' ')[2:]:
                    os.system("rm -r {0}".format(arg))

    def ver(self, *args):
        print(platform.version())
        semaphore.release()

    def start(self):
        global semaphore
        current_dir = ROOT
        root = ROOT
        os.chdir(os.path.dirname(ROOT))
        while True:
            try:
                if current_dir == root or current_dir == '' or current_dir == '/' or current_dir == 'C:/':
                    command = input(Fore.LIGHTGREEN_EX + '/> ')
                else:
                    command = input(Fore.LIGHTGREEN_EX + '{0}> '.format(current_dir).replace('C:/', '/'))
                if len(command.split(' ')) > 1 and 'cd' in command:
                    current_dir = self.cd(command)
                elif command == 'exit':
                    self.exit()
                elif 'dir' == command.split(' ')[0]:
                    self.dir(command)
                elif command == 'ver':
                    semaphore.acquire()
                    self.ver()
                elif PLATFORM and command == "cls":
                    self.clear()
                elif not PLATFORM and command == "clear":
                    self.clear()
                elif "mkdir" == command.split(' ')[0]:
                    self.mkdir(command)
                elif "cat" == command.split(' ')[0]:
                    self.cat(command)
                elif "rm" == command.split(' ')[0] and "-r" == command.split(' ')[1]:
                    self.rm_d(command)
                elif "rm" == command.split(' ')[0] and "-a" == command.split(' ')[1]:
                    self.rm_a(command)
                elif "mv" == command.split(' ')[0]:
                    self.mv(command)
                elif "edit" == command.split(' ')[0]:
                    try:
                        self.edit(command)
                    except Exception as e:
                        print(f"Erro inesperado {e}")
                else:
                    print(command.split(' ')[0:2])
                    print(Fore.RED + " '{0}' is not recognized by the system.".format(command))
                    print(Fore.RESET)
            except FileNotFoundError as e:
                print(e)
            except KeyboardInterrupt as e:
                pass
            except OSError as e:
                pass


semaphore = BoundedSemaphore(1)
if __name__ == '__main__':
    command_interpreter = CommandInterpreter()
    command_interpreter.start()
