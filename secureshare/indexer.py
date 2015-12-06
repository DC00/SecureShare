from whoosh.query import Query
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser, OperatorsPlugin
from whoosh.index import open_dir
from whoosh import scoring

import shutil

from secureshare.models import Report

import os

BASE_DIR = os.getcwd()
MEDIA_DIR = "%s/media/" % (BASE_DIR)

def make_search_index():
    # print(os.getcwd())
    shutil.rmtree('indexdir')
    os.makedirs('indexdir')
    schema = Schema(description=TEXT(stored=True), full_description=TEXT(stored=True), file_text=TEXT(stored=True), 
                    reporter=TEXT(stored=True), date=TEXT(stored=True), report_id=NUMERIC(stored=True, numtype=int))

    ix = create_in("indexdir", schema)
    writer = ix.writer()
    rlist = Report.objects.all()
    for r in rlist:
        file_text = u""
        
        if not r.is_private and r.uploaded_files != "":
            file_text = parse_file(r)


        writer.add_document(description=r.description, full_description=r.full_description, file_text=file_text, 
                            reporter=r.reporter_it_belongs_to.user_name, date=unicode(str(r.created_at)[0:10]), report_id=r.id)

        print("Indexing Report: %s   Description: %s" % (r.id, r.description))

    writer.commit()

def parse_file(reporter):
    filename = "%s" % (reporter.uploaded_files)
    path_to_file = "%s%s" % (MEDIA_DIR, filename[2:len(filename)])
    if not os.path.isfile(path_to_file):
        raise Exception, "file " + path_to_file + " not found."
    
    with open(path_to_file, 'r') as f:
        text = f.read()
    f.closed

    return unicode(text, 'utf-8')


if __name__ == "__main__":
    make_search_index()
