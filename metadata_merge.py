"""
Code to merge patient data with their ailment data.
"""

from pyspark.sql import SparkSession

DE_File = "/usr/local/spark/README.md"
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numA = logData.filter(logData.value.contains('a')).count()
numB = logData.filter(logData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i"  % (numA, numB))

spark.stop()
