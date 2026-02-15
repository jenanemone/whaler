#! user/bin/env Python3

from collections import Counter

counts = Counter(len(line.split("|")) for line in open('pools_target_cities_feb26/maricopa_master_residential.txt'))
print(counts)
