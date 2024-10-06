ARG TAG="3.12"

FROM python:${TAG}

ARG UID="1000"
ARG GID="1000"

ENV PRE_COMMIT_HOME="/code/.cache/pre-commit"

RUN groupadd --gid ${GID} user \
    && useradd --uid ${UID} --gid user --shell /bin/bash --create-home user

USER user

WORKDIR /code

RUN pip install --no-cache-dir \
    coverage \
    mypy \
    pre-commit \
    ruff

COPY setup.py setup.py
COPY README.md README.md
RUN pip install --no-cache-dir -e .

ENTRYPOINT [ "bash" ]
