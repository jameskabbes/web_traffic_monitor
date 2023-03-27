import datetime
import pytz
import kabbes_nanoid
import pandas as pd
from web_traffic_monitor import Columns

DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'

def get_current_timestamp():

    """returns current timestamp in UTC"""

    dt_now = datetime.datetime.now()
    dt_now_utc = dt_now.astimezone( pytz.utc ) 

    return dt_now_utc

def get_max_timestamp():

    """returns max timestamp"""

    return datetime.datetime.max.replace(tzinfo = pytz.utc)

def turn_df_row_into_kwargs( df_row, columns ):
    
    kwargs = {}
    for col in columns:
        kwargs[ col ] = df_row[ col ]
    return kwargs

def turn_class_atts_into_df_row( instance, columns ):

    dict_df = {}
    for col in columns:
        dict_df[ col ] = [ instance.get_attr( col ) ]

    return pd.DataFrame( dict_df )

def strftime( dt_object ):

    """string from time"""
    return dt_object.strftime( DT_FORMAT )

def strptime( string ):

    """string push time"""
    return datetime.datetime.strptime( string, DT_FORMAT )

def prep_df_for_import( df ):

    for col in df.columns:
        if col in Columns.datetime_cols:
            df[ col ] = df[ col ].apply( lambda string: strptime(string) )

    return df

def prep_df_for_export( df ):

    for col in df.columns:
        if col in Columns.datetime_cols:
            df[ col ] = df[ col ].apply( lambda dt_obj: strftime(dt_obj) )

    return df

def get_nanoid():

    return kabbes_nanoid.generate( alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', size = 20 )

