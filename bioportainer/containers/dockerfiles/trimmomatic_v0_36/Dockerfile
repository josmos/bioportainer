FROM biocontainers/biocontainers:latest

# Metadata
LABEL base.image="biocontainers:latest"
LABEL version="2"
LABEL software="Trimmomatic"
LABEL software.version="0.36"
LABEL description="A flexible read trimming tool for Illumina NGS data"
LABEL website="http://www.usadellab.org/cms/index.php?page=trimmomatic"
LABEL documentation="http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf"
LABEL license=""
LABEL tags="Genomics"

# Maintainer
MAINTAINER Josef Moser <josmos43@gmail.com>
USER root
ADD http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.36.zip .
RUN unzip Trimmomatic-0.36.zip -d /home/biodocker/
USER biodocker
WORKDIR /data/

CMD ["java", "-jar", "trimmomatic-0.36.jar"]




