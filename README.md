# Tools for process corpora
* ud-stanza-ciep: Parse texts into UD conllu files (CIEP+ version)
* ud-stanza-other: Parse texts into UD conllu files (everything-but-CIEP+ version)
* pipeline/: pipelines for building corpora (may be outdated)
* parsing/: parser functions
* export/: export tools
* stanza-cuda/: A Dockerfile for running ud-stanza scripts on GPU, using CUDA

# How to run these scripts using Docker

0. If you are on a system without the stanzacuda image i.e., your laptop first clone this repository:

```git
git clone https://github.com/rahonalab/corpus_building.git
```

Then, build the stanzacuda image:

```bash
cd parallelcorpus-tools/stanza-cuda; docker build
```

1. Once you have a stanzacuda image available on your system, you can create a container:

```bash
docker run  -u $(id -u):$(id -g) --gpus all -d -t --name <the_name_of_your_container>           -v <local_path_to_raw_texts>:<mapping_to_container_path> -v <local_path_to_stanza_resources>:/stanza_resources          -v <local_path_to_these_scripts>:/tools verkerklab/stanzacuda:0.5
```

2. Create the structure for conllu, metadata and xml files: (optional)

```bash
mkdir -p <corpus>/{conllu,metadata,xml}
```

3. Finally, you can run the parsing script with:

```bash
docker exec -it <the_name_of_your_container> python3 /tools/ud-stanza-other.py -s <container_path_to_raw_texts> -t <container_path_to_conllu_files> -m <container_path_to_metadata_files> -l <language_model_in_iso6639-1> -p tokenize,lemma,pos,depparse -c <corpus: rsc>
```

4. You can also export files in xml format, for instance for encoding your conllu corpus in Corpus Workbench. The following command merges the metadata and the conllu files in xml files:

```bash
docker exec -it <the_name_of_your_container> python3 /tools/export/conllu2vrt.py -c <container_path_to_conllu_files> -m <container_path_to_metadata_files> -x <container_path_to_xml_files>
```
 
