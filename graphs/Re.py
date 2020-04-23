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
    - we have a moving average of the positive cases
    """
    #print (df_testing.CASES)
    cases=moving_average(cases.values,7)
    all_declared_cases=np.cumsum(cases)
    active_cases=all_declared_cases[n:-1] - np.cumsum(cases[0:-n-1])
    #print ( active_cases )
    rate_increase=cases[n+1:]/active_cases
    #print (rate_increase)
    # hypothesis: 
    rate_decrease=cases[1:-n]/active_cases
    #print (rate_decrease)
    Re=(rate_increase)/(rate_decrease)
    #print (Re)
    moving_average_Re = moving_average(Re,1)
    #print (moving_average_Re)
    
    return moving_average_Re[10-n:]

def Re_estimate2(cases,n,delay_test=0):
    """
    Re estimate under the hypotheses that 
    - any person diagnosed positive to Covid-19 will have a chance 1/n to heal (or die actually)
    - we have a moving average of the positive cases
    """
    #print (df_testing.CASES)
    cases=moving_average(cases.values,7)
    all_declared_cases=np.cumsum(cases)
    active_cases=[all_declared_cases[0]]
    no_more_active=[]
    for i,n_cases in enumerate(all_declared_cases[:-1]):
        no_more_active.append(active_cases[i]*1/n)
        active_cases.append(all_declared_cases[i+1]-no_more_active[-1])

    active_cases=np.array(active_cases)
    no_more_active=np.array(no_more_active)
    #print ( active_cases )
    rate_increase=cases[1:]/active_cases[:-1]
    #print (rate_increase)
    # hypothesis 2: among all active cases, 1/n of the declared cases heal (or die actually)
    rate_decrease=no_more_active[:]/active_cases[:-1]
    #print (rate_decrease)
    Re=(rate_increase)/(rate_decrease)
    #print (Re)
    moving_average_Re = moving_average(Re,1)
    #print (moving_average_Re)
    
    return moving_average_Re[10-n:]


@register_plot_for_embedding("testing_testing_over_cases")
def plot_Re():
    """
    We make the hypotheses that 
    - any person diagnosed positive to Covid-19 will on average be positive for 14 days.

    """
    #Re_estimate14 = Re_estimate(df_testing.CASES,n=14)
    #Re_estimate12 = Re_estimate(df_testing.CASES,n=12)
    Re_estimate10 = Re_estimate(df_testing.CASES,n=10)
    Re_estimate8 = Re_estimate(df_testing.CASES,n=8)
    Re_estimate6 = Re_estimate(df_testing.CASES,n=6)
    Re_estimate4 = Re_estimate(df_testing.CASES,n=4)
    
    
    
    fig = go.Figure(data=[go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate4, name="n=4"), # +3:-4 takes into account the moving average
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate6, name="n=6"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate8, name="n=8"),
                          go.Scatter(x=df_testing.DATE[10+3:-4], y=Re_estimate10, name="n=10"),                    
                          #go.Scatter(x=df_testing.DATE[10+7:], y=Re_estimate12, name=gettext("n=12")),                    
                          ],                    
)
    fig.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('Effective number of secondary infections Re'),
                   title=gettext("Evolution of the average number of new patients infected per positive case"))
    fig.update_yaxes(range=[0, 5])
    return fig

