#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import csv
import yaml
from colour import Color

MANDATORY_COLS = ['Cycle', 'Channel', 'Layer', 'Marker', 'Cycle Color',
                  'Failed']
MANDATORY_COL_COUNT = len(MANDATORY_COLS)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(1)


def get_color(row, column):
    value = row[column].strip()

    if len(value) == 0:
        return None

    # TODO Does it make sense to have an NA in a group?
    if value.upper() == 'NA':
        return None

    return Color(value)


def get_cycle_color(row):
    value = row['Cycle Color'].strip()

    if len(value) == 0:
        raise ValueError('No color (or NA) for cycle')

    if value.upper() == 'NA':
        return None

    return Color(value)


# TODO Allow cycle names with spaces in?
def get_cycle_name(row):
    value = row['Marker'].strip()

    if row['Failed'].upper() == 'TRUE':
        value += '-failed'

    return value


custom_dumper = yaml.dumper.SafeDumper
custom_dumper.ignore_aliases = lambda self, data: True


def color_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.hex_l[1:],
                                   style='\'')


# Unfortunately there appears to be no way to have more specificity when
# determining which strings are dumped with a certain style, so the Ystr class
# is used to wrap strings that should be dumped in this way
class Ystr(str):
    pass


def Ystr_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='\'')


yaml.add_representer(Color, color_representer, Dumper=custom_dumper)
yaml.add_representer(Ystr, Ystr_representer, Dumper=custom_dumper)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Convert HMS CycIF channel mapping CSV file to YAML.'
    )
    parser.add_argument('infile', help='The CSV file to convert.')
    parser.add_argument('outfile', help='The YAML file to output.')

    args = parser.parse_args()

    with open(args.infile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        # Ensure the fixed columns are present and in the correct order
        if not reader.fieldnames[:MANDATORY_COL_COUNT] == MANDATORY_COLS:
            eprint('First {} column names must be {}.'.format(
                MANDATORY_COL_COUNT,
                MANDATORY_COLS
            ))

        channel_group_names = reader.fieldnames[MANDATORY_COL_COUNT:]

        # Ensure all of the channel groupings have names
        if not all(len(name.strip()) > 0 for name in channel_group_names):
            eprint('All columns must have a name for the channel grouping'
                   'title.')

        # Ensure there are no repeated channel grouping names
        # TODO Also ensure that no groups collide with cycle groupings?
        # Or override? Or skip?
        if len(set(channel_group_names)) != len(channel_group_names):
            eprint('Channel grouping titles must be unique')

        channels = {}
        channel_groups = {}
        for row in reader:
            default_color = get_cycle_color(row)
            channel_id = int(row['Layer'])

            if default_color:
                channels[channel_id] = {
                    'label': Ystr(get_cycle_name(row)),
                    'min': 0,
                    'max': 65536,
                    'color': default_color
                }

                channel_group = channel_groups.setdefault(
                    'Cycle_{}'.format(channel_id), []
                )

                channel_group.append({
                    'channel': 1,
                    'min': 0,
                    'max': 65536,
                    'color': default_color
                })

            for channel_group_name in channel_group_names:
                color = get_color(row, channel_group_name)

                if color:

                    channel_group = channel_groups.setdefault(
                        channel_group_name, []
                    )

                    channel_group.append({
                        'channel': channel_id,
                        'min': 0,
                        'max': 65536,
                        'color': color,
                    })

        data = {
            'channels': channels,
            'channelGroups': channel_groups
        }

        with open(args.outfile, 'wb') as outfile:
            yaml.dump(data, outfile, default_flow_style=False,
                      Dumper=custom_dumper)
