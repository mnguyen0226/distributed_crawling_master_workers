# build the image, this should auto build customed image
# docker compose build 

#!/bin/bash
docker compose up --scale worker=3