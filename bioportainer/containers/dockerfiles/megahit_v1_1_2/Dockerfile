FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="Megahit"
LABEL software.version="1.1.2"
LABEL description="An ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph"
LABEL website="https://github.com/voutcn/megahit/releases"
LABEL documentation="https://github.com/voutcn/megahit/wiki"
LABEL license="https://github.com/voutcn/megahit/blob/master/LICENSE"
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root
ADD https://github.com/voutcn/megahit/releases/download/v1.1.2/megahit_v1.1.2_LINUX_CPUONLY_x86_64-bin.tar.gz .
RUN tar -xvzf megahit_v1.1.2_LINUX_CPUONLY_x86_64-bin.tar.gz -C /home/biodocker/
USER biodocker
ENV PATH="/home/biodocker/megahit_v1.1.2_LINUX_CPUONLY_x86_64-bin/:${PATH}"

WORKDIR /data/

CMD ["megahit"]
