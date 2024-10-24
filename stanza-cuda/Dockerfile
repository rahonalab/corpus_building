# Stanford stanza with GPU support (pytorch/cuda)
FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime
RUN apt update && \
    apt install -y software-properties-common gcc build-essential git bash python3-pip python3-dev screen tree
RUN python3 -m pip install pyconll conllu
RUN python3 -m pip install  git+https://github.com/stanfordnlp/stanza.git
# Replace gid/uid with your current user's
RUN RUN groupadd -g 12029 parser && useradd -m -u 12029 -g parser parser
CMD ["/bin/bash"]
