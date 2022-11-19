import pandas as pd
from src.db import Db
from sqlalchemy import create_engine
import requests

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
    print('----- resultado ----')
    print('nome do socio', nome)
    print('resposta', response.json())
    print('----- resultado ----')
    return (response.json(), response.status_code)
    
def buscar_dados_com_neo4j(nome: str):
    db = Db()
    print(db.session)
    resp = db.return_data_by_name(nome)
    print(resp)
    
    db.close()
    
def busca_socios_na_base_offshores(conn, n_socios=None):
    query_conncat = ''
    cont_resp = 0
    if n_socios:
        query_conncat = f' LIMIT {str(n_socios)}'
    query = f'SELECT nome FROM cnpj_socios'+ query_conncat
    print(query)
    df = pd.read_sql_query(query, con=conn)
    for index, row in df.iterrows():
        socio = row['nome']
        res, status_code = buscar_dados_com_api(socio)
        if status_code == 400:
            continue
        print(res)

        # if res['results']:
        #     cont_resp+=1
        #     if cont_resp == 10:
        #         break
        del res
    del df    

if __name__ == '__main__':
    
    
    pg_conn = postgres_conn()
        
    # testando query neo4j
    # print('testando query neo4j')
    # buscar_dados_com_neo4j('Ross,Jr. - Wilbur Louis')
    
    # testando api
    print('testando api')
    
    for socio in ('JOSE FLAKSBERG', ):
        res, _ = buscar_dados_com_api(socio)
        print(res)
        
    # busca_socios_na_base_offshores(pg_conn)
    