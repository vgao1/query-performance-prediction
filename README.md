# Query Performance Prediction

## TPC-H Dataset Generation
1. Clone this repository
2. In a terminal, run `cd query-performance-prediction/dbgen`
3. Modify `makefile.suite` file in the `dbgen` folder:
```
  CC       = gcc
  DATABASE = INFORMIX
  MACHINE  = LINUX
  WORKLOAD = TPCH
```
4. Compile the dbgen tool by running `make -f makefile.suite`. You may be prompted to install developer tools before this command can run without errors. <br>
   Note: For Mac OS, the import statement for malloc in bm_utils.c and varsub.c files is `#include <sys/malloc.h>`. For other OS, you may need to use `#include <malloc.h>` instead.
6. Run `./dbgen -s <scale factor> -v` with `<scale factor>` replaced with an integer (i.e., 10)
7. There is a bug in dbgen which generates an extra | at the end of each line. To fix it, run the following command:
```
for i in `ls *.tbl`; do sed 's/|$//' $i > ${i/tbl/csv}; echo $i; done;
```
Source: https://gist.github.com/yunpengn/6220ffc1b69cee5c861d93754e759d08

## PostgreSQL Setup
1. Install Postgres.app and follow steps on https://postgresapp.com
2. In a terminal, setup a database without indexes named tpc by running
```
psql -c "CREATE DATABASE tpc"

# Creates the schema
psql -d tpc -f dss.ddl

# Adds primary keys & foreign keys.
psql -d tpc -f dss.ri

# Loads data.
psql -d tpc -c "\copy region FROM 'region.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy nation FROM 'nation.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy customer FROM 'customer.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy supplier FROM 'supplier.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy part FROM 'part.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy partsupp FROM 'partsupp.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy orders FROM 'orders.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc -c "\copy lineitem FROM 'lineitem.csv' WITH (FORMAT csv, DELIMITER '|')";
```

3. In a terminal, setup a database with indexes named tpc_citus_index by running
```
psql -c "CREATE DATABASE tpc_citus_index"

# Creates the schema
psql -d tpc_citus_index -f dss.ddl

# Adds primary keys & foreign keys.
psql -d tpc_citus_index -f dss.ri

# Loads data.
psql -d tpc_citus_index -c "\copy region FROM 'region.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy nation FROM 'nation.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy customer FROM 'customer.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy supplier FROM 'supplier.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy part FROM 'part.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy partsupp FROM 'partsupp.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy orders FROM 'orders.csv' WITH (FORMAT csv, DELIMITER '|')";
psql -d tpc_citus_index -c "\copy lineitem FROM 'lineitem.csv' WITH (FORMAT csv, DELIMITER '|')";
```
<br>
From the Postgres application, open a SQL shell connected to the tpc_citus_index database by clicking on the cylinder labeled "tpc_citus_index". In that shell, run: 

```
CREATE INDEX IDX_SUPPLIER_NATION_KEY ON SUPPLIER (S_NATIONKEY);
CREATE INDEX IDX_PARTSUPP_PARTKEY ON PARTSUPP (PS_PARTKEY);
CREATE INDEX IDX_PARTSUPP_SUPPKEY ON PARTSUPP (PS_SUPPKEY);
CREATE INDEX IDX_CUSTOMER_NATIONKEY ON CUSTOMER (C_NATIONKEY);
CREATE INDEX IDX_ORDERS_CUSTKEY ON ORDERS (O_CUSTKEY);
CREATE INDEX IDX_LINEITEM_ORDERKEY ON LINEITEM (L_ORDERKEY);
CREATE INDEX IDX_LINEITEM_PART_SUPP ON LINEITEM (L_PARTKEY,L_SUPPKEY);
CREATE INDEX IDX_NATION_REGIONKEY ON NATION (N_REGIONKEY);
CREATE INDEX IDX_LINEITEM_SHIPDATE ON LINEITEM (L_SHIPDATE, L_DISCOUNT, L_QUANTITY);
CREATE INDEX IDX_ORDERS_ORDERDATE ON ORDERS (O_ORDERDATE);
```

## Query Execution Time Data Collection
1. Navigate to `Queries` folder in this reposity. In this folder, edit `run_sql_files.sh` file:
- Replace `<current user>` value of the DB_USER variable with the value you see after running "SELECT current_user;" in PostgreSQL shell
- Edit DB_HOST and DB_PORT values as needed
2. For the first trial, 
  - No index database: use the following variable values:
      - DB_NAME="tpc"
      - SQL_FILE_LIST="no_index_queries.txt"
      - OUTPUT_DIR = "results_no_index_trial1" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.
  - Indexed database: use the following variable values:
      - DB_NAME="tpc_citus_index"
      - SQL_FILE_LIST="index_queries.txt"
      - OUTPUT_DIR = "results_index_trial1" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.

Once all the query variations finish executing for both databases, edit `record_exec_times_csv.py` in the Queries folder:
  - no_index_folder_name = "results_no_index_trial1/"
  - index_folder_name = "results_index_trial1/"
  - output_file_path = "trial1_exec_times.csv"

Lastly, run the Python script, which should generate `trial1_exec_times.csv` file in the Queries folder.
<br>
3. For the second trial,
  - No index database: use the following variable values:
      - DB_NAME="tpc"
      - SQL_FILE_LIST="no_index_queries.txt"
      - OUTPUT_DIR = "results_no_index_trial2" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.
  - Indexed database: use the following variable values:
      - DB_NAME="tpc_citus_index"
      - SQL_FILE_LIST="index_queries.txt"
      - OUTPUT_DIR = "results_index_trial2" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.

Once all the query variations finish executing for both databases, edit `record_exec_times_csv.py` in the Queries folder:
  - no_index_folder_name = "results_no_index_trial2/"
  - index_folder_name = "results_index_trial2/"
  - output_file_path = "trial2_exec_times.csv"

Lastly, run the Python script, which should generate `trial2_exec_times.csv` file in the Queries folder.
<br>
4. For the third trial,
  - No index database: use the following variable values:
      - DB_NAME="tpc"
      - SQL_FILE_LIST="no_index_queries.txt"
      - OUTPUT_DIR = "results_no_index_trial3" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.
  - Indexed database: use the following variable values:
      - DB_NAME="tpc_citus_index"
      - SQL_FILE_LIST="index_queries.txt"
      - OUTPUT_DIR = "results_index_trial3" <br>
    Then, run `./run_sql_files.sh` in the Queries folder.

Once all the query variations finish executing for both databases, edit `record_exec_times_csv.py` in the Queries folder:
  - no_index_folder_name = "results_no_index_trial3/"
  - index_folder_name = "results_index_trial3/"
  - output_file_path = "trial3_exec_times.csv"

Lastly, run the Python script, which should generate `trial3_exec_times.csv` file in the Queries folder.
<br>
5. Copy and paste SQL_query column in [trial1_exec_times.csv](https://github.com/vgao1/query-performance-prediction/blob/main/EXPLAIN%20ANALYZE%20results/trial1_exec_times.csv) into your `trial1_exec_times.csv`, `trial2_exec_times.csv`, and `trial3_exec_times.csv` files’ Sql_query column
