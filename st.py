# Importing necessary libraries
import pandas as pd
import numpy as np
import json
import os
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.io as pio
import nbformat
import streamlit as st

st.set_page_config(
    page_title="PhonePe Transaction Insights",  
    page_icon=":&#128507:",  
    layout="wide", 
    initial_sidebar_state="auto" 
)

st.markdown("""
<style>
body {
    background-color: "#FFF3CD";
}
</style>
""", unsafe_allow_html=True)


#MYSQL Connection Establishment to create required DataFrames
def get_data(query, params=None):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root',database="phonepe_transaction_insights")
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df
# mapping state names to their full forms
map_state = {
'andaman-&-nicobar-islands': 'Andaman & Nicobar',
'andhra-pradesh': 'Andhra Pradesh',
'arunachal-pradesh': 'Arunachal Pradesh',
'assam': 'Assam',
'bihar': 'Bihar',
'chandigarh': 'Chandigarh',
'chhattisgarh': 'Chhattisgarh',
'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
'delhi': 'Delhi',
'goa': 'Goa',
'gujarat': 'Gujarat',
'haryana': 'Haryana',
'himachal-pradesh': 'Himachal Pradesh',
'jammu-&-kashmir': 'Jammu & Kashmir',
'jharkhand': 'Jharkhand',
'karnataka': 'Karnataka',
'kerala': 'Kerala',
'ladakh': 'Ladakh',
'madhya-pradesh': 'Madhya Pradesh',
'maharashtra': 'Maharashtra',
'manipur': 'Manipur',
'meghalaya': 'Meghalaya',
'mizoram': 'Mizoram',
'nagaland': 'Nagaland',
'odisha': 'Odisha',
'puducherry': 'Puducherry',
'punjab': 'Punjab',
'rajasthan': 'Rajasthan',
'sikkim': 'Sikkim',
'tamil-nadu': 'Tamil Nadu',
'telangana': 'Telangana',
'tripura': 'Tripura',
'uttar-pradesh': 'Uttarakhand',
'uttarakhand': 'Uttar Pradesh',
'west-bengal': 'West Bengal'}



col1,col2 = st.columns([1,8])
with col1:
    st.image("C:/Users/mosel/Documents/PYTHON/PHONEPE_project/logo.png", width=100)
with col2:
    st.title("Phonepe Transaction Insights")



