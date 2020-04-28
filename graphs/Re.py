import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np
from graphs import register_plot_for_embedding

df_testing = pd.read_csv('static/csv/be-covid-testing.csv')

def moving_average(a, n=1) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def Re_estimate(cases,n,delay_test=0):
    """
    Re estimate under the hypotheses that 
    - any person diagnosed positive to Covid-19 will be positive for n days.
    - we have a moving average over 7 days of the positive cases (important because testing is done less during weekends)
    """
    cases=moving_average(cases.values,7)
    all_declared_cases=np.cumsum(cases)
    active_cases=all_declared_cases[n:-1] - np.cumsum(cases[0:-n-1])
    rate_increase=cases[n+1:]/active_cases
    rate_decrease=cases[1:-n]/active_cases
    Re=(rate_increase)/(rate_decrease)
    
    return rate_increase,rate_decrease,Re[10-n:]

def estimate_of_daily_exp_factor(cases,n):
    """
    Estimate of the multiplicative increase rate of the active base (on a daily basis)
    - any person diagnosed positive to Covid-19 will be positive for n days.
    - we have a moving average over 7 days of the positive cases (important because testing is done less during weekends)
    """
    cases=moving_average(cases.values,7)
    all_declared_cases=np   .cumsum(cases)
    all_no_more_active_cases=np.zeros(all_declared_cases.shape)
    all_no_more_active_cases[n:]=all_declared_cases[:-n]
    active_cases=all_declared_cases - all_no_more_active_cases
    exp_factor=active_cases[1:]/active_cases[:-1]
    
    return exp_factor

def Re_estimate2(cases,n,delay_test=0):
    """
    Re estimate under the hypotheses that 
    - any person diagnosed positive to Covid-19 will have a chance 1/n to heal (or die actually)
    - we have a moving average over 7 days of the positive cases (important because testing is done less during weekends)
    """
    cases=moving_average(cases.values,7)
    all_declared_cases=np.cumsum(cases)
    active_cases=[all_declared_cases[0]]
    no_more_active=[]
    for i,n_cases in enumerate(all_declared_cases[:-1]):
        no_more_active.append(active_cases[i]*1/n)
        active_cases.append(all_declared_cases[i+1]-no_more_active[-1])

    active_cases=np.array(active_cases)
    no_more_active=np.array(no_more_active)
    rate_increase=cases[1:]/active_cases[:-1]
    rate_decrease=no_more_active[:]/active_cases[:-1]
    Re=(rate_increase)/(rate_decrease)
    
    return Re[10-n:]


@register_plot_for_embedding("testing_testing_over_cases")
def plot_Re():
    """
    We make the hypotheses that 
    - any person diagnosed positive to Covid-19 will on average be positive for n days.

    """
    rate_increase10,rate_decrease10,Re_estimate10 = Re_estimate(df_testing.CASES,n=10)
    rate_increase8,rate_decrease8,Re_estimate8 = Re_estimate(df_testing.CASES,n=8)
    rate_increase6,rate_decrease6,Re_estimate6 = Re_estimate(df_testing.CASES,n=6)
    rate_increase4,rate_decrease4,Re_estimate4 = Re_estimate(df_testing.CASES,n=4)

    
    fig_rate_increase = go.Figure(data=[go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_increase4, name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_increase6, name="n=6"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_increase8, name="n=8"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_increase10, name="n=10"),                    
                          ],                    
)
    fig_rate_increase.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Estimated effective infection rate increase'),
                   title=gettext("Evolution of the infection rate increase"))
    #fig_rate_increase.update_yaxes(range=[0, 5])

    fig_rate_decrease = go.Figure(data=[go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_decrease4, name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_decrease6, name="n=6"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_decrease8, name="n=8"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=rate_decrease10, name="n=10"),                    
                          ],                    
)
    fig_rate_decrease.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Estimated effective infection rate decrease'),
                   title=gettext("Evolution of the infection rate decrease"))
    #fig_rate_decrease.update_yaxes(range=[0, 5])

    figRe = go.Figure(data=[go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate4, name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate6, name="n=6"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate8, name="n=8"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate10, name="n=10"),                    
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=np.array([1 for n in range((df_testing.DATE[10+3:-4].shape[0]))]), name="n=10", line=dict(width=3,color='orange')),                    
                          ],                    
)
    figRe.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Estimated effective infection rate Re'),
                   title=gettext("Evolution of the average number of new patients infected per positive case"))
    figRe.update_yaxes(range=[0, 5])
    return fig_rate_increase,fig_rate_decrease,figRe

def plot_daily_exp_factor():
    """
    We make the hypotheses that 
    - any person diagnosed positive to Covid-19 will on average be positive for n days.

    """
    exp_factor10 = estimate_of_daily_exp_factor(df_testing.CASES,n=10)
    exp_factor8 = estimate_of_daily_exp_factor(df_testing.CASES,n=8)
    exp_factor6 = estimate_of_daily_exp_factor(df_testing.CASES,n=6)
    exp_factor4 = estimate_of_daily_exp_factor(df_testing.CASES,n=4)    
    
    
    fig = go.Figure(data=[go.Scatter(x=df_testing.DATE[3:-4], y=exp_factor4, name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[3:-4], y=exp_factor6, name="n=6"),
                          go.Scatter(x=df_testing.DATE[3:-4], y=exp_factor8, name="n=8"),
                          go.Scatter(x=df_testing.DATE[3:-4], y=exp_factor10, name="n=10"),                    
                          go.Scatter(x=df_testing.DATE[3:-4], y=np.array([1 for n in range((df_testing.DATE[3:-4].shape[0]))]), name="n=10", line=dict(width=3,color='orange')),                    
                          ],                    
)
    fig.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Daily multiplicative factor'),
                   title=gettext("Estimate of the daily multiplicative rate of the number of active cases, >1 is an increase, <1 is a decrease"))
    return fig


def plot_Re_div_n():
    """
    We make the hypotheses that 
    - any person diagnosed positive to Covid-19 will on average be positive for n days.

    """
    rate_increase10,rate_decrease10,Re_estimate10 = Re_estimate(df_testing.CASES,n=10)
    rate_increase8,rate_decrease8,Re_estimate8 = Re_estimate(df_testing.CASES,n=8)
    rate_increase6,rate_decrease6,Re_estimate6 = Re_estimate(df_testing.CASES,n=6)
    rate_increase4,rate_decrease4,Re_estimate4 = Re_estimate(df_testing.CASES,n=4)
    
    
    
    fig = go.Figure(data=[go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate4**(1/4), name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate6**(1/6), name="n=6"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate8**(1/8), name="n=8"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate10**(1/10), name="n=10"),                    
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=np.array([1 for n in range((df_testing.DATE[10+3:-4].shape[0]))]), name="n=10", line=dict(width=3,color='orange')),                    
                          ],                    
)
    fig.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Re^(1/n)'),
                   title=gettext("Estimate of the multiplicative increase rate of the active base (on a daily basis) from the Re factor"))
    #fig.update_yaxes(range=[0, 2])
    return fig


