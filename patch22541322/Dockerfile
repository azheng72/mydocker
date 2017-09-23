FROM oracle/soa:12.2.1.0-quickstart

MAINTAINER Zheng Liang <zheng.liang@precise-soft.com>

USER root

COPY 22541322 /PATCH_TOP/22541322/

RUN chown oracle:oracle -R /PATCH_TOP

USER oracle

WORKDIR /PATCH_TOP/22541322/

RUN /u01/oracle/OPatch/opatch apply -silent

WORKDIR ${ORACLE_HOME}
