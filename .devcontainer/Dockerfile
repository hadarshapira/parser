FROM mcr.microsoft.com/devcontainers/miniconda:3

COPY tests/environment.yml /tmp/conda-tmp/

RUN conda env create -f /tmp/conda-tmp/environment.yml && rm -rf /tmp/conda-tmp

ENV PATH="/opt/conda/envs/parser/bin:${PATH}"
