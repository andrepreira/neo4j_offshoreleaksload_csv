from typing import List
import pandas as pd
import requests
import csv
from sqlalchemy import create_engine

from src.db import Db

POSTGRES_ADDRESS = 'localhost' ## INSERT YOUR DB ADDRESS IF IT'S NOT ON PANOPLY
POSTGRES_PORT = '5420'
POSTGRES_USERNAME = 'postgres' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES USERNAME
POSTGRES_PASSWORD = 'jNhL55q' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES PASSWORD
POSTGRES_DBNAME = 'invista_fidc' ## CHANGE THIS TO YOUR DATABASE NAME

def postgres_conn():
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
    .format(username=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    ipaddress=POSTGRES_ADDRESS,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DBNAME))
    return create_engine(postgres_str)

def buscar_dados_com_api(nome: str):
    payload = dict({'nome': nome})
    response = requests.get("http://localhost:5000/dados_offshores", params=payload)
    # print('----- resultado ----')
    # print('nome do socio', nome)
    # print('resposta', response.json())
    # print('----- resultado ----')
    return (response.json(), response.status_code)
    
def buscar_dados_com_neo4j(nome: str):
    db = Db()
    print(db.session)
    resp = db.return_data_by_name(nome)
    print(resp)
    
    db.close()

def busca_nomes_socios_postgresql(conn, n_socios=None) -> list:
    query_conncat = ''
    if n_socios:
        query_conncat = f' LIMIT {str(n_socios)}'
    query = f'SELECT nome FROM cnpj_socios'+ query_conncat
    print(query)
    print('Usando base psql..')
    df = pd.read_sql_query(query, con=conn)
    return [socio for socio in df['nome']]

def busca_nomes_socios_csv(path: str) -> list:
    print('Usando base csv..')
    nomes = []
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        for nome in csvreader:
            nomes.append(nome)
    return nomes
    
def busca_dados_socios_na_base_offshores(nome_base='csv', n_socios=None) ->List[dict]:
    base_psql = False
    print('Iniciando busca..')
    if nome_base == 'csv':
        socios = busca_nomes_socios_csv('./socios_cnpj.csv')
    elif nome_base == 'psql':
        base_psql = True
        conn = postgres_conn()
        socios = busca_nomes_socios_postgresql(conn, n_socios)
    else:
        raise Exception('Base incorreta, escolha a nome_base= psql ou csv')
    
    retorno = []
    cont_resp = 0
    print(type(n_socios))
    for socio in socios:
        if type(n_socios) == int and cont_resp == n_socios:
            break
        res, status_code = buscar_dados_com_api(socio)
        if status_code == 400 or len(res) == 0:
            continue
        
        if base_psql:
            print('sócio da base psql com dados offshores ',socio)
            retorno.append({'socio': socio, 'dados': res})
            if cont_resp == n_socios:
                print(f'{cont_resp} primeiros resultados encontrados')
                break
        elif not base_psql:
            retorno.append({'socio': socio, 'dados': res})
        del res
   
        cont_resp+=1
    return retorno
if __name__ == '__main__':
    
    
    # testando query neo4j
    # print('testando query neo4j')
    # buscar_dados_com_neo4j('JOSE FLAKSBERG')
    
    # testando api
    print('testando api')
    
    # for socio in ('JOSE FLAKSBERG', ):
    #     res, _ = buscar_dados_com_api(socio)
    #     print(res)
        
    ret = busca_dados_socios_na_base_offshores('csv', n_socios=5)
    print('-----------Lista sócios------------------')
    # for dict_ret in ret:
    #     print(dict_ret['socio'])
        
    print('-----------Lista dados encontrados------------------')
    with open('./resultados.txt', 'w') as f:
        for dict_ret in ret:
            # print(dict_ret['dados'])
            f.write(str(dict_ret['dados'])+'\n')
    