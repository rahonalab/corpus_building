# Bert aligner with GPU support (pytorch/cuda)
FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime
RUN apt update && \
    apt install -y software-properties-common gcc build-essential git bash python3-pip python3-dev screen tree
RUN python3 -m pip install pyconll conllu
RUN pip3 install -r https://raw.githubusercontent.com/bfsujason/bertalign/main/requirements.txt
RUN pip3 install -r https://raw.githubusercontent.com/neulab/awesome-align/refs/heads/master/requirements.txt
RUN pip3 install git+https://github.com/bfsujason/bertalign.git
WORKDIR /tmp
RUN git clone https://github.com/neulab/awesome-align.git
RUN python3 /tmp/awesome-aligner/setup.py install
CMD ["/bin/bash"]
