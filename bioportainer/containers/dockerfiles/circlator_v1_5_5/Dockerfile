FROM biocontainers/biocontainers:latest
MAINTAINER Paul Pham <docker@aquaron.com>

USER root


RUN conda install bwa=0.7.15

RUN conda install samtools=1.3.1

ADD https://github.com/mummer4/mummer/releases/download/v4.0.0beta2/mummer-4.0.0beta2.tar.gz /mummer.tar.gz

RUN cd / \
 && tar -xvzf mummer.tar.gz \
 && cd mummer-4.0.0beta2 \
 && ./configure \
 && make \
 && make install

ENV ZIP=SPAdes-3.6.0-Linux.tar.gz
ENV URL=https://github.com/BioDocker/software-archive/releases/download/spades
ENV FOLDER=SPAdes-3.6.0-Linux
ENV DST=/home/biodocker/bin

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    tar xvf $DST/$ZIP -C $DST && \
    rm $DST/$ZIP && \
    cd $DST/$FOLDER && \
    mv $DST/$FOLDER/bin/* /home/biodocker/bin && \
    rm -rf $DST/$FOLDER

RUN conda install prodigal

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y samtools perl python3-pip

RUN pip3 install --upgrade --no-cache-dir pip \
 && pip3 install --no-cache-dir circlator \
 && circlator progcheck

RUN conda install amos

COPY toAmos /usr/local/bin

USER biodocker

WORKDIR /data

CMD ["circlator"]


