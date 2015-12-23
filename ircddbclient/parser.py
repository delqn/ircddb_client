import datetime
import re


def cleanup(string):
    """Replace sequences of _ with a single space."""
    x = re.sub(r'[_]+', ' ', string) if string else string
    return None if x == ' ' else x


def when(string):
    """Convert string to a Parse date object."""
    dt = dict(
        year=int(string[:4]),
        month=int(string[4:6]),
        day=int(string[6:8]),
        hour=int(string[8:10]),
        minute=int(string[10:12]),
        second=int(string[12:14]))
    return {
        "__type": "Date",
        "iso": datetime.datetime(**dt).isoformat(),
        }


# example: #317470:20151223192301N0DEC___WW6BAY_B0WW6BAY_G/WW6BAYB000000D___01________
PIECES = (
    ('rowID', r'^(\d*):', int),
    ('when', r':(\d{14})', when),
    ('myCall', r'^\d*:\d{14}(.{8})', cleanup),
    ('rpt1', r'^\d*:.{22}(.{8})', cleanup),
    ('qsoStarted', r'^\d*:.{30}(\d)', lambda x: x == '0'),
    ('rpt2', r'^\d*:.{31}(.{8})', cleanup),
    ('urCall', r'^\d*:.{39}(.{8})', cleanup),
    ('flags', r'^\d*:.{47}(.{6})', cleanup),
    ('myRadio', r'^\d*:.{53}(.{4})', cleanup),
    ('dest', r'^\d*:.{59}(.{8})', cleanup),
    ('txStats', r'^\d*:.{67}(.{20})', cleanup),
    ('key', r'^\d*:\d{14}(.{33})', lambda x: x[:16] + '1' + x[17:]),
)


class Parser(object):
    def parse(self, message):
        _data = {}
        for k, regex, transform in PIECES:
            matches = re.findall(regex, message)
            value = matches[0] if len(matches) else None
            _data[k] = transform(value) if transform else value
        return _data
