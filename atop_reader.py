'''Atop logs reader.

Examples:

# read 2 most recent log dumps
for record in iterate_atop_records(list_atop_logs()[-2:]):
    print(record)

# convert to sqlite
iterator = iterate_atop_records(list_atop_logs()[-2:])
conn = to_sqlite('atop.db', iterator)
conn.close()

# print the available predefined atop schema
print(ATOP_SCHEMA)
'''
import os
import re
import glob
from subprocess import Popen, PIPE
from itertools import islice
from collections import defaultdict

from atop_schema import ATOP_SCHEMA


__all__ = [
    'ATOP_SCHEMA',
    'GENERIC_FIELDS',
    'list_atop_logs',
    'iterate_atop_records',
    'parse_atop_schema',
    'to_sqlite',
    'to_pandas',
]


GENERIC_FIELDS = ('type', 'epoch', 'sample_interval', 'sample_n', 'boot_n', 'log_file')
_GENERIC_FIELDS_TYPES = (str, int, int, int, int, str)
_SQL_TYPES = {float: 'REAL', int: 'INT', str: 'TEXT'}

_PRG_RECORD_RX = re.compile(r'^(\S+) \((.+)\) ([^()]+) \((.*)\) ([^()]+)$')
_PRX_RECORD_RX = re.compile(r'^(\S+) \((.*)\) ([^()]+)$')


def parse_atop_schema(text):
    schema = {}
    for type_schema in text.strip().split('\n\n'):
        type_line, *fields = type_schema.splitlines()
        type_, desc = type_line.split(' - ')
        fields = [f.split(' - ') for f in fields]
        schema[type_] = {'desc': desc, 'fields': fields}
    return schema


def list_atop_logs(root='/var/log/atop'):
    'List atop logs from its log directory.'

    path = os.path.join(root, 'atop_[0-9]*')
    return sorted(glob.glob(path))


def iterate_atop_records(files, record_types=('ALL',), binary='atop', infer_types=True):
    '''Iterate through atop records processing each given file sequentially.

    :returns: an iterater that yields tuples of values:
              tuple(*generic_fields, *type_specific_fields)
              to get the list of `generic_fields` see `GENERIC_FIELDS`
              to get the list of `type_specific_fields` see `ATOP_SCHEMA` and `parse_atop_schema`
    '''

    boot_n = 0
    sample_n = -1

    types_cache = {}

    for path in files:
        p = Popen([binary, '-r', path, '-P', ','.join(record_types)], stdout=PIPE, encoding='utf8')

        sample_n += 1

        # first 'RESET' line usually log reset not machine reboot so we skip it
        p.stdout.readline()

        for line in p.stdout:
            if line == 'RESET\n':
                boot_n += 1
                sample_n += 1
            elif line == 'SEP\n':
                sample_n += 1
            else:
                try:
                    type_, _, epoch, _, _, interval, record_text = line.split(maxsplit=6)

                    if type_ == 'PRG':
                        pid, name, vals1, cmd, vals2 = _PRG_RECORD_RX.match(record_text).groups()
                        record_vals = [pid, name] + vals1.split() + [cmd] + vals2.split()
                    elif type_ in ('PRC', 'PRN', 'PRD', 'PRM'):
                        pid, name, vals1 = _PRX_RECORD_RX.match(record_text).groups()
                        record_vals = [pid, name] + vals1.split()
                    else:
                        record_vals = record_text.split()

                        if type_ == 'NET' and record_vals[0] != 'upper':
                            type_ = 'NET_IF'
                        elif type_ == 'cpu':
                            type_ = 'CPU_N'

                    vals = (type_, epoch, interval, sample_n, boot_n, path, *record_vals)

                    if infer_types:
                        if type_ not in types_cache:
                            types_cache[type] = _infer_types(vals)
                        vals = tuple(typ(val) for typ, val in zip(types_cache[type], vals))

                    yield vals
                except Exception:
                    raise Exception('error parsing line: ' + line)


def _infer_types(full_record):
    types = []
    for v in full_record[len(GENERIC_FIELDS):]:
        if re.match(r'^-?\d+(\.\d+)?$', v):
            types.append(float)
        else:
            types.append(str)
    return _GENERIC_FIELDS_TYPES + tuple(types)


