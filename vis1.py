#!/usr/bin/env python3
"""Quick hack to produce a visualization of color usage in McCarthy's novel
The Road. Data included is based on http://is.gd/road_colors; incomplete info
or other errors should be reported as noted on that page.

This script produces one three-pixel-wide bar for each page in the novel,
splitting that bar vertically into however many colors are mentioned on that
page, and drawing each of those colors with equal vertical space in that bar.
Pages that mention no colors at all are made transparent_color (currently, 
very very dark gray, visually indistinguishable from black) so that the color
can be made transparent later in a graphics editor.

This is, after all, a quick hack, not a producer of a beautiful visualization,
and many things are suboptimal from one viewpoint or another. For instance,
the colors used are often HTML defaults and often (probably) don't map closely
to what McCarthy had in mind; my guess is that HTML 'green' (#00FF00) is 
probably not an actual representation of any of the ten occurrences of the
word 'green' in the novel. Similarly, splitting space evenly in single bars is
really not an acurate representation of where the word falls on the page,
which is maybe what we should be plotting. 

I'd love suggestions on how to do this better. This is a first attempt.

Script by Patrick Mooney; last update was 27 Oct 2015. If you find it useful,
you are welcome to use and adapt this script. It is licensed under the GPL v3
or (at your option) any later version. A copy of this license is in the file
LICENSE.md."""

import turtle
from pprint import pprint
import sys
import csv
import collections

data_file_name = 'data.csv'
stroke_width = 3    # How many pixels wide is the line representing a single page?
diagram_height = 120
total_pages = 287   # For this particular edition of The Road, ISBN 978-0-307-38789-9
transparent_color = "#010101"   # Should be a color that will never occur during processing; later, we'll make this color transparent in a graphics editor

raw_data = [].copy()

# Expected data format is a .csv file containing [page number], [color]. [color] is an HTML hex color: pound sign followed by six hex digits: #RRGGBB
try:
    with open(data_file_name, newline='') as f:
        reader = csv.reader(f, dialect='unix')
        for row in reader:
            raw_data.append(row)
except OSError:
    print("Can't read the file %s. Fatal error. Giving up." % data_file_name)
    sys.exit(2)

# OK, convert first field from text back to numbers again. Sigh. Stupid CSV.
# "In fact, the Microsoft version of CSV is a textbook example of how *not* to design a textual file format."
#    --Eric S. Raymond, /The Art of Unix Programming/, http://www.catb.org/esr/writings/taoup/html/ch05s02.html

numeric_data = [].copy()
for the_row in raw_data:
    try:
        numeric_data.append([int(the_row[0]), the_row[1]])
    except ValueError:
        pprint("Fatal error: can't parse page numbers. The first column of the .csv file MUST contain only INTEGRAL page numbers.")
        sys.exit(2)

# Don't sort the data: we're assuming it's sorted already, i.e. that it occurs in the file in the same order that it occurs in the book

pages_without_colors = list([x for x in range(1, 1 + total_pages) if x not in [row[0] for row in numeric_data]])

pprint(numeric_data)
print(pages_without_colors)

# And create a table of colors on each page of the novel

color_table = collections.defaultdict(lambda: [ transparent_color ])  # empty dictionary with transparent color as default
for the_item in numeric_data:       # iterate over the data table, transforming it into a dictionary mapping page number -> ordered list of colors on that page
    if the_item[0] in color_table:
        color_table[the_item[0]].append(the_item[1])
    else:
        color_table[the_item[0]] = [the_item[1]]

# OK, draw the visualization
turtle.setup(width=stroke_width * total_pages, height=diagram_height)
turtle.setworldcoordinates(0, 0, stroke_width * total_pages, diagram_height)
turtle.hideturtle()
turtle.speed("fastest")
turtle.pensize(stroke_width)
turtle.setheading(270)

for the_page in range(1, 1 + total_pages):
    color_table_this_page = color_table[the_page]
    print("%d\t-->\t%s" % (the_page, color_table_this_page))
    turtle.penup()
    turtle.setpos((the_page - 1) * stroke_width, diagram_height)
    turtle.pendown()
    for the_color in color_table_this_page:
        turtle.pencolor(the_color)
        turtle.forward(diagram_height / len(color_table_this_page))


the_canvas = turtle.getcanvas()
the_canvas.postscript(file='vis1.ps')
