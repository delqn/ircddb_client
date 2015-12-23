RAW_RESPONSE = """322941:20151223215516********PY2KPE_B2
322942:20151223215527LZ1MVR__LZ0DAB_B0LZ0DAB_GCQCQCQ__000000001600DCS023_BLZ1MVR_-_Koko_0016__
322943:20151223215529VK4BJT__VK4RDW_B0VK4RDW_GCQCQCQ__000000510000DCS028_BJohn,_Gold_Coast_AUS
322944:20151223215529VK4BJT__VK4RDW_B1VK4RDW_GCQCQCQ__000000510000________0.6s_S:0%_E:0.0%____
322945:20151223215532LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__000000001600________5.8s_S:0%_E:0.0%____
"""

RAW_RESPONSE2 = """322945:20151223215532LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__000000001600_____""" + \
                """___5.8s_S:0%_E:0.0%____
322946:20151223215534********N5DSD__C0N5DSD__GCQCQCQ__000000____00________
322947:20151223215534********N5DSD__C1N5DSD__GCQCQCQ__000000____00________0.1s_S:0%_E:0.0%____
322948:20151223215540WB4IZC__W4LET__B0W4LET__GCQCQCQ__000000____00________Steve_-_Horn_Lake,_M
322949:20151223215541WB4IZC__W4LET__B1W4LET__GCQCQCQ__000000____00________1.3s_S:0%_E:0.0%____
"""

PARSED_MESSAGES = [
    {'rpt2': 'LZ0DAB G',
     'key': 'LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__',
     'rpt1': 'LZ0DAB B',
     'qsoStarted': True, 'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:27',
              '__type': 'Date'}, 'dest': 'DCS023 B',
     'flags': '000000',
     'rowID': 322942, 'myRadio': '0016',
     'txStats': 'LZ1MVR - Koko 0016 ',
     'myCall': 'LZ1MVR '},

    {'rpt2': 'VK4RDW G',
     'key': 'VK4BJT__VK4RDW_B1VK4RDW_GCQCQCQ__',
     'rpt1': 'VK4RDW B',
     'qsoStarted': True, 'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:29',
              '__type': 'Date'}, 'dest': 'DCS028 B',
     'flags': '000000',
     'rowID': 322943, 'myRadio': '5100',
     'txStats': 'John, Gold Coast AUS',
     'myCall': 'VK4BJT '},

    {'rpt2': 'VK4RDW G',
     'key': 'VK4BJT__VK4RDW_B1VK4RDW_GCQCQCQ__',
     'rpt1': 'VK4RDW B',
     'qsoStarted': False, 'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:29',
              '__type': 'Date'}, 'dest': None, 'flags': '000000',
     'rowID': 322944, 'myRadio': '5100',
     'txStats': '0.6s S:0% E:0.0% ',
     'myCall': 'VK4BJT '},

    {'rpt2': 'LZ0DAB G',
     'key': 'LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__',
     'rpt1': 'LZ0DAB B',
     'qsoStarted': False, 'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:32',
              '__type': 'Date'}, 'dest': None, 'flags': '000000',
     'rowID': 322945, 'myRadio': '0016',
     'txStats': '5.8s S:0% E:0.0% ',
     'myCall': 'LZ1MVR '},
]

PARSED_MESSAGES2 = [
    {'rpt2': 'VK4RDW G',
     'rpt1': 'VK4RDW B',
     'dest': 'DCS028 B',
     'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:29',
              '__type': 'Date'}, 'flags': '000000',
     'key': 'VK4BJT__VK4RDW_B1VK4RDW_GCQCQCQ__',
     'myRadio': '5100',
     'txStats': '0.6s S:0% E:0.0% ',
     'myCall': 'VK4BJT '},
    {'rpt2': 'LZ0DAB G',
     'rpt1': 'LZ0DAB B',
     'dest': 'DCS023 B',
     'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:32',
              '__type': 'Date'}, 'flags': '000000',
     'key': 'LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__',
     'myRadio': '0016',
     'txStats': '5.8s S:0% E:0.0% ',
     'myCall': 'LZ1MVR '},
]


COMBINED_MESSAGES = [
    {'rpt2': 'VK4RDW G',
     'rpt1': 'VK4RDW B',
     'dest': 'DCS028 B',
     'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:29',
              '__type': 'Date'}, 'flags': '000000',
     'key': 'VK4BJT__VK4RDW_B1VK4RDW_GCQCQCQ__',
     'myRadio': '5100',
     'txStats': '0.6s S:0% E:0.0% ',
     'myCall': 'VK4BJT '},

    {'rpt2': 'LZ0DAB G',
     'rpt1': 'LZ0DAB B',
     'dest': 'DCS023 B',
     'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:32',
              '__type': 'Date'}, 'flags': '000000',
     'key': 'LZ1MVR__LZ0DAB_B1LZ0DAB_GCQCQCQ__',
     'myRadio': '0016',
     'txStats': '5.8s S:0% E:0.0% ',
     'myCall': 'LZ1MVR '},
]

COMBINED_MESSAGES2 = [
    {'rpt2': 'W4LET G',
     'rpt1': 'W4LET B',
     'dest': None, 'urCall': 'CQCQCQ ',
     'when': {'iso': '2015-12-23T21:55:41',
              '__type': 'Date'}, 'flags': '000000',
     'key': 'WB4IZC__W4LET__B1W4LET__GCQCQCQ__',
     'myRadio': None, 'txStats': '1.3s S:0% E:0.0% ',
     'myCall': 'WB4IZC '},
]
