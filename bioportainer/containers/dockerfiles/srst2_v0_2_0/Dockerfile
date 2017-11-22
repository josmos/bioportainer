FROM biocontainers/biocontainers:latest

################## METADATA ######################
LABEL base.image="biocontainers:latest"
LABEL version="1"
LABEL software="SRST2"
LABEL software.version="0.2.0"
LABEL description="Short Read Sequence Typing for Bacterial Pathogens"
LABEL website="https://github.com/katholt/srst2"
LABEL documentation="http://bioinf.spbau.ru/spades"
LABEL license="https://github.com/katholt/srst2/blob/master/LICENSE.txt"
LABEL tags="Genomics"


################## BEGIN INSTALLATION ######################
USER root

ENV ZIP=bowtie2-2.2.9-linux-x86_64.zip
ENV URL=https://github.com/BenLangmead/bowtie2/releases/download/v2.2.9/
ENV FOLDER=bowtie2-2.2.9
ENV TAR=v0.2.0.tar.gz
ENV URL2=https://github.com/katholt/srst2/archive/
ENV FOLDER2=srst2-0.2.0
ENV DST=/home/biodocker/bin

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    unzip $DST/$ZIP -d $DST && \
    rm $DST/$ZIP && \
    mv $DST/$FOLDER/* $DST && \
    rmdir $DST/$FOLDER && \
    conda install samtools=1.3.1 && \
    pip install numpy scipy && \
    wget $URL2/$TAR -O $DST/$TAR && \
    tar -xvzf $DST/$TAR -C $DST && \
    rm $DST/$TAR && \
    cd $DST/$FOLDER2/ && \
    pip install . && \
    bowtie2-build $DST/$FOLDER2/data/ARGannot.r1.fasta $DST/$FOLDER2/data/ARGannot.r1.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/ARGannot.fasta $DST/$FOLDER2/data/ARGannot.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/EcOH.fasta $DST/$FOLDER2/data/EcOH.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/LEE_mlst.fasta $DST/$FOLDER2/data/LEE_mlst.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/Plasmid18Replicons.fasta $DST/$FOLDER2/data/Plasmid18Replicons.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/PlasmidFinder.fasta $DST/$FOLDER2/data/PlasmidFinder.fasta  && \
    bowtie2-build $DST/$FOLDER2/data/ResFinder.fasta $DST/$FOLDER2/data/ResFinder.fasta && \
    mkdir /data_db && mv $DST/$FOLDER2/data/* /data_db/

USER biodocker

# CHANGE WORKDIR TO /DATA
WORKDIR /data

# DEFINE DEFAULT COMMAND
CMD ["srst2"]

##################### INSTALLATION END #####################

# File Author / Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>

# srst2 --input_pe strainA_1.fastq.gz strainA_2.fastq.gz --output strainA_test --log --gene_db resistance.fasta