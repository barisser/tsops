import random
import pandas as pd

import tsops

def generate_test_intervals():
	start_dt = pd.to_datetime('2021-01-01 10:00:00', utc=True)
	end_dt = pd.to_datetime('2021-01-01 11:00:00', utc=True)
	interval_seconds = 10
	grid = pd.date_range(start_dt, end_dt, freq='{}s'.format(interval_seconds), tz='UTC')
	intervals = pd.DataFrame(grid, columns=['start_dt'])
	intervals['end_dt'] = intervals['start_dt'] + pd.Timedelta("{}s".format(interval_seconds))
	intervals['data'] = pd.Series(intervals.index).apply(lambda x: x**3 % 13)
	return intervals

def test_merge_point_intervals():
	intervals = generate_test_intervals()
	start_dt = pd.to_datetime('2021-01-01 10:00:00', utc=True)
	points_raw = [[start_dt + pd.Timedelta("{}s".format(random.randint(0, 3600))), random.randint(0,1e6)] for _ in range(1000)]
	points = pd.DataFrame(points_raw, columns=['ts', 'data'])

	merged = tsops.merge_into_intervals(intervals, points, 'start_dt', 'end_dt', 'ts', how='outer')
	import pdb;pdb.set_trace()

