class Columns:

    id = 'id'
    slug = 'slug'
    datetime = 'datetime'
    redirect = 'redirect'
    datetime_start = 'datetime_start'
    datetime_end = 'datetime_end'
    is_current = 'is_current'


    searchable = [ id, slug, redirect ]
    datetime_cols = [ datetime, datetime_start, datetime_end ]

