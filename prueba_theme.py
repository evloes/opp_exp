# Import libraries
import streamlit as st
import pandas as pd
import numpy as np   
from matplotlib import pyplot as plt
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas
import altair as alt
from PIL import Image
from vega_datasets import data
import calendar as cal
#import zeta_theme
import urban_theme # where the color theme is 


st.set_page_config(layout="wide", page_title='ZMP-Opportunity Explorer Streamlit app')
base="light"
primaryColor="#BF2A7C" #PINK
backgroundColor="#FFFFFF" #MAIN WINDOW BACKGROUND COLOR (white)
secondaryBackgroundColor="#EBF3FC" #SIDEBAR COLOR (light blue)
textColor="#31333F"
secondaryColor="#F0F2F6" #dark_blue
tertiaryColor ="#0810A6"
light_pink = "#CDC9FA"
plot_blue_colour="#0810A6" #vibrant blue for plots


#to put everything into one page, to avoide scrolling:
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# 1- Layout settings

##Main Page
# Creating columns 1 and 2    -> This is for the main "page" not the side bar. 
col1, col2 = st.columns([13, 2])

## Header
col1.title('Zeta Oportunity Explorer: Demo')
"""This app is a demo project for ZMP's Oportunity Explorer dashboard"""

## Zeta Logo
#zeta_logo = Image.open('ZETA_BIG-99e027c9.webp') #white logo 
zeta_logo = Image.open('ZETA_BIG-99e027c92.png') #blue logo 
col2.image(zeta_logo)


# 1. Pie chart
match_rate = pd.DataFrame({"Field": ['Match Rate', 'Match Rate']
                                ,"Field metric": ['Matched to Data Cloud', 'Not Matched to Data Cloud']
                                ,"Percent" :[0.65, 0.35]
                                ,"Value": [65, 35]})

pie1 = alt.Chart(match_rate, title="Matched Rate" 
   ).encode(
    theta=alt.Theta("Value:Q", stack=True),
    color=alt.Color("Field metric:N"),
)
pie = pie1.mark_arc(outerRadius=110)
text = pie1.mark_text(radius=140, size=20,).encode(
    #theta= 
    text=alt.Text("Percent:Q", format='.0%' )
    ,color = alt.value("#0905AF")# sort=['OPENS','CLICKS']
) 

graph1= (pie+text)
#graph1= pie

st.text(" ")



# 2. Simple Bar chart
data_signal_matches = pd.DataFrame({"Field": ['Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches']
                                ,"Field metric": ['Transactional', 'Location', 'Behavioral', 'Professional', 'Credit Bureau']
                                ,"Percent" :[0.93, 0.87, 0.84, 0.96, 0.75  ]
                                ,"Value": [70, 65, 63, 72, 56]})

bars2 = alt.Chart(data_signal_matches, title= "Data Signal Matches"
).transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size = 70).encode(
alt.X('Field metric:N', axis=alt.Axis(labelAngle=0), title=None),
alt.Y('PercentOfTotal:Q', axis=None),
alt.Color("Field metric:N", )
).properties(
width=800 # controls width of bar.
, height=375  # height of the table
)
text2 = bars2.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-15, # Nudges text to right so it doesn't appear on top of the bar
    size =20
).encode(
    text= alt.Text('PercentOfTotal:Q', format ='.0%')
    ,color = alt.value("#0905AF")
)

graph2 = (bars2+text2)

# 3. Stacked Bar Chart with Text Overlay
source1=data.barley()
source1.loc[source1["site"] == "Crookston", "site"] = "Male"
source1.loc[source1["site"] == "Duluth", "site"] = "Male"
source1.loc[source1["site"] == "Grand Rapids", "site"] = "Male"
source1.loc[source1["site"] == "Morris", "site"] = "Female"
source1.loc[source1["site"] == "University Farm", "site"] = "Female"
source1.loc[source1["site"] == "Waseca", "site"] = "Female"
source1 = source1[(source1.variety.isin(['Svansota','Velvet', 'Glabron', 'Peatland']))]
source1.loc[source1["variety"] == "Svansota", "variety"] = "Customer site visitors"
source1.loc[source1["variety"] == "Velvet", "variety"] = "Customer non-site visitors"
source1.loc[source1["variety"] == "Glabron", "variety"] = "Zeta per. site visitors"
source1.loc[source1["variety"] == "Peatland", "variety"] = "Zeta non-per. site visitors"

