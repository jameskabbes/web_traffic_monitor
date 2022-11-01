from web_traffic_monitor import Tables, Columns


def get_active_redirect( slug ) -> str:

    return """
    SELECT {column_redirect} from 
        (SELECT {column_redirect},{column_slug},{column_is_current} from {table_redirects}
        WHERE {column_slug}="{slug}"
        AND {column_is_current}=1)
    """.format( 
        column_redirect = Columns.redirect,
        column_slug = Columns.slug,
        column_is_current = Columns.is_current,
        table_redirects = Tables.redirects, 
        slug = slug
    )

