import sys
import lucene
from nltk.corpus import wordnet

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

    def search(self, search_str, search_choice):
        lucene.getVMEnv().attachCurrentThread() 
        reader = DirectoryReader.openIfChanged(self.reader)
        if reader != None:
            self.reader = reader
            self.searcher = IndexSearcher(self.reader)
            self.searcher.setSimilarity(BM25Similarity())

        if len(search_str.split(" ")) == 1:
            syn = []
            for synset in wordnet.synsets(search_str):
                for lemma in synset.lemmas():
                    syn.append(lemma.name())   
            syn = set(syn)
            if len(syn) > 1:
                search_str = ""
                for index,item in enumerate(syn):
                    search_str = search_str + item.replace("_", " ")
                    if index < (len(syn) - 1):
                        search_str = search_str + " OR "
        

        query = QueryParser("tweet", self.analyzer).parse(search_str)
        MAX = 1500
        hits = self.searcher.search(query, MAX)
        results = []
        ids = []
        date = []
        for hit in hits.scoreDocs:
            doc = self.searcher.doc(hit.doc)
            if search_choice < 5 and int(doc.get("tweetCategory")) == search_choice:
                results.append(doc.get("originalTweet"))
                ids.append(doc.get("username"))
                date.append(doc.get("date"))
            elif search_choice == 5:
                results.append(doc.get("originalTweet"))
                ids.append(doc.get("username"))
                date.append(doc.get("date"))
        return results, ids, date