bars3 = alt.Chart(source1, title= "Gender Index").mark_bar().encode(
    x=alt.X('sum(yield):Q', stack='zero', axis=None),
    y=alt.Y('variety:N', title=None),
    color=alt.Color('site')
)
text3 = alt.Chart(source1).mark_text(dx=-15, dy=1, color='black', size=18).encode(
    x=alt.X('sum(yield):Q', stack='zero',  title=None),
    y=alt.Y('variety:N' , axis=alt.Axis(labelLimit = 250)),
    detail='site:N',
    text=alt.Text('sum(yield):Q', format='.0f')
    ,color = alt.value("#0905AF")
)
graph3 = (bars3 + text3).properties(
width=800 # controls width of bar.
,height=375  # height of the table
)



# 4. Bar Chart with Rounded Edges
source = data.seattle_weather()
source['date'] = source['date'].dt.month
source.loc[source["date"] == 1, "date"] = "Automotive"
source.loc[source["date"] == 2, "date"] = "Business"
source.loc[source["date"] == 3, "date"] = "Education"
source.loc[source["date"] == 4, "date"] = "Entertainment"
source.loc[source["date"] == 5, "date"] = "Health"
source.loc[source["date"] == 6, "date"] = "Home"
source.loc[source["date"] == 7, "date"] = "Humanities"
source.loc[source["date"] == 8, "date"] = "Life Events"
source.loc[source["date"] == 9, "date"] = "Recreation"
source.loc[source["date"] == 10, "date"] = "Science"
source.loc[source["date"] == 11, "date"] = "Society"
source.loc[source["date"] == 12, "date"] = "Technology"
source = source[(source.weather.isin(['drizzle','fog', 'rain', 'sun']))]
source.loc[source["weather"] == "drizzle", "weather"] = "Q1"
source.loc[source["weather"] == "fog" , "weather"] = "Q2"
source.loc[source["weather"] ==  "rain" , "weather"] = "Q3"
source.loc[source["weather"] ==  "sun", "weather"] = "Q4"

bars4 = alt.Chart(source ,title= "Quarterly Categorical Comsumption").mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x=alt.X('date:N', axis=alt.Axis(labelAngle=-48), title=None),
    y= alt.Y('count():Q', axis=None),
    color=alt.Color('weather:N',legend=alt.Legend(title="Quarter") )
).properties(
width=900 # controls width of bar.
, height=375  # height of the table
)

graph4 = bars4

# 5. Streamgraph with Interactive Legend
abd = pd.read_csv('data_Interactive Charts.csv')
abd = abd[~abd.series.isin(["Agriculture","Information","Mining and Extraction"])]
abd.loc[abd["series"] == "Government", "series"] = "Apparel & Accesories" #
abd.loc[abd["series"] == "Construction", "series"] = "Automotive" #
abd.loc[abd["series"] == "Manufacturing", "series"] = "Consumer Services" #
abd.loc[abd["series"] == "Wholesale and Retail Trade", "series"] = "Entertainment"#
abd.loc[abd["series"] == "Transportation and Utilities", "series"] = "Food & Pharmacy" #
abd.loc[abd["series"] == "Finance", "series"] = "Home" #
abd.loc[abd["series"] == "Business services", "series"] = "Mass Retailers" #
abd.loc[abd["series"] == "Education and Health", "series"] = "Office, Electronics, Games" #
abd.loc[abd["series"] == "Leisure and hospitality", "series"] = "Restaurant" #
abd.loc[abd["series"] == "Other", "series"] = "Specialty Retail" #
abd.loc[abd["series"] == "Self-employed", "series"] = "Travel" #

#selection = alt.selection_point(fields=['series'], bind='legend')

