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

#set sparkConf,sparkContext and sparkSession
def spark_conf():
    conf = SparkConf().setAppName("mergeMetaData").set("spark.executor.memory", "6g")#.setMaster("spark://54.185.228.175:7077")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark


def readAndprocess_files(spark):
    """Read in the Data Entry and BBox metadata files from S3 """

    de_file = spark.read.load("s3a://chest-xray-source-images/flat_files/Data_Entry_2017.csv")
    bbox_file = spark.read.load("s3a://chest-xray-source-images/flat_files/BBox_List_2017.csv")

    print(de_file.columns)
    print(bbox_file.columns)


def main():
    sprk = spark_conf()
    readAndprocess_files(sprk)


main()