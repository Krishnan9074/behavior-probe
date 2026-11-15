# Oracle sidecar: the only place the hidden rule exists during the agent's run.
FROM python:3.12-slim
WORKDIR /oracle
COPY . /oracle
EXPOSE 8000
CMD ["python3", "-I", "/oracle/oracle_server.py"]
