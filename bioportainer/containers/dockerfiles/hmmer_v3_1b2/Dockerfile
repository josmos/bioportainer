FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="Hmmer"
LABEL software.version="3.1b2"
LABEL description="biosequence analysis using profile hidden Markov models"
LABEL website="http://hmmer.org/"
LABEL documentation="http://hmmer.org/documentation.html"
LABEL license=""
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root

ADD http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2.tar.gz /home/biodocker/
RUN cd /home/biodocker/ && \
  tar -xvzf /home/biodocker/hmmer-3.1b2.tar.gz && \
  cd hmmer-3.1b2 && \
  ./configure --prefix /home/biodocker && \
  make && \
  rm /home/biodocker/hmmer-3.1b2.tar.gz

ENV PATH /home/biodocker/hmmer-3.1b2/src/:$PATH

USER biodocker

CMD ["hmmalign"]
