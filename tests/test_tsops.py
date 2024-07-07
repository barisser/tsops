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

def test_merge_point_intervals_non_intersecting():
	intervals = generate_test_intervals()
	start_dt = pd.to_datetime('2021-01-01 16:00:00', utc=True)
	points_raw = [[start_dt + pd.Timedelta("{}s".format(random.randint(0, 3600))), random.randint(0,1e6)] for _ in range(1000)]
	points = pd.DataFrame(points_raw, columns=['ts', 'data'])

	merged = tsops.merge_into_intervals(points, intervals, 'start_dt', 'end_dt', 'ts', how='outer')
	
	assert len(merged) == len(points) + len(intervals)
	assert len(merged[merged.ts.isna()]) == len(intervals)
	assert len(merged[merged.start_dt.isna()]) == len(points)
	
def test_merge_point_intervals_intersecting():
	intervals = generate_test_intervals()
	start_dt = pd.to_datetime('2021-01-01 10:00:00', utc=True)
	points_raw = [[start_dt + pd.Timedelta("{}s".format(random.randint(0, 3600))), random.randint(0,1e6)] for _ in range(1000)]
	points = pd.DataFrame(points_raw, columns=['ts', 'data'])

	merged = tsops.merge_into_intervals(points, intervals, 'start_dt', 'end_dt', 'ts', how='left')
	assert len(merged) == len(points)
	assert (merged['ts'] >= merged['start_dt']).all()
	assert (merged['ts'] < merged['end_dt']).all()
	assert (merged['end_dt'] - merged['ts']).max() <= pd.Timedelta('10s')
	assert (merged['ts'] - merged['start_dt']).max() < pd.Timedelta('10s')
	assert (merged['ts'] != merged['end_dt']).all()


def test_merge_point_intervals_non_continuous():
	intervals = generate_test_intervals()
	start_dt = pd.to_datetime('2021-01-01 10:00:00', utc=True)
	points_raw = [[start_dt + pd.Timedelta("{}s".format(random.randint(0, 3600))), random.randint(0,1e6)] for _ in range(1000)]
	points = pd.DataFrame(points_raw, columns=['ts', 'data'])

	intervals = intervals[intervals.start_dt > intervals.iloc[100].start_dt]
	left_merged = tsops.merge_into_intervals(points, intervals, 'start_dt', 'end_dt', 'ts', how='left')
	inner_merged = tsops.merge_into_intervals(points, intervals, 'start_dt', 'end_dt', 'ts', how='inner')
	assert len(left_merged) == 1000
	assert len(inner_merged) < 1000 and len(inner_merged) > 400

	intervals2 = generate_test_intervals()
	d1 = pd.to_datetime('2021-01-01 10:15:00', utc=True)
	d2 = pd.to_datetime('2021-01-01 10:25:00', utc=True)
	intervals2 = intervals2[(intervals2.start_dt < d1) | (intervals2.end_dt > d2)]
	merged = tsops.merge_into_intervals(points, intervals, 'start_dt', 'end_dt', 'ts', how='left')
	assert len(merged) == 1000
