#! /bin/bash

export PYTHONPATH=$(pwd)

sleep 5

cd app

alembic revision --autogenerate

alembic upgrade head

python3 -m bot.__init__