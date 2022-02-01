import streamlit as st
import pandas as pd
import altair as alt
from charts import ChartProvider
import requests
from PIL import Image
from data import DataProvider

st.set_page_config(page_title="Prism Forge - Analytics",\
        page_icon=Image.open(requests.get('https://raw.githubusercontent.com/IncioMan/on-chain-data-analysis/prism_launch/prism_launch/images/xPRISM.png',stream=True).raw),\
        layout='wide')

###

@st.cache(ttl=10, show_spinner=False, allow_output_mutation=True)
def claim(claim_hash, cols_claim):
    try:
        df_claim = pd.read_json(
            f"https://api.flipsidecrypto.com/api/v2/queries/{claim_hash}/data/latest",
            convert_dates=["BLOCK_TIMESTAMP"],
        )
    except:
        return pd.DataFrame(columns = cols_claim[claim_hash])
    if(len(df_claim.columns)==0):
        return pd.DataFrame(columns = cols_claim[claim_hash])
    return df_claim

data_provider = DataProvider(claim)
chart_provider = ChartProvider()

###
###

original_title = '<p style="font-size: 60px;">Prism Forge - Phase 1</p>'
col1, col2 = st.columns([1,12])
with col2:
    st.markdown(original_title, unsafe_allow_html=True)
with col1:
    st.image('https://raw.githubusercontent.com/IncioMan/on-chain-data-analysis/prism_launch/prism_launch/images/prism_white_small.png')
st.text('')
st.text('')
st.text('')

col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

with col2:
    st.metric(label="Total UST deposited",\
              value=f"${round((data_provider.tot_deposits/1000000.0),3)}M",\
              delta=f"{int((data_provider.tot_deposits-data_provider.next_last_ust)/1000)}k")

with col3:
    st.metric(label="Unique users", value=data_provider.n_users, delta=int(data_provider.n_users-data_provider.next_last_users),
     delta_color="off")
    
with col4:
    st.metric(label="Transactions", value=data_provider.n_txs, delta=int(data_provider.n_txs-data_provider.next_last_txs),
     delta_color="off")

with col5:
    st.metric(label="Estimated price", value=f"${round(data_provider.tot_deposits/70000000,2)}", delta=round(((data_provider.tot_deposits-data_provider.next_last_ust))/70000000,2),delta_color="off")
####
st.subheader('UST deposited over time')
st.markdown("""This graph shows the cumulative net UST deposits into the Prism Forge. 70 million PRISM tokens are allocated to the Prism Forge and will be distributed to depositors based on their net UST contributed during this phase.""")
st.altair_chart(chart_provider.cum_ust_chart(data_provider.hourly_stats_df), use_container_width=True)
####
col1, col2 = st.columns(2)
with col1:
    st.subheader('Transactions over time')
    st.markdown("""This graph represents the number of deposits and withdrawals performed every hour in the Prism Forge.         """)
    st.altair_chart(chart_provider.txs_over_time_chart(data_provider.hourly_stats_df), use_container_width=True)
with col2:
    st.subheader('Users over time')
    st.markdown("""How does the total number of users who have interacted with the Prism Forge since launch look over time?""")
    st.altair_chart(chart_provider.users_over_time_chart(data_provider.hourly_new_users_df), use_container_width=True)
####
col1, col2 = st.columns(2)
with col1:
    st.subheader('User deposits distribution')
    st.markdown("""How much UST are people depositing into the Forge each time? Well, this graph shows the distribution of deposits based on several ranges.""")
    st.altair_chart(chart_provider.users_dep_distr_chart(data_provider.deposits_bucket_df), use_container_width=True)
with col2:
    st.subheader('Number of transactions per wallet')
    st.markdown("""Are people performing one or multiple transactions on average? Here, we have the distribution of transactions per wallet into the Forge.
    """)
    st.altair_chart(chart_provider.n_tx_wallet_chart(data_provider.user_stats_df), use_container_width=True)
####
st.subheader('Participants from previous bootstrapping or community farming events')
st.markdown("""For those who have participated in these previous launch events, how many of them have participated in the Prism Forge so far?""")
st.altair_chart(chart_provider.user_part_prev_launches_chart(data_provider.prev_launches_df), use_container_width=True)
####
st.subheader('Participants\' wallet age')
st.markdown("""Are the participants mainly Terra OGs? This graph shows the number of wallets participating in the Prism Forge based on the date their wallets are created.""")
st.altair_chart(chart_provider.wallet_age_chart(data_provider.wallet_age_df, data_provider.dates_to_mark), use_container_width=True)
###
st.subheader('Top depositors')
st.markdown("""Let's now see the top 5 addresses which have deposited the most UST. If you are curious, you can 
look these addresses up on [ET Finder](https://finder.extraterrestrial.money/).""")
st.table(data_provider.top_depositors)
####
st.subheader('Deposit distribution per balance')
st.markdown("""This graph depicts the distribution of UST deposited against the average balance of the respective wallets. Essentially we are asking the question - are wallets with high average balances depositing more UST or vice versa?
You can interact with the graph by zooming in and out to explore specific ranges. Zoom all the way out to see outliers.""")
st.altair_chart(chart_provider.dep_dist_balance_chart(data_provider.deposit_balance_df), use_container_width=True)
###
st.text('')
st.markdown("This dashboard was built with love for the 🌖 community by [IncioMan](https://twitter.com/IncioMan) and [sam](https://twitter.com/sem1d5) - with the support of [flipsidecrypto](https://flipsidecrypto.xyz/). You can participate in Prism Forge [here](https://forge.prismprotocol.app/).")
st.markdown("""
<style>
    @media (min-width:640px) {
        .block-container {
            padding-left: 5rem;
            padding-right: 5rem;
        }
    }
    @media (min-width:800px) {
        .block-container {
            padding-left: 15rem;
            padding-right: 15rem;
        }
    }
    .block-container
    {
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)
hide_streamlit_style = """
                        <style>
                        footer {visibility: hidden;}
                        </style>
                        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)