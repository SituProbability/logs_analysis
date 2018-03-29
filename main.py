#!/usr/bin/env python3

"""Prints out reports based on the data in the database news."""

from newsdb import get_popular_articles, get_popular_authors,\
     get_status_result, get_not_found_result

# HTML template for the report page
HTML_WRAP = '''\
<!DOCTYPE html>
<!DOCTYPE html>
<html>
  <head>
    <title>Report</title>
  </head>
  <body>
    <h3>1. What are the most popular three articles of all time?</h3>
    <ul>
        <li>{popular_articles1}</li>
        <li>{popular_articles2}</li>
        <li>{popular_articles3}</li>
    </ul>
    <h3>2. Who are the most popular article authors of all time?</h3>
    <ul>
    {most_popular_authors}
    </ul>
    <h3>3. On which days did more than 1% of requests lead to errors?</h3>
    <ul>
    {error_status}
    </ul>
  </body>
</html>
'''


def create_output_file(path, content):
    """return a file or overwrite an existing file on the given location."""
    # Create or overwrite the output file
    output_file = open(path, 'w')

    # Output the file
    output_file.write(content)
    output_file.close()
    return output_file


# What are the most popular three articles of all time?
popular_articles = get_popular_articles()
popular_articles1 = (popular_articles[0][0] + " -- " +
                     str(popular_articles[0][1]) + " views")
popular_articles2 = (popular_articles[1][0] + " -- " +
                     str(popular_articles[1][1]) + " views")
popular_articles3 = (popular_articles[2][0] + " -- " +
                     str(popular_articles[2][1]) + " views")

# Who are the most popular article authors of all time?
popular_authors = get_popular_authors()
most_popular_authors = ""
for author in popular_authors:
    most_popular_authors += ("<li>" + author[0] + " -- " +
                             str(author[1]) + " views</li>")

# On which days did more than 1% of requests lead to errors?
status_result = get_status_result()
not_found_result = get_not_found_result()

result = {}
for i in range(len(status_result)):
    if status_result[i][0] == not_found_result[i][0]:
        error = float(not_found_result[i][1]) / float(status_result[i][1])
        if error > 0.01:
            result[status_result[i][0]] = error

error_status = ""
for i in range(len(status_result)):
    if status_result[i][0] in result.keys():
        error_status += ("<li>" + str(status_result[i][0]) + " -- " +
                         "{:0.2f}".format(result[status_result[i][0]] * 100) +
                         "% errors</li>")

# output report
path = "output.html"
content = HTML_WRAP.format(popular_articles1=popular_articles1,
                           popular_articles2=popular_articles2,
                           popular_articles3=popular_articles3,
                           most_popular_authors=most_popular_authors,
                           error_status=error_status)

create_output_file(path, content)
