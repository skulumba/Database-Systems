
from neo4j_utils import Neo4jConnection
    
conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", password="")
q  = "MATCH (f:FACULTY) WHERE f.position ='Assistant Professor' RETURN count(f) AS num_assistant_professors"
result = conn.query(q,db='academicworld')
print(result)

