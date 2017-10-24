FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="spades:3.11"
LABEL version="2"
LABEL software="spades"
LABEL software.version="3.11"
LABEL description="SPAdes Genome Assembler"
LABEL website="http://cab.spbu.ru/spades"
LABEL documentation="http://spades.bioinf.spbau.ru/release3.11.0/manual.html"
LABEL license=""
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>

USER root

ADD https://github.com/ablab/spades/releases/download/v3.11.0/SPAdes-3.11.0-Linux.tar.gz /home/biodocker/

RUN cd /home/biodocker/ && tar -xvzf  SPAdes-3.11.0-Linux.tar.gz

ENV PATH /home/biodocker/SPAdes-3.11.0-Linux/bin/:$PATH

USER biodocker

WORKDIR /data/

CMD ["bwa-spades"]

