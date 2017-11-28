FROM biocontainers/biocontainers:latest

################## METADATA ######################
LABEL base.image="biocontainers:latest"
LABEL version="1"
LABEL software="CD-Hit"
LABEL software.version="4.6.8"
LABEL description="A fast program for clustering and comparing large sets of protein or nucleotide sequences."
LABEL website="http://weizhongli-lab.org/cd-hit/"
LABEL documentation="https://github.com/weizhongli/cdhit/wiki"
LABEL license="https://github.com/weizhongli/cdhit/blob/master/license.txt"
LABEL tags="Genomics"


################## BEGIN INSTALLATION ######################
USER root

ENV ZIP=cd-hit-v4.6.8-2017-0621-source.tar.gz
ENV URL=https://github.com/weizhongli/cdhit/releases/download/V4.6.8
ENV FOLDER=cd-hit-v4.6.8-2017-0621
ENV DST=/home/biodocker/bin

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    tar -xvzf $DST/$ZIP -C $DST && \
    rm $DST/$ZIP && \
    mv $DST/$FOLDER/* $DST && \
    cp $DST/$FOLDER/.DS_Store $DST && \
    rm -rf $DST/$FOLDER && \
    cd $DST ; make && \
    cd $DST/cd-hit-auxtools ; make


USER biodocker

# CHANGE WORKDIR TO /DATA
WORKDIR /data

# DEFINE DEFAULT COMMAND
CMD ["cd-hit"]

##################### INSTALLATION END #####################

# File Author / Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>





