#!/usr/bin/env python

def stringify(object_):
    """Apply str() to all objects passed to it, except None, which is converted
    to an empty string."""
    if object_ is None:
        return ""
    return str(object_)

class Column(object):
    """A column in the table."""
    DEFAULT_PAD = str.ljust

    def __init__(self, items, heading=None, pad=None):
        self.items = [stringify(item) for item in items]
        self.heading = stringify(heading)
        if pad is None:
            self.pad = Column.DEFAULT_PAD
        else:
            self.pad = pad

    def __iter__(self):
        """Yields each entry in the column in order."""
        items = self.items
        if self.heading is not None:
            items = [self.heading] + items
        return iter(items)

    def pad_items(self, width=None):
        """Pad all items in the column to the given width."""
        if width is None:
            width = self.width()
        self.heading = self.pad(self.heading, width)
        for i, item in enumerate(self.items):
            self.items[i] = self.pad(item, width)

    def width(self):
        """Find the widest item in the column."""
        return max(len(item) for item in [self.heading] + self.items)

class Table(object):
    """Format a list of rows into columns.  The columns are fitted to the width
    of the largest item.

    Fields:
        * label - The title of the table.
        * headings - A list of the headings for each column.
        * row_sperator, column_seperator
        * top_border, bottom_border, left_border, right_border
        * body_top - The divider between the table head and table body
        * pads - A list of functions to pad the cells.  Default is str.ljust.
    """

    def __init__(self, rows, label=None, headings=None, column_seperator=" ",
                 row_seperator=None, top_border=None, bottom_border=None,
                 left_border="", right_border="", body_top=None, pads=None):
        self.rows = rows
        self.label = label
        self.headings = headings
        self.column_seperator = column_seperator
        self.row_seperator = row_seperator
        self.top_border = top_border
        self.bottom_border = bottom_border
        self.body_top = body_top
        self.left_border = left_border
        self.right_border = right_border
        self.pads = pads
        self.columns = Table.columns(rows, headings, pads)
        for column in self.columns:
            column.pad_items()

    def __iter__(self):
        """Yield each line of the table one at a time."""
        for row in self.iheader():
            yield row
        for row in self.ibody():
            yield row
        if self.bottom_border is not None:
            yield self.bottom_border * self.width()

    @staticmethod
    def columns(rows, headings=None, pads=None):
        """Construct a list of columns from the given rows and headings."""
        rows = list(rows)
        try:
            num_columns = len(rows[0])
        except IndexError:
            num_columns = 0
        if headings is None:
            headings = [None] * num_columns
        if pads is None:
            pads = [None] * num_columns
        columns = [[] for i in xrange(num_columns)]
        for row in rows:
            for item, column in zip(row, columns):
                column.append(item)
        return [Column(column, heading, pad) for heading, column, pad in
                zip(headings, columns, pads)]

    def format_row(self, items):
        """Format the given row for presentation in the table."""
        result = self.column_seperator.join(items)
        return self.left_border + result + self.right_border

    def ibody(self):
        """Yield each line of the table body one at a time."""
        rows = zip(*[column.items for column in self.columns])
        for i, row in enumerate(rows):
            yield self.format_row(row)
            if self.row_seperator is not None and i + 1 < len(rows):
                yield self.row_seperator * self.width()

    def iheader(self):
        """Yield each line of the table head one at a time."""
        if self.label is not None:
            yield self.label.center(self.width())
        if self.top_border is not None:
            yield self.top_border * self.width()
        if self.headings is not None:
            yield self.format_row(column.heading for column in self.columns)
        if self.body_top is not None:
            yield self.body_top * self.width()

    def width(self):
        """The width, in characters, of the table."""
        width = sum(column.width() for column in self.columns)
        width += (len(self.columns) - 1) * len(self.column_seperator)
        return width + len(self.left_border) + len(self.right_border)
