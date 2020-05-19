import requests
import json

# command
url = "http://localhost:8080/command"

payload = {
    "command": "import sys\nprint(len(sys.argv))"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("command finished!")
import time
time.sleep(3)


# loadfile
url = "http://localhost:8080/loadfile"

# /path/to/data.csv文件内容样例如下：
"""
column0, column1, column2
str1, 0.1, 1
str2, 0.2, 2
str3, 0.3, 3
"""
payload = {
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
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("loadfile finished!")
import time
time.sleep(3)

# query1
url = "http://localhost:8080/query"

payload = {
    "sql": "select * from table_name limit 1",
    "collect_result": "1"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("query1 finished!")
import time
time.sleep(3)

# query2
url = "http://localhost:8080/query"

payload = {
    "sql": "create table new_table as (select * from table_name)",
    "collect_result": "0"
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("query2 finished!")
import time
time.sleep(3)

# save file
url = "http://localhost:8080/savefile"

payload = {
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
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("save file finished!")
import time
time.sleep(3)


# table schema
url = "http://localhost:8080/table/schema?table=table_name"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text.encode('utf8'))
print("table schema finished!")