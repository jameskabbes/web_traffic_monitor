class DB:

    def __init__( self, schema ):

        self.schema = schema
        tables = self.get_tables()
        print (tables)
        for table in self.schema.TABLES:
            if self.schema.TABLES[ table ] not in tables: 
                self.create_table( table )

    def execute_and_commit( self, string: str ):
        self.execute( string )
        self.commit()

    def get_tables( self ):
        return [ row[0] for row in self.query( self.GET_TABLES_QUERY ) ]

    def create_table( self, table: str ):
        string = self.schema.create_table_query( table )
        self.execute( string )
