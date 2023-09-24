class Schema:

    DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'

    TABLES = {
        'VISITS': 'visits',
        'REDIRECTS': 'redirects'
    }

    COLUMNS = {
        TABLES['VISITS']: {
            'SLUG': 'slug',
            'DATETIME': 'datetime'
        },
        TABLES['REDIRECTS']: {
            'ID': 'id',
            'SLUG': 'slug',
            'REDIRECT': 'redirect',
            'START_DATETIME': 'start_datetime',
            'END_DATETIME': 'end_datetime'
        }
    }

    SCHEMA = {
        TABLES['VISITS']: {
            'columns':{
                COLUMNS[TABLES['VISITS']]['SLUG']:     [ 'TEXT', 'NOT NULL' ],
                COLUMNS[TABLES['VISITS']]['DATETIME']: [ 'TEXT', 'NOT NULL' ]
            }
        },
        TABLES['REDIRECTS']: {
            'columns':{
                COLUMNS[TABLES['REDIRECTS']]['ID']:             [ 'INTEGER', 'NOT NULL UNIQUE' ],
                COLUMNS[TABLES['REDIRECTS']]['SLUG']:           [ 'TEXT', 'NOT NULL' ],
                COLUMNS[TABLES['REDIRECTS']]['REDIRECT']:       [ 'TEXT', 'NOT NULL' ],
                COLUMNS[TABLES['REDIRECTS']]['START_DATETIME']: [ 'TEXT', 'NOT NULL' ],
                COLUMNS[TABLES['REDIRECTS']]['END_DATETIME']:   [ 'TEXT', 'NOT NULL' ]

            },
            'extra': 'PRIMARY KEY("id" AUTOINCREMENT)'
        }
    }

    QUERIES = {
        "LOG_VISIT":
            'INSERT into ' +TABLES["VISITS"]+ ' (' +COLUMNS[TABLES['VISITS']]['SLUG']+ ',' +COLUMNS[TABLES['VISITS']]['DATETIME']+') VALUES ( "{SLUG}","{DATETIME}" );',
        "DEACTIVE_REDIRECT":
            'UPDATE ' +TABLES["REDIRECTS"]+ ' SET ' +COLUMNS[TABLES['REDIRECTS']]['END_DATETIME']+ '="{{END_DATETIME}}" WHERE ' +COLUMNS[TABLES['REDIRECTS']]['SLUG']+ '="{{SLUG}}" and ' +COLUMNS[TABLES['REDIRECTS']]['END_DATETIME']+ '="";',
        "ADD_REDIRECT":
            'INSERT INTO ' +TABLES["REDIRECTS"]+ ' ( ' +COLUMNS[TABLES['REDIRECTS']]['SLUG']+ ', ' +COLUMNS[TABLES['REDIRECTS']]['REDIRECT']+ ', ' +COLUMNS[TABLES['REDIRECTS']]['START_DATETIME']+ ', ' +COLUMNS[TABLES['REDIRECTS']]['END_DATETIME']+ ' ) VALUES ( "{{SLUG}}", "{{REDIRECT}}", "{{START_DATETIME}}", "" );',
        "GET_ACTIVE_REDIRECT":
            'SELECT ' +COLUMNS[TABLES['REDIRECTS']]['REDIRECT']+ ' FROM ' +TABLES["REDIRECTS"]+ ' WHERE ' +COLUMNS[TABLES['REDIRECTS']]['SLUG']+ '="{{SLUG}}" and end_datetime="";'
    }



    class CreateTable:

        BASE = '''
            CREATE TABLE "{TABLE}" (
            {LINES}
        );'''

        JOIN = ',\n'
        LINE = '"{COLUMN}" {OTHER}'

        @staticmethod
        def prep( table: str ):
                
            lines = []
            for column in Schema.SCHEMA[ table ]['columns']:
                lines.append( Schema.CreateTable.LINE.format( COLUMN=column, OTHER=' '.join(Schema.SCHEMA[ table ]['columns'][column]) ) )

            if 'extra' in Schema.SCHEMA[ table ]:
                lines.append( Schema.SCHEMA[ table ]['extra'] )

            return Schema.CreateTable.BASE.format( TABLE=table, LINES=Schema.CreateTable.JOIN.join(lines) )            







