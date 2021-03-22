#Python Script for the PySpark classification model for Steel faults 

# Creating a Spark session 


get_ipython().system('scala -version')


#  we need to check the scala version so that you can include the correct version of the spark-bigquery-connector jar. </p>


from pyspark.sql import SparkSession
spark = SparkSession.builder  .appName('Steel defults classification with PySpark')  .getOrCreate()

spark

#  Enabling Enable repl.eagerEval 
# This will output the results of DataFrames in each step without the new need to show df.show() and also improves the formatting of the output

spark.conf.set("spark.sql.repl.eagerEval.enabled",True)


#  Import Libraries 

from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer


# Data import 


df=spark.read.csv("gs://pyspark-project-bucket/steel_faults.csv", header=True, inferSchema=True)


df.printSchema()


# PySpark dataframe 

df


#  Exploratory Data Analysis 

df.describe()


# Null and missing values in dataframe 

### Get count of null and nan values in pyspark

from pyspark.sql.functions import isnan, when, count, col

df.select([count(when(isnan(c) |col(c).isNull(), c)).alias(c) for c in df.columns]).toPandas().head()


# Target classes 

# Our faults labels are like following ('Pastry', 'Z_Scratch','K_Scatch','Stains','Dirtiness','Bumps','Other_Faults')

faults=df.groupBy("Target").count().show()


labels=['Stains','Z_Scratch','Other_Faults','Bumps','K_Scatch','Dirtiness','Pastry']


df.groupby('Target').count().toPandas().plot(kind='pie', y='count',labels=labels, startangle=90, figsize=(7, 7),legend=False)


# Assembling features 


from pyspark.ml.feature import VectorAssembler

# Pre-process the data
assembler = VectorAssembler(inputCols=['X_Minimum','X_Maximum','Y_Minimum','Y_Maximum','Pixels_Areas','X_Perimeter',
                                  'Y_Perimeter','Sum_of_Luminosity','Minimum_of_Luminosity','Maximum_of_Luminosity',
                                  'Length_of_Conveyer','TypeOfSteel_A300','TypeOfSteel_A400','Steel_Plate_Thickness',
                                  'Edges_Index','Empty_Index','Square_Index','Outside_X_Index','Edges_X_Index',
                                  'Edges_Y_Index','Outside_Global_Index','LogOfAreas','Log_X_Index','Log_Y_Index',
                                  'Orientation_Index','Luminosity_Index','SigmoidOfAreas'], 
                            outputCol="raw_features")
vector_df = assembler.transform(df)


# Scaling features

from pyspark.ml.feature import StandardScaler

# Scale features to have zero mean and unit standard deviation
standarizer = StandardScaler(withMean=True, withStd=True,
                              inputCol='raw_features',
                              outputCol='features')
model = standarizer.fit(vector_df)
vector_df = model.transform(vector_df)


vector_df


# Label encoding of Target class 

from pyspark.ml.feature import StringIndexer

# Convert categorical label to number
indexer = StringIndexer(inputCol="Target", outputCol="label")
indexed = indexer.fit(vector_df).transform(vector_df)


indexed


Indexing = indexed.select("Target","label").distinct()
Indexing


#  Train Test split


# Select features and labels dataset to inject to the model
data = indexed.select(['features', 'label'])

# train test split 
train, test = data.randomSplit([0.7, 0.3])


print(f"Train set length: {train.count()} records")
print(f"Test set length: {test.count()} records")


# Cross validation 

# Cross-validation is a model validation technique for assessing how the results of a statistical analysis will generalize to an independent data set. It is mainly used in settings where the goal is prediction, and one wants to estimate how accurately a predictive model will perform in practice.

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Create an initial RandomForest model.
rf = RandomForestClassifier(labelCol="label", featuresCol="features")

# Evaluate model
rfevaluator = MulticlassClassificationEvaluator(metricName="f1")

# Create ParamGrid for Cross Validation
rfparamGrid = (ParamGridBuilder()
             .addGrid(rf.maxDepth, [2, 5, 10, 20, 30])
             .addGrid(rf.maxBins, [10, 20, 40, 80, 100])
             .addGrid(rf.numTrees, [5, 20, 50, 100, 500])
             .build())

# Create 5-fold CrossValidator
rfcv = CrossValidator(estimator = rf,
                      estimatorParamMaps = rfparamGrid,
                      evaluator = rfevaluator,
                      numFolds = 5)

# Run cross validations.
rfcvModel = rfcv.fit(train)
print(rfcvModel)

# Use test set here so we can measure the accuracy of our model on new data
rfpredictions = rfcvModel.transform(test)


rfpredictions.toPandas().head(10)


# Select example rows to display.
rfpredictions.select("features","prediction", "label").toPandas().head(10)


# Model evaluation 

# F1 score 

# F1 score is usually more useful than accuracy, especially if you have an **uneven class distribution**. Accuracy works best if false positives and false negatives have similar cost. If the cost of false positives and false negatives are very different, it’s better to look at both Precision and Recall.

# cvModel uses the best model found from the Cross Validation
# Evaluate best model
f1= MulticlassClassificationEvaluator(labelCol ='label',predictionCol = "prediction",metricName="f1")
print('f1:', f1.evaluate(rfpredictions))


# Confusion Matrix

import pandas as pd
from pyspark.mllib.evaluation import MulticlassMetrics
predictionAndLabels = rfpredictions.select('label', 'prediction')
metrics = MulticlassMetrics(predictionAndLabels.rdd.map(lambda x: tuple(map(float, x))))

confusion_matrix = metrics.confusionMatrix().toArray()
labels = [int(l) for l in metrics.call('labels')]
confusion_matrix = pd.DataFrame(confusion_matrix , index=labels, columns=labels)


confusion_matrix


# Model metrics by class

# **Precision** is the ratio of correctly predicted positive observations to the total predicted positive observations. (Precision = TP/(TP+FP))
# 
# **Recall (Sensitivity)** is the ratio of correctly predicted positive observations to the all observations in actual class (Recall = TP/(TP+FN))
# 
# **F1 score** is the weighted average of Precision and Recall. Therefore, this score takes both false positives and false negatives into account. (F1 Score = 2*(Recall * Precision) / (Recall + Precision))
# 
# 

# Statistics by class
labels = rfpredictions.rdd.map(lambda lp: lp.label).distinct().collect()
for label in sorted(labels):
    print("Class %s precision = %s" % (label, metrics.precision(label)))
    print("Class %s recall = %s" % (label, metrics.recall(label)))
    print("Class %s F1 Measure = %s" % (label, metrics.fMeasure(label, beta=1.0)))
    print("_____________________________________________________________")


# Random Forset classifier

#Random forst model 
from pyspark.ml.classification import RandomForestClassifier

# Train a RandomForest model.
rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=1000)


model= rf.fit(train)

# Make predictions.
predictions = model.transform(test)



predictions



# Select example rows to display.
predictions.select("prediction", "label", "features").show(5)


from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))

print("Accuracy = %g" % accuracy)

