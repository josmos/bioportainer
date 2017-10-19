FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="Prokka"
LABEL software.version="1.12"
LABEL description="Rapid prokaryotic genome annotation"
LABEL website="https://github.com/tseemann/prokka"
LABEL documentation="https://github.com/tseemann/prokka#command-line-options"
LABEL license=""
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root

RUN RUN apt-get update && apt-get install -y libdatetime-perl \
   libxml-simple-perl \
   libdigest-md5-perl \
   git \
   default-jre \
   bioperl

ADD https://github.com/tseemann/prokka/archive/v1.12.tar.gz /home/biodocker/
RUN cd /home/biodocker/ && \
  tar -xvzf /home/biodocker/v1.12.tar.gz && \
  rm /home/biodocker/v1.12.tar.gz

ENV PATH /home/biodocker/prokka-1.11/bin/:$PATH

USER biodocker

CMD ["prokka"]