r = st.sidebar.radio('Navigation',["Home Page","Business Case Study"],index=0)
if r == "Home Page":
    st.subheader("**Application for Exploring Phonepe Transaction , Insurance & User Trends**")
    st.write(""" PhonePe Group is India’s leading fintech company. 
             Its flagship product, the PhonePe digital payments app, was launched in Aug 2016.
             Within a short period of time, the company has scaled rapidly to become India’s leading consumer payments app.
             On the back of its leadership in digital payments, PhonePe Group has expanded into financial services - Insurance, Lending, & Wealth as well as new consumer tech businesses - Pincode and Indus Appstore.

    **Database Used ="https://github.com/PhonePe/pulse"**
    """)

    col1,col2 = st.sidebar.columns(2,gap="medium")
    with col1:
        category = ["Transaction","User","Insurance"]
        category_select = st.sidebar.selectbox("",category)
    with col2:
        q = f"select DISTINCT concat(Year,'_Q', Quater) as Year_Qtr from aggregated_transaction;"
        df = get_data(q)
        yearquater_select = st.sidebar.selectbox("",df)


    if category_select == "Transaction":
        setname = "transaction"
        count1name = "Transaction_District_count"
        count2name="Transaction_Pincode_count"

        q = f'''select sum(Transaction_count) as 'Total Transactions',sum(Transaction_amount) as 'Total Revenue',
            avg(Transaction_count) as 'Average Transactions',avg(Transaction_amount) as 'Average Revenue'
            from aggregated_transaction where concat(Year,'_Q', Quater) = \"{yearquater_select}\"
            order by 2 DESC limit 10;'''
        df = get_data(q)
        total_transactions = df['Total Transactions'].iloc[0]
        total_revenue = df['Total Revenue'].iloc[0]
        average_transactions = df['Average Transactions'].iloc[0]
        average_revenue = df['Average Revenue'].iloc[0]

        col1, col2 = st.columns(2,gap = "small")
        with col1:
            st.metric('Total Transactions(₹)',value=total_transactions)
        with col2:
            st.metric('Total Revenue (₹)',value=total_revenue)    
        col1, col2 = st.columns(2,gap = "small")
        with col1:
            st.metric('Average Transactions(₹)',value=average_transactions)    
        with col2:
            st.metric('Average Revenue (₹)',value=average_revenue)  

        #INDIA MAP
        df = pd.read_csv("C:/Users/mosel/Documents/PYTHON/project/project_phonepe_transaction_insightAgg_Transaction.csv")
        df['State'] = df['State'].map(map_state)
        df['Year_Qtr'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        df1 = df[(df['Year_Qtr'] == yearquater_select)]
        state_list = df1['State'].unique()
        df2 = df1.groupby(['State']).agg(transcount=('Transaction_count', 'sum')).reset_index()
        fig = px.choropleth(
            df2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM", 
            locations="State",  
            color="transcount",  
            color_continuous_scale="dense",
            labels={'transcount': 'Total Transactions'}
        )

        fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
        )

        fig.update_layout(
            width=1200,
            height=800,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=True ,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    elif category_select == "User":

        setname ="User"
        count1name = "User_DistrictRegisteredusers"
        count2name = "User_PincodeRegisteredusers"

        q = f'''SELECT sum(Users_count) as 'Total Users', avg(Users_count) as 'Average Users' FROM aggregated_users
         where concat(Year,'_Q', Quater) = \"{yearquater_select}\";'''
        df = get_data(q)
        total_users = df['Total Users'].iloc[0]
        avg_users = df['Average Users'].iloc[0]
        col1,col2 = st.columns(2,gap="small")

        with col1:
            st.metric('Total Users',value=total_users)
        with col2:
            st.metric('Average Users',value=avg_users)

        #INDIA MAP
        df = pd.read_csv("C:/Users/mosel/Documents/PYTHON/project/project_phonepe_transaction_insightAgg_Users.csv")
        df['State'] = df['State'].map(map_state)
        df['Year_Qtr'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        df1 = df[(df['Year_Qtr'] == yearquater_select)]
        state_list = df1['State'].unique()
        df2 = df1.groupby(['State']).agg(usrcount=('Users_count', 'sum')).reset_index()
        fig = px.choropleth(
            df2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",  
            locations="State",  
            color="usrcount",  
            color_continuous_scale="magenta",
            labels={'usrcount': 'Total Users'}
        )

        fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
        )

        fig.update_layout(
            width=1200,
            height=800,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=True ,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    elif category_select == "Insurance":

        setname ="Insurance"
        count1name = "Insurance_District_count"
        count2name = "Insurance_Pincode_count"

        q = f'''select sum(Insurance_count) as 'Total Insurance',sum(Insurance_amount) as 'Total Insurance Revenue',
            avg(Insurance_count) as 'Average Insurance',avg(Insurance_amount) as 'Average Insurance Revenue'
            from aggregated_insurance;'''
        
        df = get_data(q)
        total_insurance = df['Total Insurance'].iloc[0]
        total_insurance_revenue = df['Total Insurance Revenue'].iloc[0]
        average_insurance = df['Average Insurance'].iloc[0]
        average_insurance_revenue = df['Average Insurance Revenue'].iloc[0]

        col1, col2 = st.columns(2,gap = "small")

        with col1:
            st.metric('Total Insurance(₹)',value=total_insurance)
        with col2:
            st.metric('Total Insurance Revenue (₹)',value=total_insurance_revenue)  

        col1, col2 = st.columns(2,gap = "small")

        with col1:
            st.metric('Average Insurance(₹)',value=average_insurance)    
        with col2:
            st.metric('Average Insurance Revenue(₹)',value=average_insurance_revenue)  

        #INDIA MAP
        df = pd.read_csv("C:/Users/mosel/Documents/PYTHON/project/project_phonepe_transaction_insightAgg_Insurance.csv")
        df['State'] = df['State'].map(map_state)
        df['Year_Qtr'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        df1 = df[(df['Year_Qtr'] == yearquater_select)]
        state_list = df1['State'].unique()
        df2 = df1.groupby(['State']).agg(insurancecount=('Insurance_count', 'sum')).reset_index()
        fig = px.choropleth(
            df2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",  
            locations="State",  
            color="insurancecount", 
            color_continuous_scale="reds",
            labels={'insurancecount': 'Total Insurance'}
        )

        fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
        )

        fig.update_layout(
            width=1200,
            height=800,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=True ,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        pass

    st.sidebar.write(f"**Top 10 {category_select}s**")

    col1,col2,col3 = st.sidebar.columns([1,1,2])
    with col1:
        if st.button("State"):
            q = f''' Select concat(substr(upper(State),1,1),substr(lower(State),2)) as State, 
            sum({count1name}) as 'Total {category_select}'
            from top_{setname}_district
            where concat(Year,'_Q', Quater) = \"{yearquater_select}\" 
            group by State order by 2 DESC limit 10;
                '''
            df = get_data(q)
            st.sidebar.write(df[['State',f'Total {category_select}']].set_index('State'))
        
    with col2:
        if st.button('District'):
            q = f''' Select concat(substr(upper({category_select}_District),1,1),substr(lower({category_select}_District),2)) as District, 
            sum({count1name}) as 'Total {category_select}'
            from top_{setname}_district
            where concat(Year,'_Q', Quater) = \"{yearquater_select}\" 
            group by District order by 2 DESC limit 10;
            '''
            df = get_data(q)
            st.sidebar.write(df[['District',f'Total {category_select}']].set_index('District'))
    
    with col3:
        if st.button("Postal Codes"):
            q = f''' Select concat(substr(upper({category_select}_Pincode),1,1),substr(lower({category_select}_Pincode),2)) as 'Postal Codes', 
            sum({count2name}) as 'Total {category_select}'
            from top_{setname}_pincode
            where concat(Year,'_Q', Quater) = \"{yearquater_select}\"
            group by 1 order by 2 DESC limit 10;
        '''
            df = get_data(q)
            st.sidebar.write(df[['Postal Codes',f'Total {category_select}']].set_index('Postal Codes'))   
  
else:
    case_studies = ["Decoding Transaction Dynamics on PhonePe",
                    "Device Dominance and User Engagement Analysis",                    
                    "Transaction Analysis for Market Expansion",
                    " User Registration Analysis",
                    "Insurance Engagement Analysis"]

    case_select = st.sidebar.selectbox("Select Business Case Study: ",case_studies)

    if case_select == case_studies[0]:

        st.subheader("Decoding Transaction Dynamics on PhonePe")
        st.write(''' PhonePe, a leading digital payments platform, has recently identified significant variations in transaction behavior across states, quarters, and payment categories. 
                 While some regions and transaction types demonstrate consistent growth, others show stagnation or decline. The leadership team seeks a deeper understanding of these patterns to drive targeted business strategies.''')
        #Insight 1
        st.subheader("The Most Popular Payment Methods")
        q="SELECT Transaction_type,sum(Transaction_count) as 'Total Transactions', sum(Transaction_amount) as 'Total Revenue' from aggregated_transaction group by Transaction_type;"
        df = get_data(q)
        fig = px.pie(df, names='Transaction_type', values='Total Transactions', 
                     title='Distribution of Payment Methods on PhonePe',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)
        
        # Insight 2  
        st.subheader("The Transaction amount by top 10 state")
        q = "SELECT State, sum(Transaction_amount) as 'Total Revenue' from aggregated_transaction group by State order by 2 DESC limit 10;"
        df = get_data(q)
        fig = px.bar(df, x='State', y='Total Revenue', 
                     title='Top 10 States by Transaction Amount',
                     color_discrete_sequence=px.colors.sequential.Sunset) 
        
        fig.update_layout(xaxis_title='State', yaxis_title='Total Revenue (₹)')
        st.plotly_chart(fig)

        # Insight 3
        st.subheader("The Transaction amount by top 10 District")
        q = "SELECT Transaction_District, sum(Transaction_District_amount) as 'Total Revenue' from top_transaction_district group by Transaction_District order by 2 DESC limit 10;"
        df = get_data(q)
        fig = px.bar(df, x='Transaction_District', y='Total Revenue', 
                     title='Top 10 District by Transaction Amount',
                     color_discrete_sequence=px.colors.sequential.Aggrnyl_r) 
        
        fig.update_layout(xaxis_title='District', yaxis_title='Total Revenue (₹)')
        st.plotly_chart(fig)

        #Insight 4
        st.subheader("The year which has the highest transaction amount")
        q = "SELECT Year, sum(Transaction_amount) as 'Total Revenue' from aggregated_transaction group by Year;"
        df = get_data(q)
        fig = px.pie(df, names='Year', values='Total Revenue',
                     title='Year with Highest Transaction Amount',
                     color_discrete_sequence=px.colors.sequential.YlOrBr)
    
        st.plotly_chart(fig)

        # Insight 5
        st.subheader("The year which has the highest transaction count")
        q = "SELECT Year, sum(Transaction_count) as 'Total Transactions' from aggregated_transaction group by Year;"
        df = get_data(q)
        fig = px.line(df, x='Year', y='Total Transactions',
                      title='Year with Highest Transaction Count',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='Year', yaxis_title='Total Transactions')
        st.plotly_chart(fig)
        
        # Insight 6
    
        st.subheader("The quaters which has the highest transaction count")
        q = "SELECT Quater, sum(Transaction_count) as 'Total Transactions' from aggregated_transaction group by Quater;"
        df = get_data(q) 
        fig = px.line(df, x='Quater', y='Total Transactions',
                      title='Quater with Highest Transaction Count',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='Quater', yaxis_title='Total Transactions')
        st.plotly_chart(fig) 

    elif case_select == case_studies[1]:

        st.subheader("Device Dominance and User Engagement Analysis")

        st.write(''' PhonePe aims to enhance user engagement and improve app performance by understanding user preferences across different device brands.
                The data reveals the number of registered users and app opens, segmented by device brands, regions, and time periods. 
                However, trends in device usage vary significantly across regions, and some devices are disproportionately underutilized despite high registration numbers.
         
                        ''')
         #Insight 1

        st.subheader("Device Brand Performance")

        q = "SELECT Users_brand, sum(RegisteredUsers) as 'Total Registered Users', sum(AppOpens) as 'Total App Opens' from aggregated_users group by Users_brand;"
        df = get_data(q)
        fig = px.bar(df, x='Users_brand', y='Total Registered Users',
                     title='Device Brand Performance',
                     color_discrete_sequence=px.colors.sequential.YlOrBr)
        fig.update_layout(xaxis_title='Device Brand', yaxis_title='Total Registered Users')
        st.plotly_chart(fig)


        #Insight 2 

        st.subheader("Engagement Rate Analysis")

        q= "SELECT Users_brand, sum(AppOpens)/sum(RegisteredUsers) as 'Engagement Rate' from aggregated_users group by Users_brand;"
        df = get_data(q)
        fig = px.bar(df, x='Users_brand', y='Engagement Rate',
                     title='Engagement Rate by Device Brand',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='Device Brand', yaxis_title='Engagement Rate')
        st.plotly_chart(fig)

        #Insight 3
        st.subheader("Regional Trends")
        q= "SELECT Users_brand, State, sum(RegisteredUsers) as 'Total Registered Users', sum(AppOpens) as 'Total App Opens' from aggregated_users group by Users_brand, State;"
        df = get_data(q)
        fig = px.pie(df, names='Users_brand', values='Total Registered Users',
                     title='Regional Trends in Device Usage',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)

        #Insight 4

        st.subheader("Time-Based Trends")
        q= "SELECT Year, Quater, sum(RegisteredUsers) as 'Total Registered Users', sum(AppOpens) as 'Total App Opens' from aggregated_users group by Year, Quater;"
        df = get_data(q)
        fig = px.line(df, x='Year', y='Total Registered Users',
                      title='Time-Based Trends in Device Usage',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='Year', yaxis_title='Total Registered Users')
        st.plotly_chart(fig)

    elif case_select == case_studies[2]:
        st.subheader("Transaction Analysis for Market Expansion")

        st.write('''PhonePe operates in a highly competitive market, and understanding transaction dynamics at the state level is crucial for strategic decision-making. 
                 With a growing number of transactions across different regions, the company seeks to analyze its transaction data to identify trends, opportunities, and potential areas for expansion.
                 ''')
        #Insight 1
        st.subheader("State-Level Transaction Summary") 

        #Insight 1 & 2:
        col1,col2,col3 = st.columns(3,gap="small")
        with col1:
            q = "select State from aggregated_users group by State;"
            ste = get_data(q)    
            ste_select = st.selectbox("Select State: ", ste)
        with col2:
            q = "select Year from aggregated_transaction group by Year;"
            yr = get_data(q)
            yr_sel = st.selectbox("Select Year: ", yr)
        with col3:    
            q = "select Quater from aggregated_transaction group by Quater;"
            qr = get_data(q)
            q_sel = st.selectbox("Select Quarter: ", qr)


        q = f'''
        SELECT * from map_transaction_hover
        WHERE State = \"{ste_select}\" AND Year = \"{yr_sel}\" AND Quater = {q_sel}
        ORDER BY Transaction_Hover_count DESC;
        '''
        df = get_data(q)        
        bss = px.line(df,x='Transaction_Hover_name', y='Transaction_Hover_count',
                title='Total Transactions by District',
                labels={'Transaction_Hover_name': 'Districts','Transaction_Hover_count': 'Total Number of Transactions'})
        bss.update_layout(width = 2000, height=500,)
        st.plotly_chart(bss)
        
     
        sr = px.line(df,x='Transaction_Hover_name', y='Transaction_Hover_count',
                title='Total Transactions by District',
                labels={'Transaction_Hover_name': 'Districts','Transaction_Hover_count': 'Total Number of Transactions'})
        st.plotly_chart(sr)


        #Insight 3:
        q = f'''Select *, concat(Year,"_Q", Quater) as Year_Qtr FROM map_transaction_hover
        WHERE State = \"{ste_select}\";
        '''
        df = get_data(q)

        lne = px.bar(df, x='Year_Qtr', y='Transaction_Hover_count',
                title='Total Transactions by Year and Quarter',
                labels={'Year_Qtr': 'Year and Quarter','Transaction_Hover_count': 'Total Number of Transactions'})
        lne.update_layout(width = 2000, height=500,)
        st.plotly_chart(lne)

    elif case_select == case_studies[3]:
        st.subheader("User Registration Analysis")

        st.write('''PhonePe aims to conduct an analysis of user registration data to identify the top states, districts,
                  and pin codes from which the most users registered during a specific year-quarter combination. 
                 This analysis will provide insights into user engagement patterns and highlight potential growth areas.''')
        #Insight 1
        st.subheader("Top 10 States by User Registration")
        q= "select State, sum(RegisteredUsers) as 'Total Registered Users' from aggregated_users group by State order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.line(df, x='State', y='Total Registered Users',
                      title='Top 10 States by User Registration',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='State', yaxis_title='Total Registered Users')
        st.plotly_chart(fig)

        #Insight 2
        st.subheader("Top 10 Districts by User Registration")
        q= "select User_District, sum(User_DistrictRegisteredUsers) as 'Total Registered Users' from top_user_district group by User_District order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.bar(df, x='User_District', y='Total Registered Users',
                        title='Top 10 Districts by User Registration',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        fig.update_layout(xaxis_title='District', yaxis_title='Total Registered Users')
        st.plotly_chart(fig)

        #Insight3
        st.subheader("Top 10 Pin Codes by User Registration")
        q= "select User_Pincode, sum(User_PincodeRegisteredUsers) as 'Total Registered Users' from top_user_pincode group by User_Pincode order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.pie(df, names='User_Pincode', values='Total Registered Users',
                     title='Top 10 Pin Codes by User Registration',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)

    elif case_select == case_studies[4]:
        st.subheader("Insurance Engagement Analysis")

        st.write('''PhonePe aims to conduct an analysis of insurance engagement data to identify the top states, districts,
                  and pin codes from which the most users engaged with insurance products during a specific year-quarter combination. 
                 This analysis will provide insights into user engagement patterns and highlight potential growth areas.''')
        #Insight 1
        st.subheader("Top 10 States by Insurance Engagement")
        q= "select State, sum(Insurance_count) as 'Total Insurance' from aggregated_insurance group by State order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.line(df, x='State', y='Total Insurance',
                      title='Top 10 States by Insurance Engagement',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title='State', yaxis_title='Total Insurance')
        st.plotly_chart(fig)

        #Insight 2
        st.subheader("Top 10 Districts by Insurance Engagement")
        q= "select Insurance_District, sum(Insurance_District_count) as 'Total Insurance' from top_insurance_district group by Insurance_District order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.bar(df, x='Insurance_District', y='Total Insurance',
                        title='Top 10 Districts by Insurance Engagement',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        fig.update_layout(xaxis_title='District', yaxis_title='Total Insurance')
        st.plotly_chart(fig)

        #Insight3
        st.subheader("Top 10 Pin Codes by Insurance Engagement")
        q= "select Insurance_Pincode, sum(Insurance_Pincode_count) as 'Total Insurance' from top_insurance_pincode group by Insurance_Pincode order by 2 DESC limit 10 ;"
        df=get_data(q)
        fig = px.pie(df, names='Insurance_Pincode', values='Total Insurance',
                     title='Top 10 Pin Codes by Insurance Engagement',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)

    else:
        pass
