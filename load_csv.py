from db import Db

if __name__ == '__main__':
    db = Db()
    if not db.is_created('neo4j'):
        exit('problemas na conexão com o neo4j !')
    
    db.load_csv()
    