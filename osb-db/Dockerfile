FROM oracle/database:12.1.0.2-ee

ENV ORACLE_SID=ORCL \
    ORACLE_PDB=OSB

COPY ./addfiles $ORACLE_BASE/addfiles

RUN $ORACLE_BASE/addfiles/myrunOracle.sh

CMD $ORACLE_BASE/$RUN_FILE
