import os
import logging
import argparse
import collections
from pprint import pformat
import json
from operator import itemgetter
from functools import partial
from geopy.distance import vincenty
import requests

API_URL = 'https://opensky-network.org/api/states/all'
DEFAULT_TIMEOUT = 15.0
PARIS = (48.85, 2.35) # Coordinates of Paris
DEFAULT_RANGE = 450.0 # Default max distance in km

def search_missing(callsign, prev_states, key=None):
    '''If attribute "k" is missing, search non-empty values in previous records.'''
    logging.info(
        '%s: "%s" field is missing. Searching in previous records',
        callsign, key
    )
    try:
        return next(it for it in prev_states if it[key] is not None)
    except StopIteration as ex:
        logging.warn('%s: %s not found', callsign, key)

def iter_states(data, distance):
    '''
    Craft states iterator.

    Arguments:
    data     : list of states returned by the API
    distance : function for calculating distance from center

    Yields:
        dictionary with latest state data per craft
    '''
    # Skip rows with empty callsigns.
    # If timestamp is missing, set it to zero.
    all_states = [
        dict(callsign=s[1].strip(), ts=s[3] if s[3] else 0, lat=s[6], lon=s[5])
        for s in data if s[1].strip() ]
    logging.info('Got %d states', len(all_states))

    # Make sure the report contains only the latest records per craft
    craft_state = {}
    for st in all_states:
        craft_state.setdefault(st['callsign'], []).append(st)
    logging.info('Crafts total: %d', len(craft_state))

    for k, v in craft_state.items():
        #logging.debug('%s states: %s', k, pformat(v))
        s = sorted(v, key=itemgetter('ts'), reverse=True)
        latest = s[0]

        # If the latest state lacks any or both of geo-coordinates,
        # search them in previous states.
        for fld in ('lat', 'lon'):
            if latest[fld] is None:
                latest[fld] = search_missing(latest['callsign'], s[1:], fld)

        if latest['lat'] and latest['lon']:
            latest['distance'] = distance((latest['lat'], latest['lon'])).kilometers
            yield latest
        else:
            logging.warn('Could not find position for callsign %s', latest['callsign'])



def search(data, lat=None, lon=None, arange=None):
    '''
    Search planes in given range.

    data  : list of states returned by the API
    lat   : geographical latitude of central point, degrees
    lon   : geographical longitude of central point, degrees
    range : radius, i.e. maximal distance, km
    '''
    distance = partial(vincenty, (lat, lon), ellipsoid='WGS-84')
    return [ s for s in iter_states(data, distance) if s['distance'] <= arange ]


def make_request(url=API_URL):
    '''
    Make GET request. Return requests.response object.
    Raise exception on a network error, bad status code or empty content.
    '''
    logging.debug('Requesting %s...', url)
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    logging.info('%s: %s - %s', resp.url, resp.status_code, resp.reason)
    resp.raise_for_status()
    assert hasattr(resp, 'json'), 'Empty content!'
    return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Search planes in given range (450km of Paris by default)')
    parser.add_argument(
        '--lat',
        type=float, default=PARIS[0], help='geographic latitude, deg., negative southwards')
    parser.add_argument(
        '--lon',
        type=float, default=PARIS[1], help='geographic longitude, deg., negative westwards')
    parser.add_argument(
        '--range',
        type=float, default=DEFAULT_RANGE, help='range, km')
    args = parser.parse_args()

    # Set debug level
    debug_var = int(os.environ.get('DEBUG_OPENSKY', '0'))
    level = logging.DEBUG if debug_var > 1 \
                          else logging.INFO if debug_var == 1 \
                          else logging.WARNING
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s',)

    try:
        data = make_request().json().get('states', [])
        res = search(data, args.lat, args.lon, args.range)
        print(json.dumps(res, indent=4, sort_keys=True, ensure_ascii=False))
    except KeyboardInterrupt as ex:
        logging.warn('Interrupted by user')
    except Exception as ex:
        logging.error(ex, exc_info=level>1)
