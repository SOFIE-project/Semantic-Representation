# SOFIE Semantic Representation component

**Table of contents:**

- [Description](#description)
  - [Relation with SOFIE](#relation-with-sofie)
  - [Architecture Overview](#architecture-overview)
  - [Key Technologies](#key-technologies)

- [Usage](#usage)
  - [Prerequisites](#prerequisites)
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

| Decision         | Technology   | Description                                    |
|------------------|------------  |------------------------------------------------|
| Docker image os  | Ubuntu 18.04 | Easy to handle with the chosen Data schema     |
| API              | Rest         | A lightweight and widely used API architecture |
| Data schema      | W3C WoT-TD   | Dependent on SR component requirements         |
| Data input       | JSON         | Easy to handle with the chosen Data schema     |

### Key Technologies

The software modules are implemented in **Python**.

## Usage

The component is handle as a dockerized webservice 

### Prerequisites

Docker

### Build and Execution

- docker build -t semantic-representation .
- docker run -p 5000:5000 -d -t --name semantic_app semantic-representation

The internal port of the component is 5000, you can change the external port:
- docker run -p "custom_port":5000 -t semantic-representation
remember then to pass the same port as environment variable before running the tests

export PORT="custom_port"

<b>NB</b> update the ports in the Dockerfile, .env and config.py if needed.
### API

OpenApi are available at the following: https://app.swaggerhub.com/apis/filippovimini/semantic-representation_open_api/1.0.0

## Testing

The component define a series of functional api tests.
These tests check that from a defined input, the output are consistently correct

### Running the tests

The functional tests are in the file tests/tests_api.py
These tests must be run against the active component. Is possible to run the component with a test configuration, 
which is found in tests/test_run.py. To use another configuration, is possible to define it in the config.py file, then 
pass that configuration instead og the test default configuration

to run the tests: python3 -m unittest

### Evaluating the results

At the current state of the implementation§ no particular results are logged after the tests.

## Integration

At the current state of the implementation there is no continuous integration support.

## Deployment 

At the current state of the implementation there is no continuous deployment support.

## Known and Open issues
 
 
## Contact Info

filippo.vimini@aalto.fi

## License

This component is licensed under the Apache License 2.0.
