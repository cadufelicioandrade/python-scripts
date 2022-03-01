import crypt, argparse

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
CIAN = '\033[36m'
YELLOW = '\033[33m'
END = '\033[37m'


def cracker_passwd(args):

    wordlist = open(args.wordlist).readlines()
    passlist = open(args.passlist).readlines()
    crackhash = args.crackhash
    typehash = int(args.typehash)
    stop = False
    print(f'\n{BLUE}[+] PROCESSO INICIADO{END}\n')
    for w in wordlist:
        try:
            word = tratar_str(w)
            salt = f'${typehash}${word}$'
            print(f'{YELLOW}[*] TESTANDO => {salt}{END}')
            for s in passlist:
                try:
                    password = tratar_str(s)
                    result = tratar_str(crypt.crypt(password, salt))
                    if result == tratar_str(f'{salt}{crackhash}'):
                        print(f'\n{CIAN}[+] ENCONTRADO:\n\nSENHA: {password}\nHASH: {result}{END}')
                        stop = True
                        break
                except:
                    continue
            if stop:
                break
        except:
            continue

def tratar_str(texto):
    return texto.replace('\n', '').replace(' ','')

def cabecalho():
    print(f'\n\t{YELLOW}{"#" * 50}\n\t#{" " * 15}{GREEN}CRACK THE HASH PASSWD{" " * 12}{YELLOW}#\n\t{"#" * 50}{END}')

    
def init_args():
    parser = argparse.ArgumentParser(description='Exemplo: python3 crack.py -wl /path/wordlist -pl /path/passlist -th 1 -ch wmbWtt7DyAOGN2wbyIljP.')
    parser.add_argument('-wl','--wordlist', help='Lista de palavras para salt.')
    parser.add_argument('-pl','--passlist', help='Lista de senhas.' )
    parser.add_argument('-th', '--typehash', type=int, choices=[1,5,6], help='Tipo de hash.')
    parser.add_argument('-ch', '--crackhash', help='Hash para quebrar.')
    args = parser.parse_args()
    
    if args.wordlist and args.passlist and args.typehash and args.crackhash:
        return args
    else:
        return None

def main():
    args = init_args()
    if args == None:
        print(f"{RED}\nCONSULTE:\npython3 crack.py --help\n{END}")
    else:
        cabecalho()
        cracker_passwd(args)


if __name__ == '__main__':
    try:
        main()   
    except Exception as e:
        print(f'Error: {e}')