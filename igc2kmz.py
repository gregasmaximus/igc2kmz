#!/usr/bin/python
#
#   igc2kmz.py  IGC to Google Earth converter
#   Copyright (C) 2008  Tom Payne
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import optparse
import sys

import igc2kmz
import igc2kmz.igc
import igc2kmz.kml
import igc2kmz.photo
import igc2kmz.xc


def add_flight(option, opt, value, parser):
    """Add a flight."""
    igc = igc2kmz.igc.IGC(open(value))
    parser.values.flights.append(igc2kmz.Flight(igc.track()))


def set_flight_option(option, opt, value, parser):
    """Set an option on the last flight."""
    flight = parser.values.flights[-1]
    setattr(flight, option.dest, value)


def add_photo(option, opt, value, parser):
    """Add a photo to the last flight."""
    flight = parser.values.flights[-1]
    photo = igc2kmz.photo.Photo(value)
    flight.photos.append(photo)


def set_photo_option(option, opt, value, parser):
    """Set an option on the last photo on the last flight."""
    flight = parser.values.flights[-1]
    photo = flight.photos[-1]
    setattr(photo, option.dest, value)


def set_flight_xc(option, opt, value, parser):
    """Set the XC of the last flight."""
    flight = parser.values.flights[-1]
    xc = igc2kmz.xc.XC(open(value))
    flight.xc = xc


def main(argv):
    parser = optparse.OptionParser(
            usage='Usage: %prog [options]',
            description="IGC to Google Earth converter")
    parser.add_option('-o', '--output', metavar='FILENAME',
            help='set output filename')
    parser.add_option('-z', '--timezone-offset', metavar='HOURS', type='int',
            help='set timezone offset')
    parser.add_option('-r', '--root', metavar='FILENAME',
            action='append', dest='roots',
            help='add root element')
    parser.add_option('--debug',
            action='store_true',
            help='enable pretty KML output')
    group = optparse.OptionGroup(parser, 'Per-flight options')
    group.add_option('-i', '--igc', metavar='FILENAME', type='string',
            action='callback', callback=add_flight,
            help='set flight IGC file')
    group.add_option('-n', '--pilot-name', metavar='STRING', type='string',
            action='callback', callback=set_flight_option,
            help='set pilot name')
    group.add_option('-g', '--glider-type', metavar='STRING', type='string',
            action='callback', callback=set_flight_option,
            help='set glider type')
    group.add_option('-c', '--color', metavar='COLOR', type='string',
            action='callback', callback=set_flight_option,
            help='set track line color')
    group.add_option('-w', '--width', metavar='INTEGER', type='int',
            action='callback', callback=set_flight_option,
            help='set track line width')
    group.add_option('-u', '--url', metavar='URL', type='string',
            action='callback', callback=set_flight_option,
            help='set flight URL')
    group.add_option('-x', '--xc', metavar='FILENAME', type='string',
            action='callback', callback=set_flight_xc,
            help='set flight XC')
    parser.add_option_group(group)
    group = optparse.OptionGroup(parser, 'Per-photo options')
    group.add_option('-p', '--photo', metavar='URL', type='string',
            action='callback', callback=add_photo,
            help='add photo')
    group.add_option('-d', '--description', metavar='STRING', type='string',
            action='callback', callback=set_photo_option,
            help='set photo comment')
    parser.add_option_group(group)
    #
    parser.set_defaults(debug=False)
    parser.set_defaults(flights=[])
    parser.set_defaults(output='igc2kmz.kmz')
    parser.set_defaults(roots=[])
    parser.set_defaults(timezone_offset=0)
    #
    options, args = parser.parse_args(argv)
    if len(options.flights) == 0:
        parser.error('no flights specified')
    if len(args) != 1:
        parser.error('extra arguments on command line: %s' % repr(args[1:]))
    #
    roots = [igc2kmz.kml.Verbatim(open(root).read()) for root in options.roots]
    kmz = igc2kmz.flights2kmz(options.flights,
            roots=roots,
            timezone_offset=options.timezone_offset)
    kmz.write(options.output, debug=options.debug)


if __name__ == '__main__':
    main(sys.argv)
