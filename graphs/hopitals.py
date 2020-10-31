import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')



def df_hospi_death():
    df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')
    idx = pd.date_range(df_hospi.DATE.min(), df_hospi.DATE.max())
    df_hospi = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum','TOTAL_IN_ICU': 'sum','NEW_IN': 'sum'})
    df_hospi.index = pd.DatetimeIndex(df_hospi.index)
    df_hospi = df_hospi.reindex(idx, fill_value=0)

    df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)
    idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
    df_mortality = df_mortality.groupby(['DATE']).agg({'DEATHS': 'sum'})
    df_mortality.index = pd.DatetimeIndex(df_mortality.index)
    df_mortality = df_mortality.reindex(idx, fill_value=0)

    df = df_mortality.merge(df_hospi, how='left', left_index=True, right_index=True)

    df = df[df.index >= '2020-03-15']
    return df




import numpy as np

def moving_average(a, n=1) :
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n-1] = ret[:n-1]/range(1,n)
    ret[n-1:] = ret[n - 1:] / n
    return ret

df = df_hospi_death()

@register_plot_for_embedding("bar_hospitalization")
def bar_hospitalization():
    """
    bar plot hospitalization
    """
    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum','TOTAL_IN_ICU': 'sum'})

    newin_bar = go.Bar(x=df.index, y=df.NEW_IN, name=gettext('#New Hospitalized'))
    newout_bar = go.Bar(x=df.index, y=df.NEW_OUT, name=gettext('#New Discharged'))
    totin_bar = go.Bar(x=df.index, y=df.TOTAL_IN, name=gettext('#Total Hospitalized'))
    icu_bar = go.Bar(x=df.index, y=df.TOTAL_IN_ICU, name=gettext('#Total ICU'))
    fig_hospi = go.Figure(data=[newin_bar, newout_bar, totin_bar,icu_bar], layout=go.Layout(barmode='group'), )
    fig_hospi.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                            title=gettext("Hospitalizations"))

    fig_hospi.update_layout(xaxis_title=gettext('Day'),
                            yaxis_title=gettext('Number of / Day'))

    return fig_hospi


@register_plot_for_embedding("hospi_waves")
def hospi_waves():
    """
    bar plot hospitalization
    """

    df = df_hospi.groupby(['DATE']).agg(
        {'TOTAL_IN': 'sum', 'TOTAL_IN_ECMO': 'sum', 'TOTAL_IN_RESP': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum',
         'TOTAL_IN_ICU': 'sum'})

    startw2 = '2020-10-07'
    dates_w1 = df.index[:40].values.tolist()
    dates_w2 = df.index[df.index >= startw2].values.tolist()

    eventsw1 = {'2020-03-17': 'lockdown'}
    eventsw2 = {'2020-10-18': 'couvre-feu 24h'}

    def addlines(fig, row, col, ymax, events, dates, color, group):
        show = True
        for date, descr in events.items():
            i = dates.index(date)

            fig.add_trace(go.Scatter(x=[i, i], y=[0, ymax], line={'color': color, 'width': 1, 'dash': 'dashdot'},
                                     name='Horizontal Line', legendgroup=group, showlegend=False), row=row, col=col)
            fig.add_trace(go.Scatter(x=[i], y=[ymax * 1.1], text=[descr], mode="text", name="wave3", legendgroup=group,
                                     showlegend=False), row=row, col=col)
            show = False

    xvals = list(range(0, min(len(dates_w1), len(dates_w2)), 2))
    xlabels = [dates_w1[v][-5:] + "|" + dates_w2[v][-5:] for v in xvals]

    fig = make_subplots(rows=5, cols=1, subplot_titles=('Total', 'ICU', 'New In', 'ECMO', 'RESP'), shared_xaxes=True,
                        vertical_spacing=0.02, )

    def add(column, row, show=False):
        y1 = df[column][:40]
        y2 = df[column][df.index >= startw2]
        wave1 = go.Bar(y=y1, name="wave1", legendgroup="wave1", showlegend=show, marker_color="red")
        wave2 = go.Bar(y=y2, name="wave2", legendgroup="wave2", showlegend=show, marker_color="blue")
        fig.add_trace(wave1, row, 1)
        fig.add_trace(wave2, row, 1)
        # fig.update_layout(xaxis_title=gettext('Day'),yaxis_title=gettext('Number of / Day'),row=row,col=1)
        fig.update_xaxes(tickmode='array', tickvals=xvals, ticktext=xlabels, row=row, col=1)
        addlines(fig, row, 1, max(max(y1), max(y2)) * 1, eventsw1, dates_w1, "red", 'wave1')
        addlines(fig, row, 1, max(max(y1), max(y2)) * 1, eventsw2, dates_w2, "blue", 'wave2')

    add('TOTAL_IN', 1, True)
    add('TOTAL_IN_ICU', 2)
    add('NEW_IN', 3)
    add('TOTAL_IN_ECMO', 4)
    add('TOTAL_IN_RESP', 5)

    fig.update_layout(template="plotly_white", height=1600, margin=dict(l=0, r=0, t=40, b=0),
                      title=gettext("Hospitalizations First Wave vs Second Wave"))

    return fig


