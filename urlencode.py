import urllib.parse, argparse

def init_args():
    parser = argparse.ArgumentParser(description='python3 urlencode.py -u http:url.com -e 0')
    parser.add_argument('-u', '--urlencode', help='Url para encodar ou decodar')
    parser.add_argument('-e', '--encodar', choices=['0','1'], help='0 para decodar, 1 para encodar')
    args = parser.parse_args()

    if args.urlencode and args.encodar:
        return  args
    else:
        return None

def main():
    args = init_args()
    if args == None:
        print(f'\nConsulte: urlencode.py --help\n')
    else:
        if args.encodar == '0':
            print(urllib.parse.unquote(args.urlencode))
        elif args.encodar == '1':
            print(urllib.parse.quote(args.urlencode))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
