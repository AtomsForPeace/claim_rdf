#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: conftest.py

from configparser import ConfigParser
import pytest
from aiosparql.client import SPARQLClient


@pytest.fixture
def config():
    cfg = ConfigParser()
    cfg.read('testing.cfg')
    yield cfg


@pytest.fixture
def sparql_endpoint(config: ConfigParser):
    yield config.get('sparql', 'endpoint')


@pytest.fixture
async def sparql_client(sparql_endpoint: str):
    _sparql_client = SPARQLClient(sparql_endpoint)
    yield _sparql_client
    await _sparql_client.close()


@pytest.fixture
async def truncate_sparql(sparql_client: SPARQLClient):
    await sparql_client.update(
        """
        DELETE
        WHERE {
          ?s ?p ?o
        }
        """
    )
