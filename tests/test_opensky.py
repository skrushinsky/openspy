import sys
from os.path import dirname
import nose
from nose.tools import ok_, eq_, assert_dict_equal
ROOTDIR = dirname(dirname(dirname(__file__)))
sys.path.append(ROOTDIR)
import opensky

data = {
    'states': [
        ['c04049', '', 'Canada', 1507203246, 1507203249, -81.126, 37.774, 10980.42, False, 245.93, 186.49, 0.33, None, 10972.8, None, False, 0],
        ['4240eb', 'UTA716  ', 'United Kingdom', 1507202967, 1507202981, 37.4429, 55.6265, 609.6, True, 92.52, 281.87, -3.25, None, None, '4325', False, 0],
        ['aa8c39', 'UAL534  ', 'United States', 1507203250, 1507203250, -118.0869, 33.8656, 1760.22, False, 111.31, 343.07, -5.2, None, 1752.6, '2643', False, 0],
        ['7800ed', 'CES5124 ', 'China', 1507203250, 1507203250, 116.8199, 40.2763, 3459.48, False, 181.88, 84.64, 11.7, None, 3566.16, '5632', False, 0],
        ['7801ed', 'CES5123 ', 'Austria', 1507203250, 1507203250, None, 40.2763, 3459.48, False, 181.88, 84.64, 11.7, None, 3566.16, '5632', False, 0],
    ],
    'time': 1507203250
}

def test_request_status():
    '''Make sure API is alive'''
    try:
        # the function throws exception on bad status codes, timeouts etc.,
        # so, there's no need to check explicitly respoonse code.
        opensky.make_request()
    except Exception as ex:
        ok_(False, 'Got exception: {}'.format(ex) )
    else:
        ok_(True)

def test_request_content():
    '''Make sure API returns JSON'''
    try:
        resp = opensky.make_request()
        data = resp.json()
        ok_(data is not None, 'Expecting JSON data')
    except Exception as ex:
        ok_(False, 'Got exception: {}'.format(ex) )

def test_outofrange():
    got = opensky.search(data['states'], 55.0, 38.0, 0.1)
    eq_(len(got), 0, 'Expected no results')

def test_count():
    got = opensky.search(data['states'], 55.0, 38.0, 100.0)
    eq_(len(got), 1, 'Expected exactly one result')

def test_content():
    got = opensky.search(data['states'], 55.0, 38.0, 100.0)
    exp = {
        'callsign': 'UTA716',
        'ts': 1507202967,
        'lat': 55.6265,
        'lon': 37.4429,
        'distance': 78.20419258063157}
    assert_dict_equal(exp, got[0])

def test_missing_callsign():
    got = opensky.search(data['states'], 37.774, -81.126, 100.0)
    eq_(len(got), 0, 'Expected no results')

def test_missing_geocoords():
    got = opensky.search(data['states'], 40.2763, 0, 10.0)
    eq_(len(got), 0, 'Expected no results')




if __name__ == '__main__':
    nose.runmodule(argv=['-d', '-s', '--verbose'])
