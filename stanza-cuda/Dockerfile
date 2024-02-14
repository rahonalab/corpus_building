# Stanford stanza with GPU support (pytorch/cuda)
#FROM pytorch/pytorch:latest
#FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-devel
FROM anibali/pytorch:latest
#FROM tensorflow/tensorflow:latest-gpu
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt update && \
    apt install -y software-properties-common gcc build-essential git bash python3-pip python3-dev screen
RUN python3 -m pip install pyconll conllu
RUN python3 -m pip install  git+https://github.com/stanfordnlp/stanza.git
CMD ["/bin/bash"]
