import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.conf import settings

from secureshare.models import Report

import re

from whoosh.query import Query
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser, OperatorsPlugin
from whoosh.index import open_dir
from whoosh import scoring

def make_search_index():
    schema = Schema(description=TEXT(stored=True), full_description=TEXT(stored=True), report_id=NUMERIC(stored=True, numtype=int))
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    rlist = Report.objects.all()
    for r in rlist:
        writer.add_document(description=r.description, full_description=r.full_description, report_id=r.id)
    writer.commit()

def ranksearch(query):
    # ix = create_in("indexdir", schema)
    ix = open_dir("indexdir")
    writer = ix.writer()
    results = []
    with ix.searcher(weighting=scoring.BM25F(0.75, 1.2)) as s:
        qp = QueryParser("full_description", ix.schema)
        cp = OperatorsPlugin(And="&", Or="\|", AndMaybe="&~", Not=None)
        qp.replace_plugin(cp)

        q = qp.parse(query, normalize=True)

        results = []

        # Make tuple list of (score, report) for AND query
        hits = s.search(q, limit=None, terms=True)
        for inx in range(len(list(hits))):
            report = Report.objects.get(pk=int(hits[inx].fields()['report_id']))
            results.append((hits[inx].score, report))
        
        # Make tuple list of (score, report) for OR query
        qOR = qp.parse(queryOR(query), normalize=True)
        hits2 = s.search(qOR, limit=None, terms=True)
        for inx2 in range(len(list(hits2))):
            report = Report.objects.get(pk=int(hits2[inx2].fields()['report_id']))
            results.append((hits2[inx2].score, report))
        
        # Make tuple list of (score, report) for AndMaybe query
        qAM = qp.parse(queryAndMaybe(query), normalize=True)
        hits3 = s.search(qAM, limit=None, terms=True)
        for inx3 in range(len(list(hits3))):
            report = Report.objects.get(pk=int(hits3[inx3].fields()['report_id']))
            results.append((hits3[inx3].score, report))

            
        # Sort by score across expanded query results: AND, OR, AndMaybe
        sorted_by_score = sorted(results, key=lambda tup: tup[0])
        ranked_results = []
        for i, j in results:
            ranked_results.append(j)

        return ranked_results


    # Next time lol
    # elif function is 'tfidf':
    #     with ix.searcher(weighting=scoring.TF_IDF) as s:
    #         q = QueryParser("full_description", ix.schema).parse(query)
    #         hits = s.search(q, limit=None)
            

def queryOR(query):
    if len(query) < 2:
        return query

    terms = query.split(' ')
    for idx, val in reversed(list(enumerate(terms))):
        if idx == 0:
            break
        terms.insert(idx, ' | ')
    
    query_OR = ""
    for t in terms:
        query_OR += t

    return query_OR

def queryAndMaybe(query):
    if len(query) < 2:
        return query

    terms = query.split(' ')
    for idx, vla in reversed(list(enumerate(terms))):
        if idx == 0:
            break
        terms.insert(idx, ' &~ ')

    query_AndMaybe = ""
    for t in terms:
        query_AndMaybe += t

    return query_AndMaybe


# Remove indexdir from the cmd line if not working and remake
# make_search_index()










