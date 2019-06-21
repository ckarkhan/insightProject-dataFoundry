"""
Code to merge patient data with their ailment data.
"""
"""
author: @CHETANKARKHANIS
"""

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import json

#set sparkConf,sparkContext and sparkSession
def spark_conf():
    conf = SparkConf().setAppName("mergeMetaData").set("spark.executor.memory", "6g")#.setMaster("spark://54.185.228.175:7077")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark


def print_rows(row):
    """ Print rows of datapram as a JSON encoded Python dictionary. """

    data = json.loads(row)
    for key in data:
        print("{key}:{value}".format(key=key, value=data[key]))


def readAndprocess_files(spark):
    """Read in the Data Entry and BBox metadata files from S3 """

    de_file = spark.read.load("s3a://chest-xray-source-images/flat_files/Data_Entry_2017.csv",format="csv",header='True',sep=",")
    bbox_file = spark.read.load("s3a://chest-xray-source-images/flat_files/BBox_List_2017.csv",format="csv",header='True',sep=",")

    df_merged = de_file.join(bbox_file, ["Image Index"], "left_outer")
    df_merged = df_merged.drop(bbox_file["Finding Label"])

    df_merged_json = json.dumps(json.loads(df_merged.toJSON())) 
    print(df_merged_json)

    #df_merged_json.foreach(print_rows)


def main():
    sprk = spark_conf()
    readAndprocess_files(sprk)


main()