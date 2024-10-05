ARG TAG="3.12"

FROM python:${TAG}

ARG UID="1000"
ARG GID="1000"

ENV PRE_COMMIT_HOME="/code/.cache/pre-commit"

RUN groupadd --gid ${GID} user \
    && useradd --uid ${UID} --gid user --shell /bin/bash --create-home user

USER user

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "bash" ]
