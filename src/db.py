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
        query =  '''MATCH (a:Officer {name:$name})-[r:officer_of|intermediary_of|registered_address*..10]-(b)
        RETURN b.name as name LIMIT 20'''
        
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