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

def read_file(spark):
    de_file = spark.read.load("s3a://chest-xray-source-images/flat_files/Data_Entry_2017.csv",format="csv",header='True',sep=",")
    cardio = de_file.filter(de_file.value.contains('Emphysema')).count()

    return cardio
    

def main():
    spark = spark_conf()

    print("Lines with Emphysema: " +  str(read_file(spark)) ) 
    

if __name__ ==  "main":
    main()