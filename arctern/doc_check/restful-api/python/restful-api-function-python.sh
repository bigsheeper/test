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

# table_schema
curl --location --request GET 'http://localhost:8080/table/schema?table=table_name'
echo "table_schema finished!"
sleep 3