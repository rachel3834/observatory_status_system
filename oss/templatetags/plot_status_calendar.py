from plotly import offline
from plotly import graph_objs as go
from datetime import datetime, timedelta
import numpy as np

@register.inclusion_tag('oss/partials/status_plot.html', takes_context=True)
def status_calendar(context):
    """
    Produces a calendar-like heatmap of the status of a facility over time, based on
    plotly community example by user Blaceus
    """
    status_map = {'Open': 0.0,
                  'Closed-weather': 0.1,
                  'Closed-unsafe-to-observe': 0.2,
                  'Closed-daytime': 0.3,
                  'Offline': 0.4,
                  'Unknown': 0.5}
    colorscale: [
    ['0.0', 'rgb(50, 168, 82)'],    # Open
    ['0.1', 'rgb(26, 80, 196)'],  # Closed-weather
    ['0.2', 'rgb(224, 132, 40)'], # Closed-unsafe
    ['0.3', 'rgb(218, 224, 40)'], # Closed-daytime
    ['0.4', 'rgb(83, 7, 105)'],     # Offline
    ['0.5', 'rgb(168, 160, 160)'], # Unrecognised status
    ]

    today = datetime.now()
    dt = timedelta(days=182.625)

	d1 = today - dt
    start_date = datetime(d1.year, d1.month, d1.day)
    d1 = today + dt
	end_date = datetime(d1.year, d1.month, d1.day)

	dt = end_date - start_date

	dates_in_year = np.array([start_date + datetime.timedelta(x) for x in range(dt.days+1)])
	weekdays = [i.weekday() for i in dates_in_year]
	weeknumber_of_dates = [int(i.strftime("%V")) for i in dates_in_year]

	status_data = [0.5]*len(dates_in_year)
    # context['status_data'] needs to be a list of entries for each date of the year
    for d, stat in context['status_data']:
        d1 = datetime.strptime(d, "%Y-%m-%d")
        if d1 >= start_date:
            idx = np.where(dates_in_year = d1)
            if len(idx) > 0:
                status_data[idx] = status_map[stat]

	text = [str(i) for i in dates_in_year]

	data = [
		go.Heatmap(
			x = weekdays_in_year,
			y = weeknumber_of_dates,
			z = status_data,
			text=text,
			hoverinfo="text",
			xgap=3,
			ygap=3,
			showscale=False,
            colorscale=colorscale,
		)
	]
	layout = go.Layout(
		title='Status of Facility',
		height=1000,
		xaxis=dict(
			showline=True,
			tickmode="array",
			ticktext=["M", "T", "W", "T", "F", "S", "S"],
			tickvals=[0,1,2,3,4,5,6],
			title=""
		),
		yaxis=dict(
			showline=True,
			title=""
		),
		plot_bgcolor=('rgb(0,0,0)') #making grid appear black
	)

	fig = go.Figure(data=data, layout=layout)
	return fig
