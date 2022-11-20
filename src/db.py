from neo4j import GraphDatabase

NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "5692132"
NEO4J_URI = "neo4j://localhost:7687"

class Db:
    def __init__(self):
       self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
       self.session = self.driver.session(database='database')
    
    def close(self):
        
        return self.driver.close()
    
    @staticmethod
    def _query_run(tx, query, **kwargs):
        return tx.run(query, **kwargs).data()
    
    def return_data_by_name(self, name) -> list:
        query =  '''MATCH p = (a:Officer {name:$name})-[r]-(b)
        RETURN
        a.name as socio_investigado,  
        r.link as relacionamento,
        b.name as nome, 
        b.original_name as nome_orinal,
        b.address as endereco,
        b.countries as pais,
        b.country_codes as codigo_pais,
        b.sourceID as sourceID,
        b.jurisdiction_description as jurisdicao,
        b.lastEditTimestamp as timestamp_ultima_edicao'''
        
        results =  self.session.read_transaction(self._query_run, query=query,name=name)
        
        return results
    
    def is_created(self,db_name) -> bool:
        print(db_name)
        query = f'''SHOW DATABASE {db_name}'''
        print(query)
        
        return bool(self.session.read_transaction(self._query_run, query=query,db_name=db_name))
    
    def is_populated(self) -> bool:
        query = '''MATCH (n) return n LIMIT 5'''
        return bool(self.session.read_transaction(self._query_run, query=query))