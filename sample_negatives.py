import os
import sys
dn=sys.argv[1]
import random

qrels_path="/home/huxiaomeng/beir/examples/generation/datasets/{}/gen-5-qrels/train.tsv".format(dn)
skip=True
dataset={}
from tqdm import tqdm
random.seed(13)
# pos passage
with open(qrels_path,'r') as f:
    for item in f:
        if skip:
            skip=False
            continue
        qid,pid,_=item.strip('\n').split('\t')
        if qid in dataset:
            dataset[qid]['pos'].append(pid)
        else:
            dataset[qid]={}
            dataset[qid]['pos']=[]
            dataset[qid]['pos'].append(pid)
# sample negative passage 
# first accumulative it's top100
hits_at_100={}
hits_path="bm25.scores/run.{}.gen-5-queries.trec".format(dn)
with open(hits_path,'r') as f:
    for item in f:
        process=item.strip('\n').split(' ')
        qid,pid=process[0],process[2]
        if qid not in hits_at_100:
            hits_at_100[qid]=[]
        hits_at_100[qid].append(pid)
for qid in tqdm(dataset):
    if qid not in hits_at_100:
        continue
    pid_list=[pid for pid in hits_at_100[qid] if pid not in dataset[qid]['pos']]
    neg_pids=random.sample(pid_list,min(len(pid_list),5))
    dataset[qid]['neg']=neg_pids
# write to tsv files
qrels_path="/home/huxiaomeng/beir/examples/generation/datasets/{}/gen-5-qrels/qrels-irrels.train.tsv".format(dn)
with open(qrels_path,'w') as f:
    for qid in dataset:
        if qid in hits_at_100 and len(dataset[qid]['neg'])>0:
            pos_ids=dataset[qid]['pos']
            neg_ids=dataset[qid]['neg']
            f.write(qid+'\t'+str(pos_ids)+'\t'+str(neg_ids)+'\n')