def _ensure_schema(full_record, schema):
    fields = (*GENERIC_FIELDS, *[f[0] for f in schema[full_record[0]]['fields']])
    assert len(full_record) == len(fields), (
        'number of fields in the schema does not match number of values in the record; '
        f'expected fields: {fields}; values: {record}')


def to_pandas(iterator, progress=None, schema='default'):
    '''Create pandas datafeame from given iterator returned by `iterate_atop_records`.
    One table per record type.

    :returns: dictionary of dataframes
    '''

    import pandas as pd
    from pandas import DataFrame

    if schema == 'default':
        schema = parse_atop_schema(ATOP_SCHEMA)

    current_file = None
    current_file_i = -1

    chunksize = 10000

    dataframes = {}

    while True:
        chunk = list(islice(iterator, chunksize))
        if not chunk:
            break

        if progress:
            file = chunk[0][5]
            if current_file != file:
                current_file = file
                current_file_i += 1
                progress(current_file_i)

        by_type = defaultdict(lambda: [])

        for record in chunk:
            type_ = record[0]
            if type_ not in dataframes:
                if schema:
                    _ensure_schema(record, schema)
                dataframes[type_] = []

            by_type[type_].append(record)

        for type_, records in by_type.items():
            dataframes[type_].append(DataFrame.from_records(records))

    for type_, parts in dataframes.items():
        df = pd.concat(parts)
        if not schema:
            extra_vals_len = len(df.columns) - len(GENERIC_FIELDS)
            columns = list(GENERIC_FIELDS) + [f'val{n}' for n in range(1, extra_vals_len+1)]
        else:
            columns = list(GENERIC_FIELDS) + [field[0] for field in schema[type_]['fields']]

        df.columns = columns
        dataframes[type_] = df

    return dataframes


def to_sqlite(filename, iterator, progress=None, schema='default', use_types=True):
    '''Create sqlite database from given iterator returned by `iterate_atop_records`.
    One table per record type.

    :returns: open sqlite connection
    '''

    import sqlite3

    if schema == 'default':
        schema = parse_atop_schema(ATOP_SCHEMA)

    conn = sqlite3.connect(filename)
    sql_expr_cache = {}
    current_file = None
    current_file_i = -1

    for record in iterator:
        if progress:
            file = record[5]
            if current_file != file:
                current_file = file
                current_file_i += 1
                progress(current_file_i)

        type_ = record[0]
        if type_ not in sql_expr_cache:

            # create table

            if not schema:
                extra_vals_len = len(record) - len(GENERIC_FIELDS)
                extra_fields = [f'val{n}' for n in range(1, extra_vals_len+1)]
            else:
                extra_fields = [field[0] for field in schema[type_]['fields']]
                _ensure_schema(record, schema)

            sql_types = [_SQL_TYPES[type(v)] for v in record]
            sql_defs = [f'{a} {b}' for a, b in zip((*GENERIC_FIELDS, *extra_fields), sql_types)]
            sql_defs = ', '.join(sql_defs)
            conn.execute(f'CREATE TABLE {type_} ({sql_defs})')

            # cache INSERT expression

            placeholder = ','.join('?' for _ in range(len(record)))
            sql_expr_cache[type_] = f'INSERT INTO {type_} VALUES ({placeholder})'

        # insert
        conn.execute(sql_expr_cache[type_], record)

    conn.commit()
    return conn


if __name__ == '__main__':
    from itertools import islice
    from pprint import pprint

    print('sample records:')
    for record in islice(iterate_atop_records(list_atop_logs()[-1:]), 20):
        print(record)

    schema = parse_atop_schema(ATOP_SCHEMA)
    type_ = 'MEM'
    print(f'\nsample type schema ({type_} - {schema[type_]["desc"]}):')
    pprint(schema[type_]['fields'])

    # import sys
    # files = list_atop_logs()[-1:]
    # iterator = islice(iterate_atop_records(files), 20000)
    # iterator = iterate_atop_records(files)
    # to_sqlite(sys.argv[1], iterator, progress=lambda i: print(files[i]))

    # import sys
    # files = list_atop_logs()[-3:]
    # iterator = islice(iterate_atop_records(files), 50000)
    # iterator = iterate_atop_records(files)
    # frames = to_pandas(iterator, progress=lambda i: print(files[i]))
    # from IPython.terminal import debugger; debugger.set_trace()
