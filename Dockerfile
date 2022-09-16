FROM python:3.10.7-alpine3.16

RUN apk add --no-cache ca-certificates gettext wget

WORKDIR /MinCostFlow

RUN wget https://raw.githubusercontent.com/gitter-lab/min-cost-flow/main/minCostFlow.py

RUN pip install --upgrade pip
RUN pip install --user ortools==9.3.10497

