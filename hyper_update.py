import pandas as pd
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, NOT_NULLABLE, NULLABLE, SqlType, \
    TableDefinition, Inserter, escape_name, escape_string_literal, HyperException, TableName

df = pd.read_csv(r"C:\Users\Gareth\PycharmProjects\pantab\test_data_new.csv")
df = df.dropna(how='all')
# create a list of column names
col_names = df.columns
# create a list of column types
col_types = df.dtypes

# dispatch table to work out what SQLType to assign the column
def get_type(column_type):
    dispatch = {
        'int64': SqlType.int(),
        'object': SqlType.text(),
        'float64': SqlType.double(),
    }
    var = dispatch[column_type]
    return var


columns = []
for i in range(0, len(col_names)):
    col_name = col_names[i]  # header of column
    col_type = col_types[i]  # pandas data type of column
    # print(col_name)
    # print(col_type)
    columns.append(TableDefinition.Column(col_name, get_type(str(col_type)), NULLABLE))


with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    print("The HyperProcess has started.")
    with Connection(hyper.endpoint, 'test_hyper.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        print("The connection to the Hyper file is open.")
        connection.catalog.create_schema('Extract')

        example_table = TableDefinition(TableName('auto_rpa'),
                                        columns=columns
                                        )
        print("The table is defined.")
        connection.catalog.create_table(example_table)
        with Inserter(connection, example_table) as inserter:
            for i in df.values.tolist():
                inserter.add_row(i)
            inserter.execute()
        print("The data was added to the table.")
    print("The connection to the Hyper extract file is closed.")
print("The HyperProcess has shut down.")
