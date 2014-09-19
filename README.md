Open311 on Fi-Ware
==================

This repository contains prototype software used to display Open311 data on a map.
It consists of three [Wirecloud](http://conwet.fi.upm.es/wirecloud/) widgets,
an Open311-to-NGSI-converter tool and a simple CORS-enabled Proxy.

The project is created for [Forum Virium Helsinki](http://forumvirium.fi/), and its main objective is
to demonstrate facilities of [Fi-Ware](http://www.fi-ware.org/) platform for this kind of use cases.
It is __not production quality__. It contains __a known security hole__. It is for prototyping purposes only and works as a basis for future projects.


Requirements
------------

The widgets run in [Fi-Ware Mashup Lab](https://mashup.lab.fi-ware.org/) environment. The widgets use
[Orion Context Broker](http://catalogue.fi-ware.org/enablers/publishsubscribe-context-broker-orion-context-broker) or some other
NGSI10-compatible data store as their data source. The server side software requires Python and Node.js, their respective package
management tools and other tools easily available on most operating systems.

Installation
------------

### The widgets
1. Create widget distribution packages:
    ` ./mkwgt.sh `
2. Upload the created widgets to your Mashup Lab workspace. Consult Wirecloud documentation on how to do this.
3. Configure wiring between the widgets. The sole Open311Map output should be wired to both Open311Image and Open311Info.
4. Configure Data source URLs. The URLs are currently hardcoded in Open311Map/js/main.js

### open3112ngsi
1. Copy open3112ngsi to a publicly accessible server.
2. `cd open3112ngsi; virtualenv .; source bin/activate; pip install docopt lxml requests==1.1.0 three;`
3. Configure Data source URLs. They are currently hardcoded in Open311Client.py and NGSIClient.py.
4. Command that imports all data from a open311 server to your NGSI server is `python open3112ngsi.py all`. You must arrange
   that to run nigtly throught cron or something similar.


### CORS-enabled proxy
Because of problems with Wirecloud proxy in Mashup Lab configuration, an ad hoc proxy server is provided to handle connections
to Orion Context Broker and external Service Object API, if available.
The provided proxy server fully exposes NGSI10 API to outside world.
__THIS IS NOT SECURE!__ This is not meant to be used in a production environment.
To use the software in a production environment, the problems with Mashup Lab environment must be solved instead.

1. Copy corsproxy directory to a publicly accessible server.
2. `cd corsproxy; npm install; ./runproxy.sh`

License
-------

Software in this repository are licensed under [the MIT license](LICENSE.md)

Contact
-------

Forum Virium Helsinki
[http://www.forumvirium.fi/](http://www.forumvirium.fi/)
