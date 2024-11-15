import re
import sys
from operator import add
import time
import json
from subprocess import call

from pyspark.sql import SparkSession


# removed typing for compatibility with Spark 3.1.3
# typing ok with spark 3.3.0

def computeContribs(urls, rank) :
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls) :
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[2]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <iterations>", file=sys.stderr)
        sys.exit(-1)

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    statistics_data = {}
    start_program_timestamp = time.time()
    partition = False
    compute_max = True
    gs_bucket = "gs://pagerankloay2"

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    #using default portable hash on key and default number of partitions
    #https://spark.apache.org/docs/latest/api/python/_modules/pyspark/rdd.html#RDD.partitionBy
    if (partition):
        links = links.partitionBy(numPartitions = None)

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        if (partition):
            ranks = ranks.partitionBy(numPartitions = None)

        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: computeContribs(
            url_urls_rank[1][0], url_urls_rank[1][1]  # type: ignore[arg-type]
        ))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    # Collects all URL ranks and dump them to console.
    time_tag = time.strftime("%Y%m%d-%H%M%S")
    ranks.coalesce(1).saveAsTextFile(gs_bucket+"/pyspark_result_"+time_tag) #colaesce needed to have single partition write access
    if (compute_max):
        top_pagerank = ranks.sortBy(lambda x : x[1],False).toDF().limit(10).rdd #top 10 pagerank only
        top_pagerank.coalesce(1).saveAsTextFile(gs_bucket+'/top_pagerank_'+time_tag) #colaesce needed to have single partition write access

    spark.stop()
    finish_program_timestamp = time.time()
    statistics_data['start_program_timestamp'] = start_program_timestamp
    statistics_data['finish_program_timestamp'] = finish_program_timestamp
    statistics_data['total_time_elapsed'] = finish_program_timestamp - start_program_timestamp

    #for (link, rank) in ranks.collect():
    #    print("%s has rank: %s." % (link, rank))

    statistics_filename = 'pyspark_statistics'+time_tag+'.json'
    with open(statistics_filename, 'w+') as outfile:
        outfile.write(json.dumps(statistics_data))

    call(["gsutil" ,"cp",statistics_filename ,gs_bucket])
