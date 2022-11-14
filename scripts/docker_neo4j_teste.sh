docker run -p 7474:7474 -p 7687:7687 --volume=$HOME/graph_data/data:/data \
  --volume=$HOME/graph_data/gameofthrones/data:/var/lib/neo4j/import \
  --env NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
  --env apoc.import.file.enabled=true \
  --env NEO4J_AUTH=neo4j/1234 \
  neo4j:4.4.9-community