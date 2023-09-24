# web_traffic_monitor
under construction

[Documentation](https://jameskabbes.github.io/web_traffic_monitor)<br>
[PyPI](https://pypi.org/project/kabbes-web-traffic-monitor)

## Users should be able to change

* the db connection and engine
* the schema, column names, etc
* 

## Description
This repo serves a couple of basic purposes:
1. Log visits to a webpage
2. Store redirect slugs to new addresses

The functionality is pretty basic, and the most important piecs are contained in the database schema. A `DB` class (built for sqlite) is provided with the package. Feel free to overwrite the class functionality if you want to use your own database.

## Functionality

* Log a visit to a slug
* Find the active redirect to a given slug
* Add a new redirect (and terminate old redirects) for a given slug

## Schema

### visits table

| slug                     | datetime                |
|--------------------------|-------------------------|
| /home                    | 2023-09-22 08:15:00 UTC |
| /about-us                | 2023-09-23 14:32:00 UTC |
| /contact                 | 2023-09-24 10:45:00 UTC |
| /products/latest-deals   | 2023-09-25 18:20:00 UTC |
| /blog/post-1             | 2023-09-26 09:10:00 UTC |
| /services                | 2023-09-27 12:55:00 UTC |
| /blog/post-2             | 2023-09-28 16:40:00 UTC |
| /portfolio/project-xyz   | 2023-09-29 11:25:00 UTC |
| /products/sale-items     | 2023-09-30 08:50:00 UTC |
| /blog/post-3             | 2023-10-01 13:05:00 UTC |

### redirects table

| nanoid       | slug           | redirect                | start_datetime          | end_datetime            |
|--------------|----------------|-------------------------|-------------------------|-------------------------|
| abcd1234     | /old-page      | /new-page1              | 2023-09-22 08:15:00 UTC | 2023-09-23 14:32:00 UTC |
| efgh5678     | /old-page      | /new-page2              | 2023-09-23 14:32:00 UTC | 2023-09-24 10:45:00 UTC |
| ijkl9012     | /old-page      | /new-page3              | 2023-09-24 10:45:00 UTC | NULL                    |
| mnop3456     | /coming-soon   | /modern-version         | 2023-09-23 14:32:00 UTC | 2023-09-24 10:45:00 UTC |
| qrst7890     | /coming-soon   | /modern-version2        | 2023-09-24 10:45:00 UTC | NULL                    |
| uvwx2345     | /outdated-info | /updated-info           | 2023-09-25 18:20:00 UTC | NULL                    |
| yzab4567     | /contact-old   | /contact-new            | 2023-09-26 09:10:00 UTC | NULL                    |
| cdef6789     | /expired1      | /events/event-2021      | 2023-09-22 08:15:00 UTC | 2023-09-23 14:32:00 UTC |
| ghij7890     | /expired2      | /new-offer              | 2023-09-23 14:32:00 UTC | 2023-09-24 10:45:00 UTC |
| klmn9012     | /expired3      | /fallback-page          | 2023-09-24 10:45:00 UTC | NULL                    |

# Author
James Kabbes