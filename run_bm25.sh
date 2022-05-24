dn=$1
python -m pyserini.search.lucene \
  --index indexes/$dn \
  --topics queries/$dn/gen-5-queries.tsv \
  --output bm25.scores/run.$dn.gen-5-queries.txt \
  --bm25