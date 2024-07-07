import pandas as pd



def merge_into_intervals(point_df, intervals_df,
		interval_start_col, interval_end_col, point_col,
		how='left', **kwargs):
	starts1 = pd.DataFrame(intervals_df[interval_start_col])
	starts1['source'] = 'interval'
	starts1['src_index'] = starts1.index
	starts1['start_index'] = starts1.index
	starts1 = starts1.rename(columns={interval_start_col: 'starts'})
	starts2 = pd.DataFrame(point_df[point_col])
	starts2['source'] = 'points'
	starts2 = starts2.rename(columns={point_col: 'starts'})
	starts2['src_index'] = starts2.index
	starts = pd.concat([starts1, starts2]).sort_values(['starts', 'source']).reset_index()
	starts['start_index'] = starts['start_index'].ffill()

	ends1 = pd.DataFrame(intervals_df[interval_end_col])
	ends1['source'] = 'interval'
	ends1['src_index'] = ends1.index
	ends1['end_index'] = ends1.index
	ends1 = ends1.rename(columns={interval_end_col: 'ends'})
	ends2 = starts2.rename(columns={'starts': 'ends'})
	ends = pd.concat([ends1, ends2]).sort_values(['ends', 'source'])[::-1]
	ends['end_index'] = ends['end_index'].ffill()

	sindex = starts[starts.source=='points'][['src_index','start_index']]
	eindex = ends[ends.source=='points'][['src_index','end_index']]

	ind = sindex.merge(eindex, on='src_index', how=how)
	ind['match_index'] = (ind['start_index'] + ind['end_index']) / 2 # hack

	df = ind.merge(point_df, left_on='src_index', right_index=True)

	check = (ind['end_index'] - ind['start_index']).sum()
	if check != 0:
		raise Exception("Something went wrong in merge")
	df = df.merge(intervals_df, left_on='match_index', right_index=True, how=how, **kwargs)
	df.drop(['src_index', 'match_index', 'start_index', 'end_index'], inplace=True, axis=1)
	return df

