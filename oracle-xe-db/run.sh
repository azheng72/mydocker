docker run -dit --hostname nfsdxdb -p 1541:1521 -p 5540:5500 --name nfsdxdb-xe --shm-size=2g oracle/db/xe:11.2.0.1.0
