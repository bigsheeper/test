# command
curl --location --request POST 'http://localhost:8080/command' \
--header 'Content-Type: application/json' \
--data-raw '{
	"command":"import sys\nprint(len(sys.argv))"
}'
echo "command finished!"
sleep 3

# loadfile
curl --location --request POST 'http://localhost:8080/loadfile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tables": [
        {
            "name": "table_name",
            "format": "csv",
            "path": "/home/sheep/workspace/arctern/sheep/test/arctern/doc_check/restful-api/data.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {
                    "column0": "string"
                },
                {
                    "column1": "double"
                },
                {
                    "column2": "int"
                }
            ]
        }
    ]
}'
echo "loadfile finished!"
sleep 3

# query1
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}'
echo "query1 finished!"
sleep 3

# drop table
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sql": "drop table if exists new_table",
    "collect_result": "0"
}'
echo "drop table finished!"
sleep 3

# query2
curl --location --request POST 'http://localhost:8080/query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}'
echo "query2 finished!"
sleep 3

# savefile
curl --location --request POST 'http://localhost:8080/savefile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tables": [
        {
            "sql": "select * from table_name",
            "format": "csv",
            "path": "/home/sheep/workspace/arctern/sheep/test/arctern/doc_check/restful-api/test_save_file.csv",
            "options": {
                "header": "True",
                "delimiter": ","
            }
        }
    ]
}'
echo "savefile finished!"
sleep 3

# table_schema
curl --location --request GET 'http://localhost:8080/table/schema?table=table_name'
echo "table_schema finished!"
sleep 3