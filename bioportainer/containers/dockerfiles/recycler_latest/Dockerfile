FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="recycler"
LABEL software.version="0.62"
LABEL description="an algorithm for detecting plasmids from de novo assembly graphs"
LABEL website="https://github.com/Shamir-Lab/Recycler"
LABEL documentation="https://github.com/Shamir-Lab/Recycler"
LABEL license="https://github.com/Shamir-Lab/Recycler/blob/master/LICENSE"
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>

USER root

RUN apt-get update && apt-get install -y libbz2-dev liblzma-dev \
    && pip install numpy pysam==0.10.0 networkx==1.11 nose==1.3.7

ADD https://github.com/Shamir-Lab/Recycler/archive/master.zip .

RUN unzip -oq master.zip  -d /recycler/ && cd /recycler/Recycler-master \
    && python setup.py install

USER biodocker

WORKDIR /data/

CMD ["recycle.py"]