import re
import sys
import time
import json
from subprocess import call
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, lit, sum as sql_sum

def parse_neighbors(urls):
    """Parses a urls pair string into URLs pair."""
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
    gs_bucket = "gs://pagerankloay2"

    # Initialize the Spark session
    spark = SparkSession.builder.appName("DataFramePageRank").getOrCreate()

    # Load input file into DataFrame
    lines_df = spark.read.text(sys.argv[1])
    links_df = lines_df.rdd.map(lambda r: parse_neighbors(r[0])).toDF(["url", "neighbor"]).distinct()

    # Group by URL and collect neighbors into a list
    links_df = links_df.groupBy("url").agg(collect_list("neighbor").alias("neighbors"))

    # Initialize ranks
    ranks_df = links_df.select("url").distinct().withColumn("rank", lit(1.0))

    # Run PageRank iterations
    for iteration in range(int(sys.argv[2])):
        # Calculate contributions of each URL to its neighbors
        contribs_df = links_df.join(ranks_df, "url").withColumn(
            "contrib", col("rank") / size("neighbors")
        ).select(explode("neighbors").alias("neighbor"), "contrib")

        # Sum contributions by neighbor and update ranks
        ranks_df = contribs_df.groupBy("neighbor").agg(sql_sum("contrib").alias("sum_contrib"))
        ranks_df = ranks_df.withColumn("rank", col("sum_contrib") * 0.85 + 0.15).select("neighbor", "rank")
        ranks_df = ranks_df.withColumnRenamed("neighbor", "url")

    # Save ranks result to Google Cloud Storage
    time_tag = time.strftime("%Y%m%d-%H%M%S")
    ranks_df.coalesce(1).write.csv(gs_bucket + "/pyspark_result_" + time_tag, header=True)

    # Optionally, save the top 10 PageRank results
    top_pagerank_df = ranks_df.orderBy(col("rank").desc()).limit(10)
    top_pagerank_df.coalesce(1).write.csv(gs_bucket + '/top_pagerank_' + time_tag, header=True)

    # Save statistics to a JSON file and upload to Google Cloud Storage
    finish_program_timestamp = time.time()
    statistics_data['start_program_timestamp'] = start_program_timestamp
    statistics_data['finish_program_timestamp'] = finish_program_timestamp
    statistics_data['total_time_elapsed'] = finish_program_timestamp - start_program_timestamp

    statistics_filename = 'pyspark_statistics' + time_tag + '.json'
    with open(statistics_filename, 'w+') as outfile:
        json.dump(statistics_data, outfile)

    call(["gsutil", "cp", statistics_filename, gs_bucket])

    spark.stop()
