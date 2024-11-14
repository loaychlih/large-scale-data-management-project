#!/bin/bash
##create bucket

# Créer le cluster avec changement de workers pour chaque experience par nous
gcloud dataproc clusters create cluster-spark \
    --enable-component-gateway \
    --region europe-west1 \
    --zone europe-west1-c \
    --master-machine-type n1-standard-4 \
    --master-boot-disk-size 500 \
    --single-node \
    --image-version 2.0-debian10 \
    --project project-test-440719

# Soumettre le job PySpark
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster cluster-spark gs://pagerankloay2/pagerankrdd.py -- gs://public_lddm_data/small_page_links.nt 3

## access results
gsutil cat gs://pagerank/pyspark_result_*
gsutil cat gs://pagerank/top_pagerank_*
