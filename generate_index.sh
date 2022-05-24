dataset=$1
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input inputs/$dataset/ \
  --index indexes/$dataset/ \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw