import os
import platform
import sys
import shutil
from threading import Semaphore
from time import sleep


if platform.system()=='Windows':
    PLATFORM=True
    import msvcrt
    semaphore = Semaphore()
    ROOT = 'C:\\'
else:
    PLATFORM=False
    ROOT = '/'
    import fcntl
    semaphore = Semaphore()


def block_access(file=None,command=None,function=None):
    ##semaphore.acquire()
    try:
        if PLATFORM:
            file = open(file, 'r+')
            msvcrt.locking(file.fileno(), msvcrt.LK_RLCK, 1)
            function(command)
        else:
            file = open(file, 'r+')
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            function(command)
    except Exception as e:
        print('Ja exite um processo acessando este arquivo', e)
    finally:
        if PLATFORM:
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
            file.close()
        else:
            fcntl.flock(file, fcntl.LOCK_UN)
            file.close()
        ##semaphore.release()
        sleep(1)


def ver():
    #Exibe versão
    print(platform.system())


def dir(command):
    #Lista o conteúdo do diretório
    if PLATFORM:
        os.system('dir {0}'.format(command))
    else:
        os.system('ls {0}'.format(command))


def exit():
    #Finalizar o interpretador de comandos
    sys.exit(0)


def mkdir(path):
    #Criar um diretório
    os.mkdir(path)


def rmd(path):
    #Apaga o diretório
    os.rmdir(path)

def rma(path):
    #Apaga um arquivo
    os.remove(path)

def mv(path):
    #Modificar o nome no arquivo
    shutil.move(path[1],path[2])


def cp(path):
    #Copiar um arquivo para outro diretório
    shutil.copy(path[1],path[2])


def cat(path):
    #Exibe o conteúdo de um arquivo
    file = open(path, 'r+')
    print(file.read())
    file.close()


def edit(path):
    #Permite editar um arquivo de texto
    if PLATFORM:
        os.system('notepad {0}'.format(path))
    else:
        os.system('nano {0}'.format(path))


def cd(path):
    #Muda de diretório
    os.chdir(path)


def current_dir():
    #Exibe diretório atual
    return os.getcwd()


while True:
    try:
        if current_dir == ROOT:
            command = input('> ')
        else:
            command = input('{0}/> '.format(current_dir().replace('\\','/').replace('C:/','')))

        if command.split(' ')[0]=='dir':
            dir(command.split(' ')[1])

        elif command.split(' ')[0]=='exit':
            exit()

        elif command.split(' ')[0]=='mkdir':
            mkdir(command.split(' ')[1])

        elif command.split(' ')[0]=='rm' and command.split(' ')[1]=='-r':
            block_access(command=command.split(' ')[2], function=rmd,file=command.split(' ')[2])

        elif command.split(' ')[0]=='rm' and command.split(' ')[1]=='-a':
            block_access(command=command.split(' ')[2], function=rma,file=command.split(' ')[2])

        elif command.split(' ')[0]=='mv':
            block_access(command=command.split(' '), function=mv,file=command.split(' ')[1])

        elif command.split(' ')[0]=='cp':
            block_access(command=command.split(' '), function=cp,file=command.split(' ')[1])

        elif command.split(' ')[0]=='cat':
            block_access(command=command.split(' ')[1], function=cat,file=command.split(' ')[1])

        elif command.split(' ')[0]=='edit':
            block_access(command=command.split(' ')[1], function=edit,file=command.split(' ')[1])

        elif command.split(' ')[0]=='cd':
            cd(command.split(' ')[1])

        else:
            print(command.split(' ')[0],' Comando não foi encontrado.')

    except PermissionError as e:
        pass
    except Exception as e:
        pass
    except KeyboardInterrupt as e:
        pass

