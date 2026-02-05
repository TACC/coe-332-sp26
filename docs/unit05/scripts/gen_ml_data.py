#!/usr/bin/env python3
import json
import random
import sys
import names

NUM = 10
CLASSES = ['CI1', 'CR2-an', 'CV3', 'EH4', 'H4', 'H5', 'H6', 'L5', 'L6', 'LL3-6', 'LL5']

def generate_meteors(num:int):
    """
    Generate and return randomly generated meteors in list of dicts format
    """
    meteors = []
    for i in range(num):
        meteor = {}
        rand_lat = '{:.4f}'.format(random.uniform(-90.0000, 90.0000))
        rand_lon = '{:.4f}'.format(random.uniform(-90.0000, 90.0000))
        meteor['name'] = names.get_first_name()
        meteor['id'] = str(10000 + 1 + i)
        meteor['recclass'] = random.choice(CLASSES)
        meteor['mass (g)'] = str(random.randrange(1, 10000))
        meteor['reclat'] = rand_lat
        meteor['reclong'] = rand_lon
        meteor['GeoLocation'] = f'({rand_lat}, {rand_lon})'
        meteors.append(meteor)
    return meteors

def main():
    data = {'meteorite_landings': generate_meteors(NUM)}
    with open(sys.argv[1], 'w') as o:
        json.dump(data, o, indent=2)
        print(f'Data written to {sys.argv[1]}!')

if __name__ == '__main__':
    main()