stream5= alt.Chart(abd, title='Transactional Category').mark_area().encode(
    alt.X('yearmonth(date):T', axis=alt.Axis(domain=False, format='%Y', tickSize=0) , title=None),
    alt.Y('sum(count):Q', stack='center', axis=None),
    alt.Color('series:N', legend=None),
    #opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).properties(
width=800 # controls width of bar.
, height=500  # height of the table
).interactive()
#.add_params(
#    selection
#)

graph5 = stream5

# 6. 2D Histogram Scatter Plot
source = data.movies.url

hist6 =alt.Chart(source, title='Zeta-scores across Age and income Bands').mark_circle(color="#0905AF").encode(
    alt.X('income in 1K:Q', bin=True, title='Income' ),
    alt.Y('ages:Q', bin=True, title='Age intervals'),
    size='count()'
).properties(
width=800 # controls width of bar.
, height=500  # height of the table
)

graph6 =hist6 



# 7. Radial chart
source = pd.DataFrame({"values": [12, 23, 47, 6, 52, 19]})

base = alt.Chart(source, title="Radial chart").encode(
    theta=alt.Theta("values:Q", stack=True),
    radius=alt.Radius("values", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color=alt.Color("values:N", ),
)

c1 = base.mark_arc(innerRadius=20, stroke="#fff")

c2 = base.mark_text(radiusOffset=20, size=20, dx=8, dy=-5).encode(text="values:Q",  color = alt.value("#0905AF"))

graph7= (c1 + c2)


# 8. Simple Bar chart
match_breakdown = pd.DataFrame({"Field": ['Match Breakdown', 'Match Breakdown', 'Match Breakdown']
                                ,"Field metric": ["Email","Full Name + Full Postal", "Phone"]
                                ,"Percent" :[0.6, 0.5, 0.4]
                                ,"Value": [60, 50, 40]})
bars8 = alt.Chart(match_breakdown).mark_bar(size=70).encode(
        x= alt.X('Field metric:N',axis=alt.Axis(labelAngle=0) , title=None),
        y=alt.Y('Value:Q', axis=None),
        color= alt.Color("Field metric:N", )
        ).properties(
width=800 # controls width of bar.
, height=375  # height of the table
)
text8 = bars8.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-15, # Nudges text to right so it doesn't appear on top of the bar
    size = 20
).encode(
    text=alt.Text('Percent:Q', format='.0%')
    , color = alt.value("#0905AF")
)

graph8 = (bars8 +text8)

# 9. Hexbin chart
size =40
xFeaturesCount = 12
yFeaturesCount = 7
xField = 'date'
yField = 'date'

# the shape of a hexagon
hexagon = "M0,-2.3094010768L2,-1.1547005384 2,1.1547005384 0,2.3094010768 -2,1.1547005384 -2,-1.1547005384Z"

las_click_date =  pd.read_csv('tableau_data/las_click_date.csv')#, encoding='utf_16', sep = "\t" 

las_click_day =  pd.read_csv('tableau_data/las_click_day.csv')#, encoding='utf_16', sep = "\t" 

click_count =  pd.read_csv('tableau_data/click_count.csv')#, encoding='utf_16', sep = "\t" 

source = result = pd.concat([las_click_date, las_click_day,click_count ], axis=1)
source = source[['LAST_CLICK_DATE', 'LAST_CLICK_DAY', 'CLICK_COUNT']]
#source_h.columns = ["Month", "Day_of_the_week", "Nb_clicks"]
#source_h.rename(columns={'LAST_CLICK_DATE': 'Month', 'LAST_CLICK_DAY': 'Day_of_the_week', 'CLICK_COUNT': 'Nb_clicks'}, inplace=True)



#source["month_name"] = source["LAST_CLICK_DATE"].apply(lambda x: cal.month_name[x] )

##, labelExpr = ( " datum.LAST_CLICK_DATE == 1 ? 'Jan' : datum.LAST_CLICK_DATE == 2 ? 'Feb'     : datum.LAST_CLICK_DATE == 3 ? 'Mar'    : datum.LAST_CLICK_DATE == 4 ? 'Apr'    : datum.LAST_CLICK_DATE == 5 ? 'May'     : datum.LAST_CLICK_DATE == 6 ? 'Jun'     : datum.LAST_CLICK_DATE == 7 ? 'Jul' : datum.LAST_CLICK_DATE == 8 ? 'Aug'     : datum.LAST_CLICK_DATE == 9 ? 'Sep'     : datum.LAST_CLICK_DATE == 10 ? 'Oct'     : datum.LAST_CLICK_DATE == 11 ? 'Nov' :  'Dec' ")

