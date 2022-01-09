# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
FROM python:3.10-bullseye as builder

WORKDIR /opt
COPY ya3-report.tar.gz .
RUN pip install -U pip \
 && pip install ya3-report.tar.gz

FROM python:3.10-slim-bullseye as runner
RUN pip install -U pip \
  && pip install jupyter
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

WORKDIR /ya3
RUN mkdir data
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "ya3-report" ]