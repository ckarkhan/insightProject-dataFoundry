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

    """ Adding  columns to dataframe for adding notes from doctors and clinicians. """
    df_augmented_metadata = df_merged.withColumn("Clinician_Notes", lit('')) \
        .withColumn("Clinician_Date", lit('')) \
        .withColumn("Doctor_Review", lit('')) \
        .withColumn("Doctor_Review_Date", lit(''))

    df_augmented_metadata.show(5)

    """ Writing to Elasticsearch Index"""
    df_augmented_metadata = df_augmented_metadata.write.format('org.elasticsearch.spark.sql') \
        .option('es.nodes', '54.218.4.105').option('es.port', '9200') \
        .option('es.resource', '%s/%s' % ('xray_chest', 'staff_notes')).save()


    print("ES Index created.")

    #df_merged_json = df_merged.toJSON()

    """ for i in df_merged_json.collect():
        print(i) """

    # return df_merged_json



def main():
    sprk = spark_conf()
    readAndprocess_files(sprk)




main()