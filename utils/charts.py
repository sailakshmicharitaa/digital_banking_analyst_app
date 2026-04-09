import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def funnel_chart(df: pd.DataFrame):
    fig = go.Figure(
        go.Funnel(
            y=df["stage"],
            x=df["count"],
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str):
    fig = px.bar(df, x=x, y=y, title=title, text_auto=True)
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str, title: str):
    fig = px.line(df, x=x, y=y, title=title, markers=True)
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def pie_chart(df: pd.DataFrame, names: str, values: str, title: str):
    fig = px.pie(df, names=names, values=values, title=title)
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=50, b=20))
    return fig
