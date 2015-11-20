#!/usr/bin/env python

from argparse import ArgumentParser
from omero_basics import OMEROConnectionManager
from omero_basics import well_from_row_col

# Configure argument parsing
parser = ArgumentParser(
    description='Get image ID for wellsample ID or well ID AND run ID'
)
parser.add_argument('wellsample', type=int)
args = parser.parse_args()

# Create an OMERO Connection with our basic connection manager
conn_manager = OMEROConnectionManager()

# Define a query to get the list of image ID in a screen complete with
# screen name, plate ID and well row/column. Only queries the first field.
if args.wellsample != None:

    q = """
        SELECT image.id
        FROM WellSample ws
        WHERE ws.id=%i
        """ % args.wellsample

else:
    q = """
        SELECT image.id
        FROM 
        """

# Run the query
rows = conn_manager.hql_query(q)

# Replace Row+Column IDs with a more meaningful Well designation
# E.g. Row 3, Column 2: D3
# Calculate the Well and assign it to the position that row was in
# row[3] = well_from_row_col(row[3], row[4])

header = ["WellSample ID"]

# Print results
print ', '.join(header)

if len(rows) != 1:
    print 'Error: No Image ID associated with this Well Sample'
    exit(1)

    print '%s' % rows[0][0]
