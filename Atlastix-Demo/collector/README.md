## Dependencies

This directory contains:

* Python code
* Elastic configuration example file
* Azure client configuration example file

## Python Dependencies

Dependency | installation with pip | Use reason
--- | --- | ---
delorean | `pip install Delorean` | Convert timestamp to milliseconds since epoch
ElasticSearch | `pip install elasticsearch` | Send the data to ElasticSearch cloud
azure.mgmt.monitor | `pip install azure-mgmt-monitor` | Communication to Azure API

## Python configuration

#### ElasticSearch configuration

Create a file called `elasticConfig.py` copy the ElasticSearch Config Template, now replace the username variable whit user asigned to the python client to send data to elastic, make the same whit the password of that user. Now copy the host of your Elastic Search instance, not include the protocol and remember include the port.

#### Azure client configuration

Create a file called `clientConfig.py` copy the Client Config Template, now replace the TENANT_ID, CLIENT, KEY variables whit your auth keys of Azure API. Now replace the subscription_id, resource_group_name, vm_name variables whit the names of the VMs that you want to monitoring

## Running the script
after setting up and install all the dependencies, open the terminal go to the project folder and run `python Atlastix-Demo.py`

## About the script

* The first part in the script import all the dependencies and configurations line (1 - 11)
* Create a Elastic Search Object whit the configuratiosn gived in `elasticConfig.py` line (14 - 18)
```python
es = Elasticsearch(...)
```
* set loopMillis with the current time to have the elapsed time in the main loop
```python
loopMillis = datetime.datetime.now()
```
* Create a function that make a query to de Azure API of one metric, this function receive a parameter that is a String with the type of metric, and return a directory which contains VM name, resource group name, metric and the data of the measurement the types of the metrics that this functions can to give are:

 * Percentage CPU: id=Percentage CPU, unit=Percent
 * Network In Billable (Deprecated): id=Network In, unit=Bytes
 * Network Out Billable (Deprecated): id=Network Out, unit=Bytes
 * Disk Read Bytes: id=Disk Read Bytes, unit=Bytes
 * Disk Write Bytes: id=Disk Write Bytes, unit=Bytes
 * Disk Read Operations/Sec: id=Disk Read Operations/Sec, unit=CountPerSecond
 * Disk Write Operations/Sec: id=Disk Write Operations/Sec, unit=CountPerSecond
 * CPU Credits Remaining: id=CPU Credits Remaining, unit=Count
 * CPU Credits Consumed: id=CPU Credits Consumed, unit=Count
 * Data Disk Read Bytes/Sec (Deprecated): id=Per Disk Read Bytes/sec, unit=CountPerSecond
 * Data Disk Write Bytes/Sec (Deprecated): id=Per Disk Write Bytes/sec, unit=CountPerSecond
 * Data Disk Read Operations/Sec (Deprecated): id=Per Disk Read Operations/Sec, unit=CountPerSecond
 * Data Disk Write Operations/Sec (Deprecated): id=Per Disk Write Operations/Sec, unit=CountPerSecond
 * Data Disk QD (Deprecated): id=Per Disk QD, unit=Count
 * OS Disk Read Bytes/Sec (Deprecated): id=OS Per Disk Read Bytes/sec, unit=CountPerSecond
 * OS Disk Write Bytes/Sec (Deprecated): id=OS Per Disk Write Bytes/sec, unit=CountPerSecond
 * OS Disk Read Operations/Sec (Deprecated): id=OS Per Disk Read Operations/Sec, unit=CountPerSecond
 * OS Disk Write Operations/Sec (Deprecated): id=OS Per Disk Write Operations/Sec, unit=CountPerSecond
 * OS Disk QD (Deprecated): id=OS Per Disk QD, unit=Count
 * Data Disk Read Bytes/Sec (Preview): id=Data Disk Read Bytes/sec, unit=CountPerSecond
 * Data Disk Write Bytes/Sec (Preview): id=Data Disk Write Bytes/sec, unit=CountPerSecond
 * Data Disk Read Operations/Sec (Preview): id=Data Disk Read Operations/Sec, unit=CountPerSecond
 * Data Disk Write Operations/Sec (Preview): id=Data Disk Write Operations/Sec, unit=CountPerSecond
 * Data Disk Queue Depth (Preview): id=Data Disk Queue Depth, unit=Count
 * OS Disk Read Bytes/Sec (Preview): id=OS Disk Read Bytes/sec, unit=CountPerSecond
 * OS Disk Write Bytes/Sec (Preview): id=OS Disk Write Bytes/sec, unit=CountPerSecond
 * OS Disk Read Operations/Sec (Preview): id=OS Disk Read Operations/Sec, unit=CountPerSecond
 * OS Disk Write Operations/Sec (Preview): id=OS Disk Write Operations/Sec, unit=CountPerSecond
 * OS Disk Queue Depth (Preview): id=OS Disk Queue Depth, unit=Count
 * Inbound Flows: id=Inbound Flows, unit=Count
 * Outbound Flows: id=Outbound Flows, unit=Count
 * Inbound Flows Maximum Creation Rate: id=Inbound Flows Maximum Creation Rate, unit=CountPerSecond
 * Outbound Flows Maximum Creation Rate: id=Outbound Flows Maximum Creation Rate, unit=CountPerSecond
 * Premium Data Disk Cache Read Hit (Preview): id=Premium Data Disk Cache Read Hit, unit=Percent
 * Premium Data Disk Cache Read Miss (Preview): id=Premium Data Disk Cache Read Miss, unit=Percent
 * Premium OS Disk Cache Read Hit (Preview): id=Premium OS Disk Cache Read Hit, unit=Percent
 * Premium OS Disk Cache Read Miss (Preview): id=Premium OS Disk Cache Read Miss, unit=Percent
 * Network In Total: id=Network In Total, unit=Bytes
 * Network Out Total: id=Network Out Total, unit=Bytes
 ```python
    def getMeasurement(measurement):
      ...
      return {...}
 ```
* The main loop is responsible for taking the measurement of time so that every minute the last minute data is sent to elasticsearch. To create the data to send call the function getMeasurement () with the parameters `Percentage CPU`, `Disk Read Bytes`, `Disk Write Bytes`, `Network In Total` and `Network Out Total`
```python
   while True:
     ...
     es.index(index='azure', body=data)
```
