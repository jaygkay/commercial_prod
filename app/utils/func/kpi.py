import json
import plotly
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from app.utils.proc import proc


def GRAPH_OPERATIONS(df_master, target_id):
    df = df_master.groupby(['period_type', 'period']).agg({str(target_id): 'sum'}).reset_index()
    df['period'] = [i.split('(')[1].split()[0] if 'W' in i else i for i in df['period']]
    df['pct_change'] = round(df.groupby(['period_type'])[str(target_id)].pct_change() * 100, 2)
    df['text'] = df[str(target_id)].astype(str) + ' (' + df['pct_change'].astype(str).replace('nan', '0') + '%)'

    fig = px.bar(
        df,
        x='period',
        y=str(target_id),
        color = str(target_id),
        facet_row='period_type',
        template='plotly_white',
        height=800,
        text=str(target_id),
        hover_name='text',
        category_orders={'period_type': ['ALL', 'YEAR', 'QUARTER', 'MONTH', 'WEEK']},
    )

    fig.for_each_annotation(lambda a: a.update(text='<b>' + a.text.split("=")[1] + '</b>', textangle=-360))
    fig.for_each_xaxis(lambda x: x.update(showticklabels=True, matches=None))
    fig.for_each_yaxis(lambda y: y.update(showticklabels=True, matches=None))
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig


