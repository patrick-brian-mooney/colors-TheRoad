#!/usr/bin/env python3
"""Quick hack to produce a visualization of color usage in McCarthy's novel
The Road. Data included is based on http://is.gd/road_colors; incomplete info
or other errors should be reported as noted on that page.

This script produces one three-pixel-wide bar for color mention in the novel,
regardless of what other colors may be mentioned on that page or how long it's
been since a color was mentioned.

This is, after all, a quick hack, not a producer of a beautiful visualization,
and some of my concerns are documented somewhat in the docstring for the 
vis1.py script. Those apply here, too.

I'd love suggestions on how to do this better. This is a first attempt.

Script by Patrick Mooney; last update was 27 Oct 2015. If you find it useful,
you are welcome to use and adapt this script. It is licensed under the GPL v3
or (at your option) any later version. A copy of this license is in the file
LICENSE.md."""

import turtle
from pprint import pprint
import sys
import csv

data_file_name = 'data.csv'
stroke_width = 3    # How many pixels wide is the line representing a single color mention?
diagram_height = 120
total_pages = 287   # For this particular edition of The Road, ISBN 978-0-307-38789-9

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

pprint(numeric_data)
print("number of entries is %d" % len(numeric_data))

# OK, draw the visualization
turtle.setup(width=stroke_width * len(numeric_data), height=diagram_height)
turtle.setworldcoordinates(0, 0, stroke_width * len(numeric_data), diagram_height)
turtle.hideturtle()
turtle.speed("fastest")
turtle.pensize(stroke_width)
turtle.setheading(270)

for the_color_data in numeric_data:
    turtle.penup()
    current_x, current_y = turtle.position()
    turtle.setpos(current_x + stroke_width, diagram_height)
    turtle.pendown()
    turtle.pencolor(the_color_data[1])
    turtle.forward(diagram_height)

the_canvas = turtle.getcanvas()
the_canvas.postscript(file='vis2.ps')
