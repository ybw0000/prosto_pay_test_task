#!/bin/bash

./dc.sh exec server alembic revision --autogenerate -m "$@"
