# Stanford stanza on arm64v8 (mac)
FROM arm64v8/python:latest
RUN apt update && \
    apt install -y software-properties-common gcc build-essential git bash python3-pip python3-dev screen tree
RUN python3 -m pip install pyconll conllu
RUN python3 -m pip install  git+https://github.com/stanfordnlp/stanza.git
CMD ["/bin/bash"]
