curl --header "Content-Type: application/json"   --request POST   --data '{"username":"xyz","password":"xyz"}'   http://0.0.0.0:5000/api/v1/validate

curl --header "Content-Type: application/json"   --request POST   --data '{"lockerId":1234,"price":35, "volume":15}'   http://0.0.0.0:5000/api/v1/validate

curl --header "Content-Type: application/json"   --request POST   --data '{"lockerId":1234,"price":100, "volume":15}'   http://0.0.0.0:5000/api/v1/validate

curl --header "Content-Type: application/json"   --request POST   --data '{"lockerId":1234,"price":-5, "volume":15}'   http://0.0.0.0:5000/api/v1/validate

