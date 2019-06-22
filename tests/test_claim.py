#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: test_claim.py

import pytest
from aiosparql.client import SPARQLClient

from claim_rdf import Claim, get_claims, add_claim, remove_claims


@pytest.mark.asyncio
async def test_get_claims(sparql_client: SPARQLClient, truncate_sparql: None):
    claim_prefix = 'http:test.com/'
    claim_source = '<http:test.com/claim_source>'
    claim_subject_1 = '<http:test.com/claim_subject_1>'
    claim_predicate_1 = '<http:test.com/claim_predicate_1>'
    claim_object_1 = '<http:test.com/claim_object_1>'

    # add a claim to use for testing
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject_1,
        claim_predicate=claim_predicate_1,
        claim_object=claim_object_1,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject_1,
        claim_predicate=claim_predicate_1,
        claim_object=claim_object_1,
    )
    assert isinstance(claims, list)
    assert len(claims) == 1
    claim = claims[0]
    assert await claim.get_source() == claim_source
    assert await claim.get_subject() == claim_subject_1
    assert await claim.get_predicate() == claim_predicate_1
    assert await claim.get_object() == claim_object_1

    # add a second claim but with the same source
    claim_subject_2 = '<http:test.com/claim_subject_2>'
    claim_predicate_2 = '<http:test.com/claim_predicate_2>'
    claim_object_2 = '<http:test.com/claim_object_2>'
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject_2,
        claim_predicate=claim_predicate_2,
        claim_object=claim_object_2,
    )

    # search but only with the source to get both claims
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
    )
    assert isinstance(claims, list)
    assert len(claims) == 2


@pytest.mark.asyncio
async def test_add_claim(sparql_client: SPARQLClient, truncate_sparql: None):
    claim_prefix = 'http:test.com/'
    claim_source = '<http:test.com/claim_source>'
    claim_subject = '<http:test.com/claim_subject>'
    claim_predicate = '<http:test.com/claim_predicate>'
    claim_object = '<http:test.com/claim_object>'
    claim = await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    assert isinstance(claim, Claim)
    assert await claim.get_source() == claim_source
    assert await claim.get_subject() == claim_subject
    assert await claim.get_predicate() == claim_predicate
    assert await claim.get_object() == claim_object


@pytest.mark.asyncio
async def test_remove_claims_simple(
    sparql_client: SPARQLClient,
    truncate_sparql: None
):
    claim_prefix = 'http:test.com/'
    claim_source = '<http:test.com/claim_source>'
    claim_subject = '<http:test.com/claim_subject>'
    claim_predicate = '<http:test.com/claim_predicate>'
    claim_object = '<http:test.com/claim_object>'
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    assert len(claims) == 1
    await remove_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    assert len(claims) == 0


@pytest.mark.asyncio
async def test_remove_claims_source_only(
    sparql_client: SPARQLClient,
    truncate_sparql: None
):
    claim_prefix = 'http:test.com/'
    claim_source = '<http:test.com/claim_source>'
    claim_subject = '<http:test.com/claim_subject>'
    claim_predicate = '<http:test.com/claim_predicate>'
    claim_object = '<http:test.com/claim_object>'
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    assert len(claims) == 1
    await remove_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject,
        claim_predicate=claim_predicate,
        claim_object=claim_object,
    )
    assert len(claims) == 0


@pytest.mark.asyncio
async def test_remove_claims_multiple_claims(
    sparql_client: SPARQLClient,
    truncate_sparql: None
):
    claim_prefix = 'http:test.com/'
    claim_source = '<http:test.com/claim_source>'
    claim_subject_1 = '<http:test.com/claim_subject_1>'
    claim_predicate_1 = '<http:test.com/claim_predicate_1>'
    claim_object_1 = '<http:test.com/claim_object_1>'
    claim_subject_2 = '<http:test.com/claim_subject_2>'
    claim_predicate_2 = '<http:test.com/claim_predicate_2>'
    claim_object_2 = '<http:test.com/claim_object_2>'
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject_1,
        claim_predicate=claim_predicate_1,
        claim_object=claim_object_1,
    )
    await add_claim(
        sparql_client=sparql_client,
        claim_prefix=claim_prefix,
        claim_source=claim_source,
        claim_subject=claim_subject_2,
        claim_predicate=claim_predicate_2,
        claim_object=claim_object_2,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject_1,
        claim_predicate=claim_predicate_1,
        claim_object=claim_object_1,
    )
    assert len(claims) == 1
    await remove_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
    )
    claims = await get_claims(
        sparql_client=sparql_client,
        claim_source=claim_source,
        claim_subject=claim_subject_1,
        claim_predicate=claim_predicate_1,
        claim_object=claim_object_1,
    )
    assert len(claims) == 0
