import os
from dotenv import load_dotenv
from gremlin_python.driver import client, serializer
 
load_dotenv()
 
gremlin_client = client.Client(
    os.getenv("COSMOS_ENDPOINT"),
    "g",
    username=f"/dbs/{os.getenv('COSMOS_DATABASE')}/colls/{os.getenv('COSMOS_GRAPH')}",
    password=os.getenv("COSMOS_KEY"),
    message_serializer=serializer.GraphSONSerializersV2d0()
)
 
 
# ------------------------------------------
# Create or get vertex (prevents 409 errors)
# ------------------------------------------
def create_entity_node(entity_id: str, entity_type: str, properties: dict):
    # Use fold().coalesce() pattern to avoid duplicate insert
    query = f"""
    g.V('{entity_id}')
      .fold()
      .coalesce(
          unfold(),
          addV('{entity_type}')
            .property('id', '{entity_id}')
            .property('pk', 'graph')
    """
 
    for key, value in properties.items():
        query += f".property('{key}', '{value}')"
 
    query += ")"
 
    callback = gremlin_client.submitAsync(query)
    callback.result()
 
 
# ------------------------------------------
# Create relationship safely
# ------------------------------------------
def create_relationship(from_id: str, to_id: str, relationship: str):
    query = f"""
    g.V('{from_id}')
     .as('a')
     .V('{to_id}')
     .coalesce(
         inE('{relationship}').where(outV().as('a')),
         addE('{relationship}').from('a')
     )
    """
 
    callback = gremlin_client.submitAsync(query)
    callback.result()
 
 
# ------------------------------------------
# Simple entity extraction (placeholder logic)
# ------------------------------------------
def extract_simple_entities(text: str):
    entities = []
 
    if "Company" in text:
        entities.append(
            ("Company_Company", "Company", {"name": "Company"})
        )
 
    if "Client" in text:
        entities.append(
            ("Client_Client", "Client", {"name": "Client"})
        )
 
    return entities
 
 
# ------------------------------------------
# Build graph once per document
# ------------------------------------------
def build_graph_from_chunk(text: str):
    entities = extract_simple_entities(text)
 
    for entity_id, entity_type, props in entities:
        create_entity_node(entity_id, entity_type, props)
 
    if len(entities) >= 2:
        create_relationship(
            entities[0][0],
            entities[1][0],
            "related_to"
        )