import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

# importing modules
import pandas as pd
import plotly.express as px
import datetime

# Loading dataset from an url
belgium = ["antwerp", "brussels", "charleroi", "ghent", "kortrijk", "leuven", "liege", "mons", "namur"]

belgium_df = pd.DataFrame()

for e in belgium:
    df = pd.read_csv("static/csv/tomtom/BEL_" + e + ".csv")
    df['city'] = e
    df['Time'] = pd.to_datetime(df['Time'])
    df.index = df['Time']
    df = df.between_time('07:00', '09:00')
    df = df[df.index.dayofweek < 5]
    df = df[df.Time.dt.date != datetime.date(2020, 5, 1)]
    df = df[df.Time.dt.date > datetime.date(2020, 4, 14)]
    df = df.groupby([df.city, df.Time.dt.date]).agg(['mean'])
    df.columns = df.columns.droplevel(1)
    belgium_df = belgium_df.append(df, ignore_index=False)  # Add df one by one



@register_plot_for_embedding("tomtom_traffic_working_days")
def plot_tomtom_be_working_days():
    """
    tomtom traffic working days
    """
    # Plotting a Map to show real-time traffic around the world
    # fig = px.bar(bel_bru, y='LiveTraffic', x='Time')
    fig = px.line(belgium_df, y='LiveTraffic', x=belgium_df.index.get_level_values(1),
                  color=belgium_df.index.get_level_values(0))

    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide',
                      xaxis_title="TomTom Traffic Index",
                      yaxis_title="Day",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

