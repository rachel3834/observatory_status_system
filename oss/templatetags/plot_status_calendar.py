from plotly import offline
from plotly import graph_objs as go
from datetime import datetime, timedelta
import numpy as np
from django import template
from django.conf import settings
import pytz

register = template.Library()

@register.inclusion_tag('oss/partials/status_plot.html')
def status_calendar(tel_status):
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
    rev_status_map = {}
    for key, value in status_map.items():
        rev_status_map[value] = key

    colorscale = [
    [0.0, 'rgb(50, 168, 82)'],    # Open
    [0.09, 'rgb(50, 168, 82)'],    # Open
    [0.1, 'rgb(26, 80, 196)'],  # Closed-weather
    [0.19, 'rgb(26, 80, 196)'],  # Closed-weather
    [0.2, 'rgb(224, 132, 40)'], # Closed-unsafe
    [0.29, 'rgb(224, 132, 40)'], # Closed-unsafe
    [0.3, 'rgb(218, 224, 40)'], # Closed-daytime
    [0.39, 'rgb(218, 224, 40)'], # Closed-daytime
    [0.4, 'rgb(83, 7, 105)'],     # Offline
    [0.49, 'rgb(83, 7, 105)'],     # Offline
    [0.5, 'rgb(168, 160, 160)'], # Unrecognised status
    [1.0, 'rgb(168, 160, 160)'], # Unrecognised status
    ]

    today = datetime.now()
    today = today.replace(tzinfo=pytz.UTC)

    dt = timedelta(days=182.625)

    d1 = today - dt
    start_date = datetime(d1.year, d1.month, d1.day)
    start_date = start_date.replace(tzinfo=pytz.UTC)
    d1 = today + dt
    end_date = datetime(d1.year, d1.month, d1.day)
    end_date = end_date.replace(tzinfo=pytz.UTC)

    date_range = end_date - start_date
    dates_in_year = np.array([start_date + timedelta(days=x) for x in range(date_range.days+1)])

    weeks = []
    week_ticks = []
    week_labels = []
    weekdays = []
    year_rollover = False
    for i,d in enumerate(dates_in_year):
        weekdays.append(d.weekday())
        if not year_rollover:
            week_number = int(d.strftime("%W"))
            month_number = int(d.strftime("%m"))
        else:
            week_number = int(d.strftime("%W"))+51
            month_number = int(d.strftime("%m"))+12
        weeks.append(week_number)
        if d.weekday() == 0:
            if week_number not in week_ticks:
                week_ticks.append(week_number)
                week_labels.append(d.strftime("%Y %B %d"))

        if d == datetime(d.year, 12, 31, tzinfo=pytz.UTC):
            year_rollover = True
        #print(i, d, weeks[-1], d.strftime("%W"), weekdays[-1], months[-1], months_text[-1], year_rollover)

    # Initialize whole mape to 'Unknown' status
    status_data = [0.5]*len(dates_in_year)

    # context['status_data'] needs to be a list of entries for each date of the year
    for d, stat in tel_status.timeline:
        day = datetime(d.year, d.month, d.day, tzinfo=pytz.UTC)
        if day >= start_date:
            idx = np.where(dates_in_year == day)[0]
            if len(idx) > 0:
                status_data[idx[0]] = status_map[stat]

    entry_labels = []
    for i,d in enumerate(dates_in_year):
        entry_labels.append(str(d)+': '+rev_status_map[status_data[i]])
        #print(i, d, entry_labels[-1])

    data = [
        go.Heatmap(
            x = weeks,
            y = weekdays,
            z = status_data,
            text=entry_labels,
            hoverinfo="text",
            xgap=3,
            ygap=3,
            showscale=False,
            colorscale=colorscale,
            )
        ]
    layout = go.Layout(
        title='Telescope Status Timeline',
        #height=1000,

        xaxis=dict(
            showline=True,
            title="Week starting date",
            tickmode="array",
            ticktext=week_labels,
            tickvals=week_ticks,
        ),
        yaxis=dict(
            showline=True,
            tickmode="array",
            ticktext=["M", "T", "W", "T", "F", "S", "S"],
            tickvals=[0,1,2,3,4,5,6],
            title="Day of week"
        ),
        plot_bgcolor=('rgb(255,255,255)')
    )

    fig = offline.plot(go.Figure(data=data, layout=layout), output_type='div')

    return {'figure': fig}
