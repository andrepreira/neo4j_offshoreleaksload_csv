import os
from flask import Flask, request
from flask_restful import Resource, Api

try:
    from src.db import Db
except ModuleNotFoundError:
    from db import Db
    
app = Flask(__name__)
api = Api(app)

class DadosOffshores(Resource):
    
    def get(self):
        nome = request.args.get('nome', None)
                
        database = Db()
        if not isinstance(database, Db):
            exit('falha na conexao com o neo4j !')
            
        results = database.return_data_by_name(name=nome)
                
        if nome is None:
            return {},400
        
        return results, 200

api.add_resource(DadosOffshores, '/dados_offshores')

if __name__ == '__main__':
    #define the localhost ip and the port that is going to be used
    # in some future article, we are going to use an env variable instead a hardcoded port 
    app.run(host='0.0.0.0', port=os.getenv('PORT'),debug=True)