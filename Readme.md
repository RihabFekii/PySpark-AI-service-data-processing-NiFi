# End-to-end AI solution with PySpark & real time data processing with Apache NiFi

This project demostrates in a first phase, how to collect data in real-time via the [NGSI-LD Context Broker](https://fiware-orion.readthedocs.io/en/master/), transform and persist it using [DRACO](https://github.com/ging/fiware-draco) (based on Apache NiFi). In a second phase, it shows how to run Apache Spark and Jupyter Notebooks on a Google Cloud [Dataproc](https://cloud.google.com/dataproc) cluster. 

Further information about [NiFi](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/tree/master/Nifi) and [PySpark](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/tree/master/PySpark) configuration can be found within their respective folders. 

## Agenda 

- [General architecture](#general-architecure)
- [Used technologies](#used-technologies)
- [Setting up the Cloud environment](#setting-up-the-cloud-environment)

## General architecture 

![AI service reference architecture](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/General%20architecture.png)

## Used technologies  

- [NGSI-LD Context Broker](https://github.com/FIWARE/context.Orion-LD): A FIWARE generic enabler to manage context data in real time. It allows you to manage the entire lifecycle of context information including updates, queries, registrations and subscriptions.

- [DRACO](https://github.com/ging/fiware-draco): A FIWARE generic enabler for managing the history of context data. Internally, Draco is based on [Apache NiFi](https://nifi.apache.org/docs.html), NiFi is a dataflow system based on the concepts of flow-based programming. It supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic. It was built to automate the flow of data between systems.

- [Dataproc](https://cloud.google.com/dataproc) : A managed Spark and Hadoop service that lets you take advantage of open source data tools for batch processing, querying, streaming, and machine learning.

- [PySpark](https://spark.apache.org/docs/latest/api/python/): An interface for Apache Spark in Python. It not only allows you to write Spark applications using Python APIs, but also provides the PySpark shell for interactively analyzing your data in a distributed environment. PySpark supports most of Spark’s features such as Spark SQL, DataFrame, Streaming, MLlib (Machine Learning) and Spark Core.

- [Spark MLlib](https://spark.apache.org/docs/latest/ml-guide.html): Built on top of Spark, MLlib is a scalable machine learning library that provides a uniform set of high-level APIs that help users create and tune practical machine learning pipelines.

- [Jupyter Notbeook](https://jupyter.org/): An open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text. Uses include: data cleaning and transformation, numerical simulation, statistical modeling, data visualization, machine learning, and much more.

## Setting up the Cloud environment

As shown in the general architecture above, this project uses Google Cloud Services (GCS). 
The following steps demonstrates how to set up the Cloud environment which is used within this project: 

-   Create a Google cloud project

-   Create a Google Cloud Storage bucket 

-   Create a Dataproc Cluster with Jupyter and Component Gateway

-   Access the JupyterLab web UI on Dataproc

-   Create a Python Notebook for the AI solution based on PySpark

-   Running a Spark job and plotting the results.

### Step 1: Create a Google cloud project

Sign-in to Google Cloud Platform console at
[console.cloud.google.com](http://console.cloud.google.com/) and create a new project:

![](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image10.jpg)

In the Cloud Shell run the following commands to enable the Dataproc service, Compute Engine and Storage APIs:

```shell
 $ gcloud config set project <project_id>
```

Then 

```shell
$ gcloud services enable dataproc.googleapis.com \
  compute.googleapis.com \
  storage-component.googleapis.com
```

#### Step 2 : Create a Google Cloud Storage bucket

Create a Google Cloud Storage bucket in the region closest to your data
and give it a unique name. This will be used for the Dataproc cluster.

To do that we need to follow two steps :

1.  Open the Cloud **Storage** browser in the Google Cloud Console.

![bucket](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image19.png)

2.  Click **Create bucket** to open the bucket creation form.

![bucket form](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image26.png)

#### Step 3 : Create your Dataproc Cluster with Jupyter & Component Gateway

The cluster creation could done through Dataproc service GUI or from the cloud shell. 

In the cloud shell, run this gcloud command to create your cluster with all the necessary components to work with Jupyter on your cluster.

```shell
$ gcloud beta dataproc clusters create ${CLUSTER_NAME} \
 --region=${REGION} \
 --image-version=1.4 \
 --master-machine-type=n1-standard-4 \
 --worker-machine-type=n1-standard-4 \
 --bucket=${BUCKET_NAME} \
 --optional-components=ANACONDA,JUPYTER \
 --enable-component-gateway
 ```

PS:
-   The machine types to use for your Dataproc cluster. You can see a list of available [machine types here](https://cloud.google.com/compute/docs/machine-types).

-   By default, 1 master node and 2 worker nodes are created if you do
not set the flag --num-workers

It should take about 90 seconds to create your cluster and once it is
ready you will be able to access your cluster from the [Dataproc Cloud
console UI](https://console.cloud.google.com/dataproc/clusters).

![cluster](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image11.png)


#### Step 4: Accessing the JupyterLab web interface

Once the cluster is ready you can find the Component Gateway link to the
JupyterLab web interface by going to [Dataproc Clusters - Cloud
console](https://console.cloud.google.com/dataproc/clusters),
clicking on the cluster you created and going to the Web Interfaces tab.

![WebUI](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image30.png)


#### Step 5: Create a Python Notebook for the AI solution based on PySpark

It is recommended to use "Python 3" notebooks because it has access to
all the data science packages installed with Anaconda as well as PySpark
and which also allows you to configure the SparkSession in the notebook
and include other google cloud APIs(e.g [BigQuery Storage
API](https://cloud.google.com/bigquery/docs/reference/storage) or
other APIs)

![python](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image29.png)

Before creating a new jupyter notebook we need to create a folder where
it will be saved in our google cloud storage bucket under GCS(in this example)

![](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Images/image23.png)




More information about the AI solution modeling and the dataset are found under the [PySpark](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/tree/master/PySpark) folder. 






