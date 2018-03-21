FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="hmmer2go"
LABEL software.version="0.17.5"
LABEL description=""
LABEL website="https://github.com/sestaton/HMMER2GO"
LABEL documentation="https://github.com/sestaton/HMMER2GO/wiki"
LABEL license="https://github.com/sestaton/HMMER2GO/blob/master/LICENSE"
LABEL tags=""

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>

USER root

RUN apt-get update && apt-get install -y emboss cpanminus libxml-libxml-perl

ADD http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2.tar.gz /

RUN tar xf /hmmer-3.1b2.tar.gz && cd hmmer-3.1b2 && ./configure && make && make install

ADD https://github.com/sestaton/HMMER2GO/archive/v0.17.5.tar.gz /

RUN cpanm App::Cmd && cpanm App::Cmd && cpanm  HTML::TableExtract && cpanm \
    IPC::System::Simple && cpanm Try::Tiny

RUN tar xf /v0.17.5.tar.gz && cd HMMER2GO-0.17.5 && perl Makefile.PL && make && make test && make install

USER biodocker

WORKDIR /data/

CMD ["hmmer2go"]