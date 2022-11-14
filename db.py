from neo4j import GraphDatabase
from neo4j_backup import Extractor,Importer

NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "1234"
NEO4J_URI = "neo4j://localhost:7687"

NAME_EXEMPLE = 'Ross, Jr. - Wilbur Louis'

class Db:
    def __init__(self):
       self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
       self.session = self.driver.session(database='neo4j')
    
    def close(self):
        
        return self.driver.close()
    
    @staticmethod
    def _query_run(tx, query, **kwargs):
        return tx.run(query, **kwargs).data()
    
    def return_data_by_name(self, name) -> list:
        query =  '''MATCH (a:Officer {name:$name})-[r:officer_of|intermediary_of|registered_address*..10]-(b)
        RETURN b.name as name LIMIT 20'''
        results =  self.session.read_transaction(self._query_run, query=query,name=name)
        
        print(type(results))
        print(results)
        for record in results:
            print(record['name'])
        return results
    
    def is_created(self,db_name) -> bool:
        query = f'''SHOW DATABASE {db_name}'''
        
        return bool(self.session.read_transaction(self._query_run, query=query,db_name=db_name))
    
    def is_populated(self) -> bool:
        query = '''MATCH (n) return n LIMIT 5'''
        return bool(self.session.read_transaction(self._query_run, query=query))
    
    def load_csv(self,csv_name) -> bool:
        print(csv_name)
        query = f'''WITH "file:///got-s1-edges.csv" AS uri
                    LOAD CSV WITH HEADERS FROM uri AS row
                    MATCH (source:Character {id: row.Source})
                    MATCH (target:Character {id: row.Target})
                    MERGE (source)-[:SEASON1 {weight: toInteger(row.Weight)}]-(target)'''
        print(query)
    
    def return_data_by_name(self, name) -> list:
        query =  '''MATCH (a:Officer {name:$name})-[r:officer_of|intermediary_of|registered_address*..10]-(b)
        RETURN b.name as name LIMIT 20'''
        results =  self.session.read_transaction(self._query_run, query=query,name=name)
        
        print(type(results))
        print(results)
        for record in results:
            print(record['name'])
        return results