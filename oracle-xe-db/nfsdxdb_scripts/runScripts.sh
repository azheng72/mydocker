cd /u01/app/oracle/product/11.2.0/xe/bin

echo exit | ./sqlplus sys/welcome1@0.0.0.0:1521 as sysdba @/nfsdxdb_scripts/createUserNfsdx.sql

echo exit | ./sqlplus nfsdx/nfsdx123@0.0.0.0:1521/XE @/nfsdxdb_scripts/NFSDX-DDL-creates_Release2.sql

echo exit | ./sqlplus nfsdx/nfsdx123@0.0.0.0:1521/XE @/nfsdxdb_scripts/grantsNfsdxUser.sql
