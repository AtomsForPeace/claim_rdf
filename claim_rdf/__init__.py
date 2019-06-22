#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: __init__.py

from typing import Optional, List, Dict
from uuid import uuid4
from aiosparql.client import SPARQLClient


PREFIXES = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""


class TooManyClaims(Exception):
    """
    Just in case for whatever reason multiple claims come up
    """
    pass


class Claim:
    """
    A claim has a source, subject, predicate and object.
    The source is where the information of the statement came from.
    """

    def __init__(self, sparql_client: SPARQLClient, uri: str) -> None:
        self.sparql_client = sparql_client
        self.uri = uri
        self._source = None
        self._subject = None
        self._predicate = None
        self._object = None

    async def _get_claim(self):
        claim = await get_claim(
            sparql_client=self.sparql_client,
            claim_uri=self.uri
        )
        self._source = convert_str_to_uri(claim.get('claim_source'))
        self._subject = convert_str_to_uri(claim.get('claim_subject'))
        self._predicate = convert_str_to_uri(claim.get('claim_predicate'))
        self._object = convert_str_to_uri(claim.get('claim_object'))

    async def get_source(self):
        if self._source:
            return self._source
        await self._get_claim()
        return self._source

    async def get_subject(self):
        if self._subject:
            return self._subject
        await self._get_claim()
        return self._subject

    async def get_predicate(self):
        if self._predicate:
            return self._predicate
        await self._get_claim()
        return self._predicate

    async def get_object(self):
        if self._object:
            return self._object
        await self._get_claim()
        return self._object


async def get_claim(
    sparql_client: SPARQLClient,
    claim_uri: str
) -> Dict:
    """
    Gets the source, subject, predicate and object of a given claim.
    """
    query_string = """
    {prefixes}

    SELECT *
    WHERE {{
      {claim_uri}   rdfs:isDefinedBy    ?claim_source       ;
                    a                   rdf:Statement       ;
                    rdf:subject         ?claim_subject      ;
                    rdf:predicate       ?claim_predicate    ;
                    rdf:object          ?claim_object       .
    }}
    """.format(
        prefixes=PREFIXES,
        claim_uri=claim_uri
    )
    claims = (await sparql_client.query(query_string))['results']['bindings']
    if len(claims) > 1:
        raise TooManyClaims(
            'Got too many claims ({amount}) for {claim}'.format(
                amount=len(claims), claim=claim_uri
            )
        )
    if len(claims) == 0:
        return None
    claim = claims[0]
    return {k: v['value'] for k, v in claim.items()}


async def get_claims(
    sparql_client: SPARQLClient,
    claim_source: Optional[str] = None,
    claim_subject: Optional[str] = None,
    claim_predicate: Optional[str] = None,
    claim_object: Optional[str] = None
) -> List[Claim]:
    """
    Gets all claims based on the source and/or any part of the statement or the
    entire statement.

    ie. You could get all claims from one source or one subject etc.
    """
    query_string = """
    {prefixes}

    SELECT *
    WHERE {{
      ?claim    rdfs:isDefinedBy    {claim_source}      ;
                a                   rdf:Statement       ;
                rdf:subject         {claim_subject}     ;
                rdf:predicate       {claim_predicate}   ;
                rdf:object          {claim_object}      .
    }}
    """.format(
        prefixes=PREFIXES,
        claim_source=claim_source or '?claim_source',
        claim_subject=claim_subject or '?claim_subject',
        claim_predicate=claim_predicate or '?claim_predicate',
        claim_object=claim_object or '?claim_object',
    )
    claims = (await sparql_client.query(query_string))['results']['bindings']
    return [
        Claim(
            sparql_client=sparql_client,
            uri=convert_str_to_uri(uri_string=claim['claim']['value'])
        )
        for claim in claims
    ]


# TODO: improve, find external library, or something
def convert_str_to_uri(uri_string: str) -> str:
    """
    A simple way of creating the URIs from strings
    """
    return '<' + uri_string + '>'


async def add_claim(
    sparql_client: SPARQLClient,
    claim_prefix: str,
    claim_source: str,
    claim_subject: str,
    claim_predicate: str,
    claim_object: str
):
    """
    Creates a claim by generating a URI for the claim and then adding it to the
    RDF store with the source, subject, predicate and object given.
    """
    claim_uri = '<' + claim_prefix + str(uuid4()) + '>'
    query_string = """
    {prefixes}

    INSERT DATA {{
      {claim_uri}   rdfs:isDefinedBy    {claim_source}      ;
                    a                   rdf:Statement       ;
                    rdf:subject         {claim_subject}     ;
                    rdf:predicate       {claim_predicate}   ;
                    rdf:object          {claim_object}      .
    }}
    """.format(
        prefixes=PREFIXES,
        claim_uri=claim_uri,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    await sparql_client.update(query_string)
    return Claim(sparql_client=sparql_client, uri=claim_uri)


async def remove_claims(
    sparql_client: SPARQLClient,
    claim_source: Optional[str] = None,
    claim_subject: Optional[str] = None,
    claim_predicate: Optional[str] = None,
    claim_object: Optional[str] = None
):
    """
    Removes all claims that satisfy the properties given. This can be as
    minimal as wished.

    ie. Delete all claims from a source or with one subject.
    """
    query_string = """
    {prefixes}

    DELETE WHERE {{
      ?claim    rdfs:isDefinedBy    {claim_source}      ;
                a                   rdf:Statement       ;
                rdf:subject         {claim_subject}     ;
                rdf:predicate       {claim_predicate}   ;
                rdf:object          {claim_object}      .
    }}
    """.format(
        prefixes=PREFIXES,
        claim_source=claim_source or '?claim_source',
        claim_subject=claim_subject or '?claim_source',
        claim_predicate=claim_predicate or '?claim_predicate',
        claim_object=claim_object or '?claim_object',
    )
    await sparql_client.update(query_string)