@register_plot_for_embedding("exp_fit_hospi")
def exp_fit_hospi():
    x = df.index
    y = df.TOTAL_IN.values #moving_average(df.TOTAL_IN.values, 7)
    lastx = x[-15:]
    lasty = y[-15:]

    import numpy as np
    from scipy.optimize import curve_fit

    def exponenial_func(x, a, b, c):
        return a * np.exp(-b * x) + c

    import math

    lastxx = np.arange(0, len(lasty), 1)

    popt, pcov = curve_fit(exponenial_func, lastxx, lasty, p0=(1, 1e-6, 1))

    #doubling = math.log(0.5) / popt[1]
    doubling = -(1 / popt[1]) * math.log((2 * popt[0] + popt[2]) / popt[0])

    lastyy = exponenial_func(lastxx, *popt)

    fig = px.line(x=x, y=y, log_y=True, labels={'x': 'date', 'y': 'total hospitals (log scale)'},
                  title="Hospitalizations log scale and doubling period computation",height=600)

    # Creating the dataset, and generating the plot
    #fitexp = go.Scatter(
    #    x=lastx,
    #    y=lastyy,
    #    mode='markers',
    #    name='exponential fit'
    #)

    #fig.add_trace(fitexp)

    #fig.add_trace(go.Scatter(
    #    x=[lastx[0]],
    #    y=[lastyy[0]],
    #    mode="markers+text",
    #    name="doubling period",
    #    text=["doubling period:" + str(round(doubling, 1)) + " days"],
    #    textposition="bottom center"
    #))

    fig.update_layout(template="plotly_white")

    return fig

@register_plot_for_embedding("bar_hospitalization_tot")
def bar_hospitalization_tot():
    """
    bar plot hospitalization
    """
    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum','TOTAL_IN_ICU': 'sum'})

    newin_bar = go.Bar(x=df.index, y=df.NEW_IN, name=gettext('#New Hospitalized'))
    newout_bar = go.Bar(x=df.index, y=df.NEW_OUT, name=gettext('#New Discharged'))
    totin_bar = go.Bar(x=df.index, y=df.TOTAL_IN, name=gettext('#Total Hospitalized'))
    icu_bar = go.Bar(x=df.index, y=df.TOTAL_IN_ICU, name=gettext('#Total ICU'))
    fig_hospi = go.Figure(data=[totin_bar], layout=go.Layout(barmode='group'), )
    fig_hospi.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                            title=gettext("Total Hospitalizations"))

    fig_hospi.update_layout(xaxis_title=gettext('Day'),
                            yaxis_title=gettext('Number of / Day'))

    return fig_hospi


@register_plot_for_embedding("bar_hospitalization_in_out")
def bar_hospitalization_in_out():
    """
    bar plot hospitalization
    """
    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum','TOTAL_IN_ICU': 'sum'})

    newin_bar = go.Bar(x=df.index, y=df.NEW_IN, name=gettext('#New Hospitalized'))
    newout_bar = go.Bar(x=df.index, y=df.NEW_OUT, name=gettext('#New Discharged'))
    totin_bar = go.Bar(x=df.index, y=df.TOTAL_IN, name=gettext('#Total Hospitalized'))
    icu_bar = go.Bar(x=df.index, y=df.TOTAL_IN_ICU, name=gettext('#Total ICU'))
    fig_hospi = go.Figure(data=[newin_bar, newout_bar], layout=go.Layout(barmode='group'), )
    fig_hospi.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                            title=gettext("Daily IN-Out Hospitalizations"))

    fig_hospi.update_layout(xaxis_title=gettext('Day'),
                            yaxis_title=gettext('Number of / Day'))

    return fig_hospi



