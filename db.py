from datetime import datetime

"""
Test Innings table
CREATE TABLE IF NOT EXISTS test_innings (
    id INT AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    country CHAR(5) NOT NULL,
    score SMALLINT NOT NULL,
    not_out ENUM('T', 'F') DEFAULT 'F',
    minutes SMALLINT,
    balls SMALLINT,
    fours SMALLINT,
    sixes SMALLINT,
    strike_rate FLOAT,
    inn_num TINYINT NOT NULL,
    opposition CHAR(20) NOT NULL,
    ground CHAR(50) NOT NULL,
    match_date DATE NOT NULL,
    match_uri CHAR(50) NOT NULL, 
    PRIMARY KEY (id),
    UNIQUE(name, country, inn_num, match_uri)
)  ENGINE=INNODB;
"""


test_inn_columns = [
    ('name', str),
    ('score', str),  # because it might contain asterisk
    ('minutes', int),
    ('balls', int),
    ('fours', int),
    ('sixes', int),
    ('strike_rate', float),
    ('inn_num', int),
    ('opposition', lambda x: x[2:]),
    ('ground', str),
    ('match_date', lambda x: datetime.strptime(x, '%d %b %Y')),
    ('match_uri', str)
]


def create_record_row(line):
    parts = filter(None, line.strip().split('\t'))
    row_dict = {}
    for col, text in zip(test_inn_columns, parts):
        try:
            row_dict[col[0]] = col[1](text)
        except ValueError:
            row_dict[col[0]] = None
    name_country = row_dict['name']
    bracket_start = name_country.index('(')
    bracket_end = name_country.index(')')
    row_dict['name'] = name_country[:bracket_start].strip()
    row_dict['country'] = name_country[bracket_start + 1: bracket_end].strip()
    row_dict['not_out'] = 'T' if row_dict['score'].endswith('*') else 'F'
    if row_dict['not_out'] == 'T':
        row_dict['score'] = int(row_dict['score'][:-1])
    else:
        row_dict['score'] = int(row_dict['score'])
    return row_dict


def create_inserts(row_dict):
    keys = row_dict.keys()
    values = []
    for k in keys:
        v = row_dict[k]
        if v is None:
            values.append("NULL")
        elif isinstance(v, str):
            values.append('"%s"' % v)
        elif isinstance(v, datetime):
            values.append("'%s'" % v.date().isoformat())
        else:
            values.append(str(v))
    return 'insert into test_innings (%s) values (%s);' % (','.join(keys), ','.join(values))


with open('data/batting.20180903.txt') as f, open('data/inserts.sql', 'w') as w:
    for i, inp in enumerate(f):
        print("Parsing line number %d" % (i + 1))
        w.write(create_inserts(create_record_row(inp)) + '\n')
