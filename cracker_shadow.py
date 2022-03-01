import crypt, argparse

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CIAN = '\033[36m'
END = '\033[37m'


def cracker_shadow(args):
    wordlist = open(args.wordlist).readlines()
    salt = tratar_str(args.salt)
    shadow = tratar_str(args.hash)
    
    print(f'\n{BLUE}[+] PROCESSO INICIADO{END}\n')
    print(salt)
    print(shadow)
    for w in wordlist:
        word = tratar_str(w)
        print(f'{YELLOW}[*] TESTANDO => {word}{END}')
        result = crypt.crypt(word, salt)
        if result == shadow:
            print(f'\n{CIAN}[+] SENHA ENCONTRADA:\n\n\t=> {word}{END}')
            break
    

def tratar_str(texto):
    return texto.replace('\n', '').replace(' ', '')

def cabecalho():
    print(f'\n\t{YELLOW}{"#" * 50}\n\t#{" " * 15}{GREEN}CRACK THE HASH SHADOW{" " * 12}{YELLOW}#\n\t{"#" * 50}{END}')

def init_args():
    parser = argparse.ArgumentParser(description="Exemplo: python3 cracker_shadow.py -w /path/wordlist -s '$1$admin$' -hash '$1$admin$Iv7IQmAby/cp05haguKYQ0'")
    parser.add_argument('-w','--wordlist', help='wordlist/passwords')
    parser.add_argument('-s','--salt', help='salt do hash')
    parser.add_argument('-hash', help='hash completo passwd')
    args = parser.parse_args()
    
    if args.wordlist and args.salt and args.hash:
        return args
    else:
        return None

def main():
    args = init_args()
    if args == None:
        print('\nUSE: python3 cracker_shadow.py --help\n')
    else:
        cabecalho()
        cracker_shadow(args)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'ERROR: {e}')