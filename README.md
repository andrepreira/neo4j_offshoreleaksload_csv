# NEO4J Offshoreleaks

Projeto criado para resolver o problema de imports dos dados de offshoreleaks. 

Esse projeto ira:
 
 - baixar o dump dos dados de offshoreleaks<br>
    bash ./scripts/dump.sh
 - subir api para conexão com o neo4j<br>
    sudo docker-compose up -d --build api (docker) <br>
    python src/api.py (local)
 - subir visualizador de logs (Opcional)<br>
    sudo docker-compose up -d --build dozzle
 - usar o arquivo socios_cnpj (nome_base = 'csv') para pesquisar dados de offshores<br>
    python test_api.py
 - outra possibilidade seria subir o banco de dados postgresql caso vc tenha dados de nomes de socios em um dump postgres (nome_base = 'psql')<br>



## Offshoreleaks

https://github.com/ICIJ/offshoreleaks-data-packages