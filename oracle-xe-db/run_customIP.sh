docker run -dit --net mynet --ip 172.18.0.2 -p 1531:1521 -p 5510:5500 --name oracle-db-xe-1 --shm-size=2g oracle/db/xe:11.2.0.1.0
