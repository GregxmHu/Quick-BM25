from pyserini.search.lucene import LuceneSearcher
import sys
from tqdm import tqdm
import os
dn=sys.argv[1]
searcher = LuceneSearcher('indexes/{}'.format(dn))
topics="queries/{}/gen-5-queries.tsv".format(dn)
output="bm25.scores/run.{}.gen-5-queries.trec".format(dn)
queries=[]
with open(topics,'r') as f:
    for item in f:
        qid,query=item.strip('\n').split('\t')
        queries.append((qid,query))
trec={}
for qpair in tqdm(queries):
    qid,query=qpair[0],qpair[1]
    hits = searcher.search(query,k=100)
    trec[qid]=[]
    for i in range(len(hits)):
        trec[qid].append((i,hits[i].docid,hits[i].score))
with open(output,'w') as f:
    for qid in tqdm(trec):
        for item in trec[qid]:
            f.write(
                qid+' '+'Q0'+' '+item[1]+' '+str(item[0])+' '+str(item[2])+' '+'Anserini'+'\n'
            )
