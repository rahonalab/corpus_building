# Bert aligner with GPU support (pytorch/cuda)
FROM pytorch/pytorch:latest
RUN apt update && \
    apt install -y software-properties-common gcc build-essential git bash python3-pip python3-dev screen tree
RUN python3 -m pip install pyconll conllu
RUN pip3 install -r https://raw.githubusercontent.com/bfsujason/bertalign/main/requirements.txt
RUN pip3 install -r https://raw.githubusercontent.com/neulab/awesome-align/refs/heads/master/requirements.txt
RUN pip3 install git+https://github.com/bfsujason/bertalign.git
WORKDIR /tmp
RUN git clone https://github.com/neulab/awesome-align.git
WORKDIR /tmp/awesome-align
RUN python3 setup.py install
# Replace gid/uid with your current user's
RUN groupadd -g 12029 aligner && useradd -m -u 12029 -g aligner aligner
CMD ["/bin/bash"]
