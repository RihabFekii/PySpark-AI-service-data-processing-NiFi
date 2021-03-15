# End-to-end AI Solution With PySpark & Real-time Data Processing With Apache NiFi

This project demostrates in a first phase, how to collect data in real-time via the [Conext Broker](https://fiware-orion.readthedocs.io/en/master/), transform it and persist it using [DRACO](https://github.com/ging/fiware-draco)(based on Apache NiFi). In a second phase, how to run Apache Spark and Jupyter Notebooks on a Google Cloud [Dataproc](https://cloud.google.com/dataproc) cluster. 

## Agenda 

- [General architecture](#general-architecure)
- [Used technologies](#used-technologies)
- [Setting up the Cloud environment]



## General architecure 

![AI service reference architecture](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/General%20architecture.png)

## Used technologies  

- [Conext Broker](https://fiware-orion.readthedocs.io/en/master/): A FIWARE generic enbaler to manage context data in real time. 

- [DRACO](https://github.com/ging/fiware-draco): An easy to use, powerful, and reliable system to process and distribute data. Internally, Draco is based on [Apache NiFi](https://nifi.apache.org/docs.html), NiFi is a dataflow system based on the concepts of flow-based programming. It supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic. It was built to automate the flow of data between systems.

- [Dataproc](https://cloud.google.com/dataproc) : A managed Spark and Hadoop service that lets you take advantage of open source data tools for batch processing, querying, streaming, and machine learning.

- [PySpark](https://spark.apache.org/docs/latest/api/python/): An interface for Apache Spark in Python. It not only allows you to write Spark applications using Python APIs, but also provides the PySpark shell for interactively analyzing your data in a distributed environment. PySpark supports most of Spark’s features such as Spark SQL, DataFrame, Streaming, MLlib (Machine Learning) and Spark Core.

- [Spark MLlib](https://spark.apache.org/docs/latest/ml-guide.html): Built on top of Spark, MLlib is a scalable machine learning library that provides a uniform set of high-level APIs that help users create and tune practical machine learning pipelines.

- [Jupyter Notbeook](https://jupyter.org/): An open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text. Uses include: data cleaning and transformation, numerical simulation, statistical modeling, data visualization, machine learning, and much more.

## Setting up the Cloud environment

As shown in the general architecture above, we are using Google Cloud Services (GCS). 
The following steps demonstasrte how to set up the Cloud environemnt which is used within this project: 

-   Create a Google cloud project

-   Create a Google Cloud Storage bucket 

-   Create a Dataproc Cluster with Jupyter and Component Gateway

-   Access the JupyterLab web UI on Dataproc

-   Create a Python Notebook for the AI solution based on PySpark

-   Running a Spark job and plotting the results.

### Create a Google cloud project

Sign-in to Google Cloud Platform console at
[console.cloud.google.com](http://console.cloud.google.com/) and create a new project:

![](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image10.jpg)

In the Cloud Shell run the following commands to enable the Dataproc service, Compute Engine and Storage APIs:

```shell
 gcloud config set project <project_id>
```

Then 

```shell
gcloud services enable dataproc.googleapis.com \
  compute.googleapis.com \
  storage-component.googleapis.com
```








