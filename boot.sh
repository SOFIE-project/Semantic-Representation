#!/bin/bash
pip3 install -r /var/semantic-representation/project/requirements.txt

python3 /var/semantic-representation/run.py > /var/log/semantic_representation.log