hexbin= alt.Chart(source, title="Click Behavior of the Day across Months​").mark_point(size=size*(size/2), shape=hexagon).encode(
    x=alt.X('xFeaturePos:N', axis=alt.Axis(title='Month', grid=False, tickOpacity=10, domainOpacity=10 
                                           , values=(1, 2,3,4,5,6,7,8,9,10,11,12)
                                           ,labelAngle= 0)),
    y=alt.Y('LAST_CLICK_DAY:O', axis=alt.Axis(title='Day of the week', labelPadding=20, tickOpacity=0, domainOpacity=0)),
    #stroke=alt.value('black'),
    strokeWidth=alt.value(0.2),

    fill=alt.Color('mean(CLICK_COUNT):Q',  legend=alt.Legend(title='Average clicks')), #scale = 
    tooltip=['LAST_CLICK_DATE:O', 'LAST_CLICK_DAY:O', 'mean(CLICK_COUNT):Q']
).transform_calculate(
    # This field is required for the hexagonal X-Offset
    xFeaturePos='( datum.LAST_CLICK_DAY % 2) / 2 + datum.LAST_CLICK_DATE'
    
).properties(
    # Exact scaling factors to make the hexbins fit
    width=size * xFeaturesCount * 2,
    height=size * yFeaturesCount * 1.7320508076,  # 1.7320508076 is approx. sin(60°)*2
).configure_view(
    strokeWidth=0
)

graph9 = hexbin


#Stacked BARS -> category of Consumptions

# 10. Layered Area chart - Transactional categories from tableua  change the colomns "series" from eg data to the categories from transactional 
layer_df =pd.read_csv('tableau_data/Layered_graph.csv')

layered10 =alt.Chart(layer_df, title="Click and open distribution").mark_area().encode(
    x=alt.X("MONTH:O", axis = alt.Axis(labelAngle =0, title='Month'  )),
    y=alt.Y("sum(count):Q", axis=None, ),
    color=alt.Color("action:N",  sort=['OPENS','CLICKS'])
).properties(
    height=500 
    ,width= 900
)
graph10 = layered10

# 11. Predictions graph 
forecast = pd.read_csv('competitors.csv')
forecast = forecast.reset_index().melt('date', var_name='Company', value_name='Conversions')
forecast = forecast[~forecast.Company.isin(['index'])]

line_a=alt.Chart(forecast).mark_line().encode(
    x='yearmonth(date):T',
    y='mean(Conversions):Q',
    color='Company:N'
).transform_filter(
    alt.FieldOneOfPredicate(field='Company', oneOf=['Motel6', 'Motel6_pred'])
)


line_b = alt.Chart(forecast).mark_line().encode(
    x='yearmonth(date):T',
    y='mean(Conversions):Q',
    color='Company:N'
#).transform_filter(
#    alt.FieldOneOfPredicate(field='Company', oneOf=['Motel6', 'Motel6_pred'])
)

#######################

col1, col2 , col3 = st.columns([7,1,7])

with col1:
    st.header("  ")
    st.altair_chart(graph1, use_container_width=True)  
    st.header("  ")
    graph3
    st.header("  ")
    st.altair_chart(graph5, use_container_width=True)
    st.header("  ")
    st.altair_chart(graph7, use_container_width=True)
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    graph9
    #source_h
    st.header("  ")
    options = st.multiselect('Select your competitor',('Company', 'Competitor B'))

    if 'Competitor B' in options:
        line_b
    
    else:
        line_a

with col2:
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")
    st.header("  ")

with col3:
    st.header("  ")
    graph2
    st.header("  ")
    graph4
    st.header("  ")
    graph6
    st.header("  ")
    graph8  
    st.header("  ")
    st.altair_chart(graph10, use_container_width=True)
    st.header("  ")


 