#!/bin/bash
##create bucket


gcloud dataproc clusters create cluster-spark \
    --enable-component-gateway \
    --region europe-west1 \
    --zone europe-west1-c \
    --master-machine-type n1-standard-4 \
    --master-boot-disk-size 500 \
    --single-node \
    --image-version 2.0-debian10 \
    --project project-test-440719



## create the cluster 2 workers
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project master-2-large-scale-data
## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster cluster-spark gs://pagerankloay2/pagerankrdd.py -- gs://public_lddm_data/small_page_links.nt 3

## access results
gsutil cat gs://pagerank/pyspark_result_*
gsutil cat gs://pagerank/top_pagerank_*