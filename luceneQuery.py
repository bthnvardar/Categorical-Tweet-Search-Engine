import sys
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.search.similarities import BM25Similarity

class lucene_query:
    def __init__(self):
        lucene.initVM()
        self.analyzer = StandardAnalyzer()
        self.indexPath = File("index/").toPath()
        self.indexDir = NIOFSDirectory.open(self.indexPath)
        self.reader = DirectoryReader.open(self.indexDir)
        self.searcher = IndexSearcher(self.reader)
        self.searcher.setSimilarity(BM25Similarity())

    def search(self, search_str):
        lucene.getVMEnv().attachCurrentThread() 
        reader = DirectoryReader.openIfChanged(self.reader)
        if reader != None:
            self.reader = reader
            self.searcher = IndexSearcher(self.reader)
            self.searcher.setSimilarity(BM25Similarity())
        query = QueryParser("tweet", self.analyzer).parse(search_str)
        MAX = 5000
        hits = self.searcher.search(query, MAX)
        results = []
        for hit in hits.scoreDocs:
            doc = self.searcher.doc(hit.doc)
            results.append(doc.get("originalTweet"))#.encode("utf-8"))
        return results
