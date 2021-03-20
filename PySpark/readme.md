# PySpark AI service for steel faults classification 

The [notebook](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/PySpark/PySpark_Steel_faults_Classification.ipynb) covers the Exploratory Data Analysis (EDA) and the modeling steps using PySpark, the Machine Learning library of Apache Spark.  


## About the Dataset

### Context
This [dataset](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/tree/master/PySpark/dataset) comes from research by [Semeion](http://www.semeion.it/wordpress/en/), Research Center of Sciences of Communication. The original aim of the research was to correctly classify the type of surface defects in stainless steel plates, with six types of possible defects (plus "other"). The Input vector was made up of 27 indicators that approximately describe the geometric shape of the defect and its outline.

### Content
There are 34 fields. The first 27 fields describe some kind of steel plate faults seen in images. Unfortunately, there is no other information to describe these columns.

- X_Minimum
- X_Maximum
- Y_Minimum
- Y_Maximum
- Pixels_Areas
- X_Perimeter
- Y_Perimeter
- SumofLuminosity
- MinimumofLuminosity
- MaximumofLuminosity
- LengthofConveyer
- TypeOfSteel_A300
- TypeOfSteel_A400
- SteelPlateThickness
- Edges_Index
- Empty_Index
- Square_Index
- OutsideXIndex
- EdgesXIndex
- EdgesYIndex
- OutsideGlobalIndex
- LogOfAreas
- LogXIndex
- LogYIndex
- Orientation_Index
- Luminosity_Index
- SigmoidOfAreas

The last column represents the target classes of the different steel faults: 

- Pastry
- Z_Scratch
- K_Scatch
- Stains
- Dirtiness
- Bumps
- Other_Faults



 