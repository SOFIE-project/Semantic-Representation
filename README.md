# SOFIE Semantic Representation component

**Table of contents:**

- [Description](#description)
  - [Architecture Overview](#architecture-overview)
  - [Relation with SOFIE](#relation-with-sofie)
  - [Key Technologies](#key-technologies)

- [Usage](#usage)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Execution](#execution)

- [Testing](#testing)
  - [Running the tests](#running-the-tests)
  - [Evaluating the results](#evaluating-the-results)

- [Integration](#integration)
- [Deployment](#deployment)
- [Open and Known Issues](#known-and-open-issues)
- [Contact Info](#contact-info)

## Description

The SOFIE Semantic Representation component is a validator for the data coming from the IoT devices to the SOFIE enabled platform. 
The validator checks if the data are conform to the schema, if they are not the component informs the IoT platform with a message explaining the error.

### Relation with SOFIE

The Semantic Representation component is standalone, it may be used by other SOFIE components and applications as necessary.

## Architecture Overview

This chapter shows different views to explain the component architecture

### Object Flow View

![Alt text](docs/img/object-flow.jpg "Object flow")

| Name                   | Description                                                                                                                                                                                                                                                                 |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IoT Silos              | This element represents an external stakeholder’s composition of IoT devices. They offer functionalities to external users and can be considered like a siloed platform which wants to join a SOFIE enabled platform                                                        |
| SOFIE enabled platform | This is can be considered like a project which is built with the SOFIE framework                                                                                                                                                                                            |
| IoT Silos Data Model   | The data model of the IoT Silos. The SOFIE enabled platform cannot understand this data model                                                                                                                                                                               |
| Federation adapter     | The element is optional, but it translates the IoT silos Data Model into an object which can be used by a SOFIE enabled platform                                                                                                                                            |
| Not Validated SR obj   | This object can be the output of the Federation Adapter or it can be created in any way by the IoT silos owner. It describes the data of the IoT Silos in a structure understandable by the SOFIE enabled platform.                                                         |
| SR component           | This component takes in input an object and return an object which is compliant with the SOFIE enabled platform semantic rules                                                                                                                                              |
| SR Thing Description   | This is the schema supported by the SOFIE enabled platform. Each platform implementation has a different schema, it should be sent to the SR Component as a parameter and can be updated during the SR Component lifetime. It is used to validate the object from IoT Silos |
| SR linter              | This is a sub-component of the Semantic Representation. It validates the object in input with the schema found in the SR Thing Description. If everything is good, it returns a validated object                                                                            |
| Validated SR obj       | The result of the SR linter. Is an object which contains the data of the IoT silos in a structure understandable by the SOFIE enabled platform and its components                                                                                                           |

#### Objects Example

| Thing description                                  |
|----------------------------------------------------|
| ![Thing Description](docs/img/ThingDescriptionExample.png) |

| Valid SR object                          | Not valid SR object                         |
|------------------------------------------|---------------------------------------------|
| ![Valid obj](docs/img/validTDobject.png) | ![Not valid obj](docs/img/NotValidSRobject.png) |

### Sequence diagram

![Sequence Diagram](docs/img/sequence_diagram.png)

## Main Decisions

| Docker image os  | Alpine 3.7 | Widely used os for docker containers           |
|------------------|------------|------------------------------------------------|
| API              | Rest       | A lightweight and widely used API architecture |
| Message protocol | Https      | Dependent on the API choice                    |
| Data schema      | W3C WoT-TD | Dependent on SR component requirements         |
| Data input       | JSON       | Easy to handle with the chosen Data schema     |

### Key Technologies

The software modules are implemented in **Python**.

## Usage

The component is handle as a dockerized webservice 

### Prerequisites

Docker and docker-compose

### configuration

When the docker image starts the components search for these files in the <b>project/static/</b> folder:

- config.yaml

config.yaml must contains these parameters:

```
schema_path: path of the custom schema
iot_schema_path: path of the standard schema (e.g. W3C ThingDescription)
secret_key: 'your-secret'
host: component host addr
port: component host port
debug: True or False
```

### Execution

docker-compose up

## Testing

The `test/` directory contains the scripts to unit test the software modules of the component.

### Running the tests

python3 tests/test_schema.py

### Evaluating the results

At the current state of the implementation, no particular results are logged after the tests.

## Integration

At the current state of the implementation, there is no continuous integration support.

## Deployment 

At the current state of the implementation, there is no continuous deployment support.

## Known and Open issues

## Contact Info

filippo.vimini@aalto.fi

## License

This component is licensed under the Apache License 2.0.
