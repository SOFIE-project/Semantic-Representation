# SOFIE Semantic Representation component

**Table of contents:**

- [Description](#description)
  - [Relation with SOFIE](#relation-with-sofie)
  - [Architecture Overview](#architecture-overview)
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

Docker

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

<b>NB</b> update the ports in the Dockerfile, .env and config.py if needed.
### API
| HTTP Method | Resource URL         | Notes                   |
|-------------|----------------------|-------------------------|
| POST        | /api/add_schema      | Add new schema          |
| POST        | /api/get_schema      | Return a schema         |
| GET         | /api/get_schema/'id' | Return the schema with id = 'id'        |
| POST        | /api/remove_schema   | Remove a schema         |
| POST        | /api/update_schema   | Updates a shema         |
| POST        | /api/extend_schema   | Extend a schema context |

#### Add schema
This endpoint us used to add a schema in the SR component db. The schemas are identified by name which must be unique.
The component will notify is the schema is already saved in the db. e.g. 
```
data = {'name': 'schema_name', 'schema': schema}
requests.post(url, json=data)
```

If a schema extension is added then
```
data = {'name': 'extension name', 'schema': 'schema', 'extended': 'extended schema name'}
requests.post(url, json=data)
```

on success the route respond 
```
Status code: 200

{
    'id': 'schema id',
    'name': 'schema name',
    'schema': 'schema',
    'extended': 'extended schema' // if present
 }
```

If the schema name is already in the db the component respond wit 
```
Status code: 400

{ "error": "Bad Request", "message": "schema name already saved"}'
```
If a some of the minimum information is missing
```
Status code: 400

'{ "error": "Bad Request", "message": "must include schema and schema name"}'
```
#### Get schema
This route returns the schemas information saved in the SR component DB. e.g.
```
data = {'name': 'schema_name'}
requests.post(url, json=data)
```

and it returns
```
Status code: 200

{
    'id': 'schema id',
    'name': 'schema name',
    'schema': 'schema',
    'extended': 'extended schema' // if present
 }
```

If a post request is sent without any data, then the component respond with the info of every schema saved in the db

If the schema is not in the DB then
```
Status code: 400

{'error': 'Bad Request', 'message': 'schema not found'}
``` 

The schema can be retrieved with a get to the endpoint. To get the schema the schema id must be used
```
http:www.example.com/get_schema/1
```
#### Remove schema
This API provide the functionality to remove a schema by its name. e.g.
```
data = {'name': 'schema_name'}
requests.post(url, json=data)
```

If the schema is removed successfully then
```
Status code: 200

{"message": "schema removed"}
```

If the schema is not in the DB
```
Status code: 400

{ "error": "Bad Request", "message": "schema not found"}
```
If the API required information is not satisfied
```
Status code: 400

{ "error": "Bad Request", "message": "must include the schema name"}
```

#### Update schema
This API is used to update the schema in the SR component DB. e.g.
```
data = {'name': 'schema name', 'schema': 'schema'}
requests.post(url, json=data)
```
If the update is successful, then
```
Status code: 200

{
    'id': 'schema id',
    'name': 'schema name',
    'schema': 'schema',
    'extended': 'extended schema' // if present
 }
```
If the schema is not in the DB, then
```
Status code: 400

{ "error": "Bad Request", "message": "schema not found"}
```
If the request data is not correct, then
```
Status code: 400

'{ "error": "Bad Request", "message": "must include schema and schema name"}'
```

#### Validate
This API is used to validate a json messages against a specified schema. e.g.
```
data = {'message': json_msg, 'schema_name': 'schema name'}
requests.post(url, json=data)
```
If the message is valid for the mentioned schema, then
```
{"message": "valid"}
```
If the message is not valid then the component respond with status code 400 and what made the message invalid

## Testing

The component define a series of functional api tests.
These tests check that from a defined input, the output are consistently correct

### Running the tests

The functional tests are in the file tests/tests_api.py
These tests must be run against the active component. Is possible to run the component with a test configuration, 
which is found in tests/test_run.py. To use another configuration, is possible to define it in the config.py file, then 
pass that configuration instead og the test default configuration
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
