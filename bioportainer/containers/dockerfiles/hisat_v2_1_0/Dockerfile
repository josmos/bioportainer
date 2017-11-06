FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="hisat2"
LABEL software.version="2.1.0"
LABEL description="Graph-based alignment (Hierarchical Graph FM index)"
LABEL website="https://github.com/infphilo/hisat2"
LABEL documentation="http://ccb.jhu.edu/software/hisat/manual.shtml"
LABEL license="https://github.com/infphilo/hisat2/blob/master/LICENSE"
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root

RUN wget --directory-prefix=/home/biodocker/ ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-Linux_x86_64.zip
RUN cd /home/biodocker/ && \
  unzip /home/biodocker/hisat2-2.1.0-Linux_x86_64.zip && \
  rm /home/biodocker/hisat2-2.1.0-Linux_x86_64.zip

ENV PATH /home/biodocker/hisat2-2.1.0/:$PATH

USER biodocker

CMD ["hisat2"]