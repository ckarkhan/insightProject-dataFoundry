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


def sparkConf():
    """Setting up some initial configs."""
    conf = SparkConf().setAppName("mergeMetaData").set("spark.executor.memory", "6g")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark


def readAndProcessFiles(spark):
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


    """ Writing to Elasticsearch Index
    df_augmented_metadata = df_augmented_metadata.write.format('org.elasticsearch.spark.sql') \
        .option('es.nodes', '10.0.0.13').option('es.port', '9200') \
        .option('es.mapping.id', 'Image Index') \
        .option('es.resource', '%s/%s' % ('xray_chest_2', 'staff_notes')).save()"""

    return df_augmented_metadata

def writeES(df):
    """ Writing to Elasticsearch Index"""
    df_final_metadata = df.write.format('org.elasticsearch.spark.sql') \
        .option('es.nodes', '10.0.0.13').option('es.port', '9200') \
        .option('es.mapping.id', 'Image Index') \
        .option('es.resource', '%s/%s' % ('xray_chest_3', 'staff_notes')).save()

def main():
    sprk = sparkConf()
    df_aug = readAndProcessFiles(sprk)
    writeES(df_aug)


main()