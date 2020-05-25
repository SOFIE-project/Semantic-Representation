#!/bin/bash
pip3 install -r /var/semantic-representation/project/requirements.txt

export Flask_APP=run.py

flask db init
flask db migrate -m "init table"
flask db upgrade

python3 /var/semantic-representation/run.py > /var/log/semantic_representation.log