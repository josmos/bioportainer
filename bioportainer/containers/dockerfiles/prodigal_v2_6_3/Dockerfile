FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="Prodigal"
LABEL software.version="2.6.3"
LABEL description="Prodigal Gene Prediction Software"
LABEL website="https://github.com/hyattpd/Prodigal"
LABEL documentation="https://github.com/hyattpd/prodigal/wiki"
LABEL license="https://github.com/hyattpd/Prodigal/blob/GoogleImport/LICENSE"
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root
ADD https://github.com/hyattpd/Prodigal/archive/v2.6.3.tar.gz /home/biodocker/
RUN cd /home/biodocker/ ; tar -xvzf /home/biodocker/v2.6.3.tar.gz ; cd Prodigal-2.6.3 ; make install INSTALLDIR=/home/biodocker/ ; make
ENV PATH="/home/biodocker/Prodigal-2.6.3//:${PATH}"
USER biodocker

WORKDIR /data/

CMD ["prodigal"]




