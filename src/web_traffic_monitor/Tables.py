from web_traffic_monitor import Columns

class Tables:

    visits = 'visits'
    redirects = 'redirects'

    tables = {
        visits: {
            'columns': [
                        Columns.slug, Columns.datetime
            ]
        },
        redirects: {
        'columns': [
                    Columns.id, Columns.slug, Columns.redirect, Columns.datetime_start, Columns.datetime_end, Columns.is_current
        ]
        }

    }

