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

Docker and docker-compose

### configuration

Component configuration can be handled creating a file .env in the root of the component folder:

- .env:

```
SECRET_KEY = '1234'
HOST = 127.0.0.1
PORT = 5000
DEBUG = False
DATABASE_URL = sqlite:///project/app.db
```
to further control the component configuration, the file config.py holds two classes that represent production and test
 configuration 

### Build and Execution

- docker build /"Dockerfile folder"/ -t semantic-representation
- docker run -p 5000:5000 -t semantic-representation

<b>NB</b> update the ports in the Dockerfile, docker-compose file and config.yaml if needed.
### API
| HTTP Method | Resource URL         | Notes                   |
|-------------|----------------------|-------------------------|
| POST        | /api/add_schema      | Add new schema          |
| POST        | /api/get_schema      | ToDO                    |
| GET         | /api/get_schema/<id> | Return a schema         |
| POST        | /api/remove_schema   | Remove a schema         |
| POST        | /api/update_schema   | Updates a shema         |
| POST        | /api/extend_schema   | Extend a schema context |

### Output

The component produce an outputs when a JSON object is sent to the component:

If a Valid JSON object is sent the response will be JSON with the tuple status: "success" and the data key with empty value 
```
{'status': 'success', 'data': 'null'}
```

If an invalid JSON object is sent the response will be a JSON
with the tuple status: "fail" and the information about the error
and the component schema as value of the data key. Example below:

```
{
    "status": "fail",
    "data": {
        "message": "'lockerId' is a required property",
        "schema": {
            "$id": "http://smaugexample.com/schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "@context": [
                "https://www.w3.org/2019/wot/td/v1"
            ],
            "properties": {
                "authServiceUrl": {
                    "description": "The authorization server url",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "type": "string"
                },
                "location": {
                    "description": "The latitude and longitude of the locker in degrees",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "properties": {
                        "latitude": {
                            "forms": [
                                {
                                    "href": "//api/status"
                                }
                            ],
                            "maximum": 90,
                            "minimum": -90,
                            "type": "number"
                        },
                        "longitude": {
                            "forms": [
                                {
                                    "href": "//api/status"
                                }
                            ],
                            "maximum": 180,
                            "minimum": -180,
                            "type": "number"
                        }
                    },
                    "required": [
                        "latitude",
                        "longitude"
                    ],
                    "type": "object"
                },
                "lockerId": {
                    "description": "The unique identifier of the locker",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "type": "integer"
                },
                "price": {
                    "description": "The price for the locker",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "maximum": 50,
                    "minimum": 0,
                    "type": "integer"
                },
                "smartContractAdds": {
                    "description": "The smart contract address of the locker",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "type": "string"
                },
                "volume": {
                    "description": "The volume of the locker in cc",
                    "forms": [
                        {
                            "href": "//api/status"
                        }
                    ],
                    "minimum": 0,
                    "type": "integer"
                }
            },
            "required": [
                "lockerId",
                "price",
                "volume"
            ],
            "security": [
                "bearer_sc"
            ],
            "securityDefinitions": {
                "bearer_sc": {
                    "alg": "ES256",
                    "description": "bearer token available to locker renter",
                    "format": "jwt",
                    "in": "header",
                    "scheme": "bearer"
                }
            },
            "title": "SMAUG data model schema",
            "type": "object"
        }
    }
}
```

## Testing

The `test/` directory contains the scripts to unit test the software modules of the component. 
To perform functional tests you must create 2 files:
- tests/static/custom_valid_requests.json
- tests/static/custom_invalid_requests.json

The first file must contains the valid JSON objects, based on the schema (config.yaml -> schema_path). 

The second file must contain the not valid JSON objects, based on the schema (config.yaml -> schema_path).

Examples are in:
- tests/static/default_valid_requests.json
- tests/static/default_invalid_requests.json

### Running the tests

The first test file performs UNIT tests on the validation function:

```
python3 tests/test_validation.py
```

The second test file performs POST requests using as input the JSON object in the file created in the previous chapter.

```
python3 tests/test_requests.py
```
<b>NB</b> RUN the component before stating the SECOND test

The third test file is used to check that the custom schema (config.yaml -> schema_path) created ad-hoc 
for the specific use of this component is congruent with the W3C TD standard.

```
test_custom_schema_validation.py
```
The test return "valid" if the custom schema is congruent with the W3C TD standard. 
Otherwise it return an error messages with the description of the problems

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
