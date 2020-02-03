import datetime
import time
import delorean as d
from elasticsearch import Elasticsearch

from azure.mgmt.monitor import MonitorManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# import configuration files
import elasticConfig
import clientConfig

#create an ElasticSearch Object
es = Elasticsearch(
	    [ elasticConfig.username + ":" + elasticConfig.password + "@" + elasticConfig.host],
	    scheme="https",
	    request_timeout=30
	)

# initial Loop Timestamp
loopMillis = datetime.datetime.now()


# getMeasurement use the Azure API for consult a measurement of one metric
def getMeasurement(measurement):

    # Create a client
    TENANT_ID = clientConfig.TENANT_ID
    CLIENT = clientConfig.CLIENT
    KEY = clientConfig.KEY

    credentials = ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID
    )

    # Get the ARM id of your resource. You might chose to do a "get"
    # using the according management or to build the URL directly
    # Example for a ARM VM

    subscription_id = clientConfig.subscription_id
    resource_group_name = clientConfig.resource_group_name
    vm_name = clientConfig.vm_name


    resource_id = (
        "subscriptions/{}/"
        "resourceGroups/{}/"
        "providers/Microsoft.Compute/virtualMachines/{}"
    ).format(subscription_id, resource_group_name, vm_name)

    # Create client

    client = MonitorManagementClient(
        credentials,
        subscription_id
    )

    # Get measurement of the last minute for this VM
    today = datetime.datetime.now()
    #.strftime("%Y/%m/%d %H:%M:%S")
    lastminute = today - datetime.timedelta(minutes=1)

    metrics_data = client.metrics.list(
        resource_uri = resource_id,
        timespan="{}/{}".format(lastminute, today),
        interval='PT1M',
        metricnames= measurement,
        aggregation='Total'
    )

    for item in metrics_data.value:
        # azure.mgmt.monitor.models.Metric
        for timeserie in item.timeseries:
            for data in timeserie.data:
                # azure.mgmt.monitor.models.MetricData
                return {
                    "VM": vm_name,
                    "resource_group_name": resource_group_name,
                    "Measurement": measurement,
                    "data": data.total,
                }
# main loop

while True:
    # Time Now
    currentMillis = datetime.datetime.now()
    # Used Delorean to parse timestamp to integer, and subtract to know time elapsed since last loop
    if (d.Delorean(currentMillis, timezone="UTC").epoch * 1000) - (d.Delorean(loopMillis, timezone="UTC").epoch * 1000) >= 60000:

        # Get the timestamp of the new loop
        loopMillis = datetime.datetime.now()

        # Mesuremnts, CPU, Disk Read, Disk Write, Network In, Network Out
        CPU = getMeasurement("Percentage CPU")
        DiskRead = getMeasurement("Disk Read Bytes")
        DiskWrite = getMeasurement("Disk Write Bytes")
        NetworkIn = getMeasurement("Network In Total")
        NetworkOut = getMeasurement("Network Out Total")

        # Build JSon Data to send to ElasticSearch
        data = {
            "@timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "host" :{
                "vm_name" : CPU['VM'],
                "resource_group" : CPU['resource_group_name']
            },
            "measurements": {
                "cpu": (CPU['data'])/100,
                "disk_read": DiskRead['data'],
                "disk_write": DiskWrite['data'],
                "network_in": NetworkIn['data'],
                "network_out": NetworkOut['data'],
            },
            "ecs":{
                "version": 1.4
            }
        }

        # Send data to ElasticSearch
        es.index(index='azure', body=data)

        print (data)
