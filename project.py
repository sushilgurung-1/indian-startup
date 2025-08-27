import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="StartUp Analysis")

# data insertion
df = pd.read_csv("startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    # last5_df = df[df["Investors"] == "Ratan Tata"].sort_values(by="date")[["date", "startup", "vertical", "city", "round", "amount"]].head()
    last5_df = df[df["Investors"].str.contains(investor)].sort_values(by="date")[["date", "startup", "vertical", "city", "round", "amount"]].head()

    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
    # biggest Investments
        st.subheader("Biggest Investors")
        big_df = df[df["Investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(big_df.index,big_df.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df["Investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sectors invested in")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f")
        st.pyplot(fig1)

    # year-based investments
    df["year"] = df["date"].dt.year

    year_df = df[df["Investors"].str.contains("Amazon")].groupby("year")["amount"].sum()
    st.subheader("Year-based Investments")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_df.index, year_df.values)
    st.pyplot(fig2)

def load_overall_analysis():
    st.title("Overall Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # total invested amount
        total = round(df["amount"].sum())
        st.metric("total", total, "Cr")
    with col2:
        # max amount infused in a startup
        max_funding = df.groupby("startup")["amount"].max().sort_values(ascending=False).head().values[0]
        st.metric("Max", max_funding, "Cr")
    with col3:
        # avg ticket size
        avg = round(df.groupby("startup")["amount"].sum().mean())
        st.metric("Avg", avg, "Cr")
    with col4:
        # Total funded startup
        num_startups = df["startup"].nunique()
        st.metric("Funded Startups", num_startups, "Cr")

    st.header("MoM graph")

    selected_option = st.selectbox("Select Type", ["Total", "Count"])
    if selected_option == "Total":
        temp_df  = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        temp_df  = df.groupby(["year", "month"])["amount"].count().reset_index()
    temp_df["x_axis"] = temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df["x_axis"], temp_df["amount"])
    st.pyplot(fig3)


# st.header("Upload a file")
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select One", ["Overall Analysis", "StartUp", "Investor"])

if option == "Overall Analysis":
    # # st.title("Overall Analysis")
    # btn0 = st.sidebar.button("Show Overall Analysis")
    # if btn0:
    load_overall_analysis()


elif option == "StartUp":
    st.sidebar.selectbox("Select StartUp", sorted(df["startup"].unique().tolist()))
    btn = st.sidebar.button("Startup Analysis")
    st.title("StartUp Analysis")
elif option == "Investor":
    # st.title("Investor Analysis")
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df["Investors"].str.split(",").sum())))
    btn = st.sidebar.button("Investors Analysis")

    if btn:
        load_investor_details(selected_investor)