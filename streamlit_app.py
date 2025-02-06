import streamlit as st
import pandas as pd 
import plotly.express as px 
from plotly.subplots import make_subplots

#set page layout
st.set_page_config(layout='wide')

st.title("Retail Store Analysis Results")


df = pd.read_csv('retail_store_sales.csv')
print(df)
df['transaction date'] = pd.to_datetime(df['transaction date'])

categories=list(df['category'].unique())


def page1():
    st.header('Customer Data')
    tab1 , tab2  = st.tabs(['Spendings' , 'Payment' ])
    
 
    
    with tab1:
        st.header('How much does a customer usually spend ')
        st.plotly_chart(px.violin(df , x='total spent' , box = True ))
        
        st.header('Customer Spending Pattern and purchase behaviour')
        st.plotly_chart(px.density_heatmap(df , x='quantity' , y='total spent'))
        # df_temp = df[(df['category'] == 'Butchers') & (df['transaction date'].dt.year == 2024)]
        st.plotly_chart(px.scatter(df, x='quantity', y='total spent', trendline='ols', title='Quantity vs. Total Spent'))

            
    with tab2:

        st.header('The prefered payment method for the customers between online and in store purchases')
        st.plotly_chart(px.pie(df , names='payment method' , color_discrete_sequence=['navy','teal','maroon'] ,facet_col='location', title='Prefered payment method'))
    


def page2():
    st.header('Sales')
    tab1 , tab2,tab3  = st.tabs(['by Year' , 'Category and purchase location','Category and year' ])
    with tab1:
        st.header('sales over time by year')
        years=list(df['transaction date'].dt.year.unique())
        year=st.select_slider('select year',years)
        st.write(year)
        df_temp = df[df['transaction date'].dt.year == year]
        df_grouped =df_temp.groupby('transaction date')['total spent'].sum().reset_index()
        st.plotly_chart(px.line(df_grouped, x='transaction date', y='total spent', title='Total Sales Over Time'))
    
    with tab2:
        st.header('Sales by category and the place of purchase')
        categories=list(df['category'].unique())
        category=st.selectbox('select cat',categories)
        st.write(category)
        locations=df['location'].unique()
        location=st.radio('Select purchase location',locations)
        st.write(location)
        st.plotly_chart(px.histogram(df_temp , x='category' , y = 'total spent' , color='location', text_auto=True ,title='Sales by category' 
             ,color_discrete_sequence=['navy','gray'] ,barmode='group'))
    
    with tab3:
        st.header('Sales of a specific category over year')
        categories=list(df['category'].unique())
        category=st.selectbox('select category',categories)
        st.write(category)
        years=list(df['transaction date'].dt.year.unique())
        year=st.select_slider('select year',years)
        st.write(year)
        df_temp = df[(df['category'] == category) & (df['transaction date'].dt.year == year)]
        st.plotly_chart(px.histogram(df_temp , x='transaction date' , y='total spent' , color_discrete_sequence=['navy'] , text_auto=True ))
    




def page3():

    st.header(" Distribution of Total Spent per Category")
    st.plotly_chart(px.box(df, x='category', y='total spent', color='category', title='Total Spent Distribution per Category',
       color_discrete_sequence=['navy', 'gray', 'lightblue','maroon', 'teal', 'gold','black','blue','purple']
)
)
    

pages = {
    'Customer Data' : page1,
    'Sales' : page2,
    'Other' : page3
}

pg = st.sidebar.radio('Navigate between pages' , pages.keys())

pages[pg]()