@register_plot_for_embedding("bar_hospitalization_ICU")
def bar_hospitalization_ICU():
    """
    bar plot hospitalization
    """
    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum', 'TOTAL_IN_ICU': 'sum'})

    icu_bar = go.Bar(x=df.index, y=df.TOTAL_IN_ICU, name=gettext('#Total ICU'))
    fig_hospi = go.Figure(data=[icu_bar], layout=go.Layout(barmode='group'), )
    fig_hospi.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                            title=gettext("Hospitalizations ICU"))

    fig_hospi.update_layout(xaxis_title=gettext('Day'),
                            yaxis_title=gettext('Number of / Day'))

    today = str((pd.to_datetime('today') - pd.Timedelta('0 days')).date())
    today = str((pd.to_datetime('today') - pd.Timedelta('0 days')).date())

    today_ = str((pd.to_datetime('today') - pd.Timedelta('100 days')).date())
    today_ = str((pd.to_datetime('today') - pd.Timedelta('100 days')).date())

    # Add shapes
    fig_hospi.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0="2020-03-15",
            y0=300,
            x1=today,
            y1=300,
            line=dict(
                color="RoyalBlue",
                width=3
            )
        ))

    # Add shapes
    fig_hospi.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0="2020-03-15",
            y0=2001,
            x1=today,
            y1=2001,
            line=dict(
                color="red",
                width=3
            )
        ))

    # Create scatter trace of text labels
    fig_hospi.add_trace(go.Scatter(
        x=[today_, today_],
        y=[330, 2030],
        text=["15% capa ICU",
              "100% capa ICU"],
        mode="text", name=""
    ))

    return fig_hospi



df_prov = pd.read_csv('static/csv/be-covid-provinces.csv')

# compute number of hospi / case in each province
df_tot_provinces_hospi = df_hospi.groupby(['PROVINCE_NAME']).agg({'NEW_IN': 'sum'})
df_tot_provinces_cases = df_prov.groupby(['PROVINCE_NAME']).agg({'CASES': 'sum'})
df_tot_provinces_hospi["NEW_IN_PER_CASES"] = df_tot_provinces_hospi['NEW_IN']/df_tot_provinces_cases["CASES"] #nombre d'hospi/nombre de cas
df_tot_provinces_hospi.reset_index(level=0, inplace=True)
df_tot_provinces_hospi.sort_values(by=["NEW_IN_PER_CASES"],inplace=True)
range_min = df_tot_provinces_hospi["NEW_IN_PER_CASES"].min()
range_max = df_tot_provinces_hospi["NEW_IN_PER_CASES"].max()


@register_plot_for_embedding("hospi_per_case_per_province")
def bar_hospi_per_case_per_province():
    fig = px.bar(df_tot_provinces_hospi,
                 y='PROVINCE_NAME',
                 x='NEW_IN_PER_CASES',
                 color='NEW_IN_PER_CASES',
                 orientation='h',
                 color_continuous_scale="deep",
                 range_color=(range_min, range_max),
                 hover_name="PROVINCE_NAME",
                 labels={'NEW_IN_PER_CASES': gettext('Total Hospitalisation per positive case')},
                 height=400)
    fig.update_traces(
        hovertemplate=gettext("<b>%{y}</b><br>%{x:.3f} hospitalisation per positive case"),
        textposition='outside',
        texttemplate='%{x:.3f}'
    )
    fig.layout.coloraxis.colorbar.titleside = 'right'
    fig.layout.yaxis.title = ""
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("hospi_over_death_smooth")
def hospi_over_death_smooth():
    data_y = moving_average(df.DEATHS.values, 7) / moving_average(df.TOTAL_IN.values, 7)
    fig = px.line(x=df.index, y=data_y, labels={'x': 'date', 'y': 'ratio death/hospi'})
    fig.update_layout(template="plotly_white")
    return fig


@register_plot_for_embedding("icu_over_hospi(")
def icu_over_hospi():
    data_y = df.TOTAL_IN_ICU / df.TOTAL_IN
    fig = px.line(x=df.index, y=data_y, labels={'x': 'date', 'y': 'ratio ICU/Hospi'})
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("death_over_icu_smooth")
def death_over_icu_smooth():
    fig = px.line(x=df.index,y=moving_average(df.DEATHS.values, 7)/moving_average(df.TOTAL_IN_ICU.values, 7),labels={'x':'date', 'y':'deaths/ICU'})
    fig.update_layout(template="plotly_white")
    return fig


@register_plot_for_embedding("hospi_smooth")
def hospi_smooth():
    fig = px.line(x=df.index,y=moving_average(df.TOTAL_IN.values, 7),labels={'x':'date', 'y':'total hospitals'},title="Total Hospitalization avg(7days)")
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("newin_smooth")
def newin_smooth():
    fig = px.line(x=df.index,y=moving_average(df.NEW_IN.values, 7),labels={'x':'date', 'y':'daily new in hospitals'},title="New Daily Hospitalization avg(7days)")
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("death_smooth")
def death_smooth():
    fig = px.line(x=df.index, y=moving_average(df.DEATHS.values, 7), labels={'x': 'date', 'y': 'deaths'},title="Daily deaths avg(7days)")
    fig.update_layout(template="plotly_white")
    return fig
