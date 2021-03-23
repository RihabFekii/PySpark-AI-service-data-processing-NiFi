# Data transformation and persistence with Apache NiFi 

This part of the project demostrates how to transform data in NGSI-LD fomat to CSV and save the collected CSV dataset in Google cloud storage (GCS) service. 

This dataset will be in further steps used to train a machine learning model based on PySpark. 

## Agenda
- [About Apache NiFi](#about-nifi)
- [General architecture](#general-architecure)
- [NiFi flow](#nifi-flow)
- [Detailed NiFi flow description](#detailed-nifi-flow-description)
- [Further information](further-information)

## About Apache NiFi

Apache NiFi is being used by many companies and organizations to power their data distribution needs. One of NiFi's strengths is that the framework is data agnostic. It doesn't care what type of data you are processing. There are processors for handling JSON, XML, CSV, Avro, images and video, and several other formats. There are also several general-purpose processors, such as RouteText and CompressContent. Data can be hundreds of bytes or many gigabytes. This makes NiFi a powerful tool for pulling data from external sources; routing, transforming, and aggregating it; and finally delivering it to its final destinations.

## General architecture 

![Nifi architecture](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/NiFi_architecture.png)

PS: In this example the following [data model of Weather
Observed] was used (https://github.com/FIWARE/data-models/blob/master/specs/Weather/WeatherObserved/example-normalized-ld.jsonld)
in NGSI-LD format to perform the transformation with Apache NiFi.


## NiFi flow

![flow](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image13.png)

Overview about the steps and the function of each processor:

-   **ListenHTTP**: configured as source for receiving notifications from Orion Context Broker

-   **GetFile**: Reads data in JSON-LD format

-   **JoltTransformJSON**: Transforms nested JSON to a simple attribute value JSON file which will be used to form the csv file

-   **ConvertRecord**: Converts each JSON file to a CSV file

-   **MergeContent**: Merges the resulting CSV files to form a generic CSV
(PS: The min number of entries can be set to perform the merge processor. Also a max number of flow files can be set)

-   **PutGCSObject**: Saves the resulting CSV in Google Cloud Storage bucket


## Detailed NiFi flow description


### GetFile processor  


![getfile](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image3.png)

### ListenHTTP

The Listen HTTP processor starts an HTTP Server and listens on a given base path to transform incoming requests into FlowFiles. The default URI of the Service will be http://{hostname}:{port}/v2/notify. Only HEAD and POST requests are supported. GET, PUT, and DELETE will result in an error and the HTTP response status code 405. We use this NiFi native processor for receiving the HTTP notifications coming from NGSI-LD Context Broker.

![getfile](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image15.png)


### JoltTransformJSON processor


`JoltTransformJSON` applies a list of Jolt specifications to the flowfile JSON payload.

A new JSON FlowFile is created with transformed content.

The NiFi JoltTransform uses the powerful Jolt language to parse JSON.
Combined with the NiFi Schema Registry, this gives NiFi the ability to
traverse, recurse, transform, and modify nearly any data format that can
be described in AVRO or, using JSON as an intermediary step.

A Jolt Specification is a JSON structure that contains two main
elements:

-  **operation** (string): shift, sort, cardinality, modify-default-beta, modify-overwrite-beta, modify-define-beta, or
remove

-  **spec** (JSON): A set of key/value pairs of the form {"input-side search": "output-side transformation"}.

In this project the Shift operation was used to transform the nested JSON-LD
in the way which gives a simple key value JSON file to be converted to
CSV in a later step.

-  **Shift** ebales reading values or portions of the input JSON tree and
adding them to specified locations in the output.

The following is the configuration of the `JoltTransformJSON` processor:

![jolt](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image5.png)

### Convert Record processor: 

After Connecting to the source processor which generates the JSON files
to ConvertRecord.

The following steps are:

-   Configure ConvertRecord and set `Record Reader` to use `JsonTreeReader` controller service and `Record Writer` to use `CSVRecordSetWriter` controller service

-   Configure both the controller services and set `Schema Registry` property to use `AvroSchemaRegistry`

![convert_record](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image2.png)

**JsonTreeReader**

The `JsonTreeReader` Controller Service reads a JSON Object and creates a Record object for the entire JSON Object tree. The Controller Service must be configured with a Schema that describes the structure of the JSON data. If any field exists in the JSON that is not in the schema, that field will be skipped. If the schema contains a field for which no JSON field exists, a null value will be used in the Record (or the default value defined in the schema, if applicable).

![JsonReader](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image4.png)

**AvroSchemaRegistry**

Provides a service for registering and accessing schemas. You can register a schema as a dynamic property where 'name' represents the schema name and 'value' represents the textual representation of the actual schema following the syntax and semantics of Avro's Schema format.

To create the Avro Schema from the data model and verify that it is
correct, check the following [Avro Schema From JSON Generator](https://toolslick.com/generation/metadata/avro-schema-from-json)

Follow the following steps to configure this processor:

-   Configure AvroSchemaRegistry. Go to the `Properties` tab and click the + button which lets you add a dynamic property.

-   Give some property name (ex: `weather`) and for the value, give the Avro schema expected for your JSON input.

![Avro](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image10.png)


Configure both `JsonTreeReader` and `CsvRecordSetWriter` and set the
`Schema Name` property to the name provided above, in this case,
`weather`.

**CsvRecordSetWriter**

The `CsvRecordSetWriter` Controller Service writes the contents of a RecordSet (ouptput of `JsonTreeReader`) as CSV data. The first line written will be the column names (unless the 'Include Header Line' property is false). All subsequent lines will be the values corresponding to the record fields.

![CSV_writer](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image6.png)

### MergeContent 

The reason to use the `MergeContent` processor is to merge the incoming flow files in CSV format into one CSV.

![Merge](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image8.png)

Define a header to the resulting CSV file and reconfigure the
**ConvertRecord** processor and in the controller service of
**CscRecordSetWriter** set the property **Include Header Line** to False

![processor](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image7.png)


### PutGCSObject

`PutGCSObject` enables putting flow files to a Google Cloud Bucket.

The following configuration of the processor have to be set

![PutGCS](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image9.png)



There is a controller service associated with this processor which is
[GCPCredentialsControllerService](https://nifi.apache.org/docs/nifi-docs/components/nifi-docs/components/org.apache.nifi/nifi-gcp-nar/1.9.0/org.apache.nifi.processors.gcp.credentials.service.GCPCredentialsControllerService/index.html)

Basically to enable storing the resulting flowFiles in Google cloud
storage bucket these are the steps to be done:

First open:
[https://console.cloud.google.com/](https://console.cloud.google.com/)
and select the project that you want to work with.

Supposing that a bucket associated with this project is created the
following steps are needed to get the credentials in JSON format to get
access to the storage service from Nifi.

**1/** Go to **IAM & Admin** service

As an example here my project name is "FIWARE on K8S"

![IAM](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image11.png)


**2/** Click on the entry **Service Accounts** on the left side bar and
then **create a service Account**

You get a form in which you only need to provide a service account name

![Credentials](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image12.png)


Copy the **Service account email** it is needed in the coming steps

Example: myservice@projectID.iam.gserviceaccount.com

**3/** Go to the **Storage** service and select the bucket then on
**Permissions**.


![permission](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image1.png)

You need to add a new permission then click on the ADD button and you get the following form

**4/** Select the Role **Storge Legacy Bucket Owner** which enables you to
read and write in the bucket.

Then Download the JSON key which you will need to provide in the NiFi
processor GCPCredentialsControllerService under the property **Service Account JSON**

![GCS](https://github.com/RihabFekii/PySpark-AI-service_Data-processing-NiFi/blob/master/Nifi/Images/image14.png)


The previous processors can be reused and the output processor(e.g `PutGCSObject`) can be changed with other processors to put object to AWS or to save the output dataset lacally etc,..

## Further information

The follwing is the list of the Apache NiFi processors and controller services used within this project: 

- [GetFile](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.5.0/org.apache.nifi.processors.standard.GetFile/index.html)
- [ListenHTTP](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.6.0/org.apache.nifi.processors.standard.ListenHTTP/)
- [JoltTransformJSON](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.5.0/org.apache.nifi.processors.standard.JoltTransformJSON/)
- [ConvertRecord](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.5.0/org.apache.nifi.processors.standard.ConvertRecord/index.html)
- [MergeContent](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.6.0/org.apache.nifi.processors.standard.MergeContent/index.html)
- [PutGCSObject](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-gcp-nar/1.10.0/org.apache.nifi.processors.gcp.storage.PutGCSObject/index.html)


The follwing is the list of the Apache NiFi processors and controller services used within this project: 

- [AvroSchemaRegistry](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-registry-nar/1.12.1/org.apache.nifi.schemaregistry.services.AvroSchemaRegistry/index.html)
- [JsonTreeReader](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-record-serialization-services-nar/1.5.0/org.apache.nifi.json.JsonTreeReader/index.html)
- [CsvRecordSetWriter](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-record-serialization-services-nar/1.5.0/org.apache.nifi.csv.CSVRecordSetWriter/index.html)
- [GCPCredentialsControllerService](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-gcp-nar/1.5.0/org.apache.nifi.processors.gcp.credentials.service.GCPCredentialsControllerService/)

The following testing tool was used to create the Avro schema for the data model in JSON format:
- [Avro Schema From JSON Generator](https://toolslick.com/generation/metadata/avro-schema-from-json)

The following testing tool was used to create the Jolt transfomation: 
- [Jolt Transform Demo](https://jolt-demo.appspot.com/#inception)

All Jolt transformation operations are covered in this [article](https://community.cloudera.com/t5/Community-Articles/Jolt-quick-reference-for-Nifi-Jolt-Processors/ta-p/244350) 




