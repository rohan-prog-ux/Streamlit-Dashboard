# pylint: disable=use-dict-literal
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Getting data from googlesheet or CSV


def data_read():
    df = pd.read_csv("/Users/mac/Desktop/Streamlit/load.csv")
    return df

# List of all states


def get_states(df):
    return sorted(df["state"].unique())


def main():
    df = data_read()

    # # Get list of all available states

    # Title of the dashboard
    st.title('Consumer Financial Complaints Dashboard')

    # Giving header to all states
    st.subheader(
        'Display Data for “All States” or “Colorado” State (Based on Filter Selected)')

    st.write(df)

    col1, col2, col3, col4 = st.columns(4)

    selected_state = st.sidebar.selectbox(
        "Select a State", sorted(df["state"].unique()))

    filtered_data = df[df["state"] == selected_state]

    # Display charts and KPIs based on DATA
    col1.metric(label="Total Complaints",
                value=filtered_data["compliant_ids"].nunique())

    closed_data = filtered_data[filtered_data["company_respopnse"].str.contains(
        "Closed")]
    col2.metric(label="Total Closed Complaints",
                value=closed_data["compliant_ids"].nunique())

   # "% of Timely Responded Complaints"
    timely_data = filtered_data[filtered_data["timely"] == "Yes"]
    percentage = round((timely_data["compliant_ids"].nunique(
    ) / filtered_data["compliant_ids"].nunique()) * 100, 2)
    col3.metric(label="% Timely Response", value=percentage)

   # "Total Number of Complaints with In Progress Status"
    in_progress_data = filtered_data[filtered_data["company_respopnse"]
                                     == "In progress"]
    col4.metric(label="In Progress Complaints",
                value=in_progress_data["compliant_ids"].nunique())

    st.subheader("Horizontal Bar Plot of Number of complaints by products")
    products = filtered_data.groupby("products").size()
    st.bar_chart(products)

    st.subheader("Line Chart of Number of Complaints Over Time (Month Year)")
    filtered_data["date_recive"] = pd.to_datetime(
        filtered_data["date_recive"])
    time_data = filtered_data.groupby(pd.Grouper(
        key="date_recive", freq="M")).size().reset_index(name="Count")
    st.line_chart(time_data.set_index("date_recive"))

    if selected_state != "All States":
        df = df[df["state"] == selected_state]

    # Pie Chart
    st.subheader("Pie Chart of Number of complaint by Submitted Via Channel")
    pie_chart_data = df.groupby("submitted_via").agg(
        {"compliant_ids": "count"}).reset_index()
    fig = px.pie(pie_chart_data, values="compliant_ids", names="submitted_via")
    st.plotly_chart(fig, use_container_width=True)

    # Tree Map
    treemap_data = df.groupby(["issues", "sub_issue"]).agg(
        {"compliant_ids": "count"}).reset_index()
    fig = go.Figure(go.Treemap(
        labels=treemap_data["issues"] + " - " + treemap_data["sub_issue"],
        parents=["" for _ in range(len(treemap_data))],
        values=treemap_data["compliant_ids"]
    ))
    fig.update_layout(margin=dict(t=20, l=0, r=0, b=0))

    st.subheader("Treemap of Number Over Complaints by issues and Sub-Issue")

    st.plotly_chart(fig, use_container_width=True)
    # its give the designed by:
    st.write("Designed by Rohan Vaswani")


if __name__ == "__main__":
    main()
