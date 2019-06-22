# claim_rdf
A simple async library for handling claims in an RDF store

By using RDF, SPARQL, and [reification](https://www.w3.org/2001/sw/DataAccess/rq23/#queryReification) this library creates, removes and finds claims.

A claim is a subject, predicate, and object that have a source where this information comes from. 

## To install 
pip install git+https://github.com/AtomsForPeace/claim_rdf

## Documentation
```python
from claim_rdf import add_claim
sparql_client = SPARQLCLient('<your_sparql_endpoint>')

# Add a claim that my friend knows my other friend
await add_claim(
    sparql_client=sparql_client,
    claim_prefix='www.example.com/',
    claim_source='<www.example.com/reliable_source>',
    claim_subject='<www.example.com/my_friend>',
    claim_predicate='<http://xmlns.com/foaf/0.1/knows>'
    claim_object='<www.example.com/my_other_friend>'
)

# Who does my friend know?
claims = await get_claims(
    sparql_client=sparql_client,
    claim_subject='<www.example.com/my_friend>',
    claim_predicate='<http://xmlns.com/foaf/0.1/knows>'
)
she_knows = [await claim.get_object() for claim in claims]

print(she_knows)
['<www.example.com/my_other_friend>', ]
```

## To test
Have a test instance of a RDF store. Be aware that testing requires modification and deletion of the RDF store. Set the address of the RDF store in the testing.cfg. 

Run pytest tests/
