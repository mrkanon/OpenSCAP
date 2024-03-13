FROM oraclelinux:8

RUN yum update -y && \
    yum install -y python3 openscap scap-security-guide

COPY ./OscapScanTool /home/.

WORKDIR /home/

RUN python3 -m venv sandbox

RUN source sandbox/bin/activate && pip3 install --upgrade pip && pip3 install lxml

CMD ["/bin/bash"]
