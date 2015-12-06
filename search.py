import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.conf import settings

from whoosh.query import Query
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser, OperatorsPlugin, GtLtPlugin
from whoosh.index import open_dir
from whoosh import scoring


from secureshare.models import Report

from indexer import *


def ranked_search(query):
    # ix = create_in("indexdir", schema)
    ix = open_dir("indexdir")
    writer = ix.writer()
    with ix.searcher(weighting=scoring.BM25F(0.75, 1.2)) as searcher:
        # qp = QueryParser("full_description", schema)
        qp = MultifieldParser(["description", "full_description", "file_text", "reporter", "date"], ix.schema)
        cp = OperatorsPlugin(And="&", Or="\|", AndMaybe="&~", Not=None)
        qp.replace_plugin(cp)

        qAND = qp.parse(query, normalize=True)
        qOR = qp.parse(queryOR(query), normalize=True)
        qAM = qp.parse(queryAndMaybe(query), normalize=True)
        
        # results are Result objects which have lists of hits
        qAND_docs = searcher.search(qAND, limit=None, terms=True)
        qOR_docs = searcher.search(qOR, limit=None, terms=True)
        qAM_docs = searcher.search(qAM, limit=None, terms=True)

        qAND_docs.fragmenter.maxchars = 160
        qOR_docs.fragmenter.maxchars = 160
        qAM_docs.fragmenter.maxchars = 160

        # Shortening the surrounding chars of text. Default was 20. Now tweet size
        qAND_docs.fragmenter.surround = 20
        qOR_docs.fragmenter.surround = 20
        qAM_docs.fragmenter.surround = 20


        # Used for highlighting matched terms
        # Scoring will still be reflected in order.
        # Sending only OR docs will just simplify display
        hits = get_stats(qOR_docs)

        results = []

        for i in range(len(list(qAND_docs))):
            report_id = Report.objects.get(pk=int(qOR_docs[i].fields()['report_id']))
            results.append((report_id, qOR_docs[i].score))
            

        for j in range(len(list(qOR_docs))):
            report_id = Report.objects.get(pk=int(qOR_docs[j].fields()['report_id']))
            results.append((report_id, qOR_docs[j].score))

        for k in range(len(list(qAM_docs))):
            report_id = Report.objects.get(pk=int(qAM_docs[k].fields()['report_id']))
            results.append((report_id, qAM_docs[k].score))


        results = removeDuplicates(results)

        
        results_and_info = { 'results' : results,
                              'hits' : hits,
                        }


        # for numid, fields in hits.items():
        #     print(numid)
        #     for field, field_value in fields.items():
        #         print(field)
        #         if field == 'full_description':
        #             for term in field_value:
        #                 print(term)
        #             print('\n')
        #         elif field == 'description':
        #             for term2 in field_value:
        #                 print(term2)
        #             print('\n')
        #         elif field == 'file_text':
        #             print(field_value)
        #             print('\n')
        #         elif field == 'date':
        #             print(field_value)
        #             print('\n')
        #         elif field == 'reporter':
        #             print(field_value)
        #             print('\n')

        
        for r, s in results:
            for numid, fields in hits.items():
                if r.id == numid:
                    print(numid)
                    for field, field_value in fields.items():
                        print(field)          



        
        return results_and_info
        


def get_stats(or_docs):
    # report_id : stats
    hits = {}
    matched_terms = []
    for a, b in or_docs.matched_terms():
        matched_terms.append(b)

    for h in or_docs:
        r_id = h.fields()['report_id']
        hits[r_id] = {}
        hits[r_id]['description'] = set()
        hits[r_id]['full_description'] = set()
        hits[r_id]['file_text'] = ""
        hits[r_id]['reporter'] = set()
        hits[r_id]['date'] = set()


        for term in matched_terms:
            if term.lower() in h.highlights('description', top=5).lower():
                hits[r_id]['description'].add(term)

            if term.lower() in h.highlights('full_description', top=5).lower():
                hits[r_id]['full_description'].add(term)

            # if term.lower() in h.highlights('file_text', top=5).lower():
                # hits[r_id]['file_text'].add(term)
            

            if term.lower() in h.highlights('reporter', top=5).lower():
                hits[r_id]['reporter'].add(term)

            if term.lower() in h.highlights('date', top=5).lower():
                hits[r_id]['date'].add(term)

        hits[r_id]['file_text'] += h.highlights('file_text', top=5)

    return hits



def removeDuplicates(results):
    results = sorted(results,key=lambda x: x[0].id, reverse=True)
    for i in reversed(range(len(results))):
        if results[i][0] == results[i-1][0] and i != 0:
            results.pop(i)

    results = sorted(results,key=lambda x: x[1], reverse=True)
    return results


# Query Expansion. Generate OR and AndMaybe queries
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
make_search_index()
ranked_search('normandy ethiopia holocaust derek report')
