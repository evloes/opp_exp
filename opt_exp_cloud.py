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


#Pie chart 1 - Match rate

#match_rate = pd.read_csv('tableau_data/Match Rate.csv', encoding='utf_16', sep = "\t" )
match_rate = pd.DataFrame({"Field": ['Match Rate', 'Match Rate']
                                ,"Field metric": ['Matched to Data Cloud', 'Not Matched to Data Cloud']
                                ,"Percent" :[0.65, 0.35]
                                ,"Value": [65, 35]})

pie1 = alt.Chart(match_rate).encode(
    theta=alt.Theta("Value:Q", stack=True),
    color=alt.Color("Field metric:N", legend=None, scale=alt.Scale(scheme='set1')),
)
pie = pie1.mark_arc(outerRadius=120)
text = pie1.mark_text(radius=215, size=20).encode(
    text="Field metric:N"
)
#text_2 = pie1.mark_text(radius=50, size=15).encode(
#    text= alt.Text("Value:Q" , format ='.0%' , color= 'black') )


#Bar 1 - Match Breakdown
#match_breakdown = pd.read_csv('tableau_data/Match Breakdown.csv', encoding='utf_16', sep = "\t" )
match_breakdown = pd.DataFrame({"Field": ['Match Breakdown', 'Match Breakdown', 'Match Breakdown']
                                ,"Field metric": ["Email","Full Name + Full Postal", "Phone"]
                                ,"Percent" :[0.6, 0.5, 0.4]
                                ,"Value": [60, 50, 40]})
bars1 = alt.Chart(match_breakdown).mark_bar(size=70).encode(
        x= alt.X('Field metric:N',axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Value:Q', axis=alt.Axis(title='Match Count')),
        color= alt.Color("Field metric:N", legend = None, scale=alt.Scale(scheme='accent'))
        ).properties(
    width=alt.Step(200) # size controls width of bar. and width allocates for each bar in the chart the width
    #, height=500  # height of the table
)
text1 = bars1.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-10, # Nudges text to right so it doesn't appear on top of the bar
    size = 20
).encode(
    text='Value:Q'
)


#Bar 2 - Data Signal Matches
#data_signal_matches	= pd.read_csv('tableau_data/Data Signal Matches.csv', encoding='utf_16', sep = "\t" )
data_signal_matches = pd.DataFrame({"Field": ['Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches', 'Data Signal Matches']
                                ,"Field metric": ['Transactional', 'Location', 'Behavioral', 'Professional', 'Credit Bureau']
                                ,"Percent" :[0.93, 0.87, 0.84, 0.96, 0.75  ]
                                ,"Value": [70, 65, 63, 72, 56]})

bars2 = alt.Chart(data_signal_matches).transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size = 70).encode(
alt.X('Field metric:N', axis=alt.Axis(labelAngle=0)),
alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%', title='Match Count')),
alt.Color("Field metric:N", legend=None, scale=alt.Scale(scheme='category10'))
).properties(
width=alt.Step(150) # controls width of bar.
    #, height=500  # height of the table
        
)
text2 = bars2.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-10, # Nudges text to right so it doesn't appear on top of the bar
    size =20
).encode(
    alt.Text('PercentOfTotal:Q',
    format ='.0%')
)

#Bar 3 - Omni-channel  Reach
#omni_channel_reach = pd.read_csv('tableau_data/Omni-Channel Reach.csv', encoding='utf_16', sep = "\t" )
omni_channel_reach = pd.DataFrame({"Field": ['omni-chnnel','omni-chnnel', 'omni-chnnel' , 'omni-chnnel']
                                   ,"Field metric": ['Email', 'Programmatic', 'Social', 'Direct Mail']
                                   , "Value": [40, 50, 30, 20] 
                                   , 'Percent' :[0.4,0.5,0.3,0.2]})


#Bars
bars3 = alt.Chart(omni_channel_reach).transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size=70).encode(
alt.X('Field metric:N', axis=alt.Axis(labelAngle=0)),
alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%', title='Match Count')),
alt.Color("Field metric:N", legend=None, scale=alt.Scale(scheme='set1'))

).properties(
width=alt.Step(170) # controls width of bar.
    #, height=500  # height of the table
        
)
text3 = bars3.mark_text(
    align='center',
    baseline='middle',
    dx=0,dy=-10, # Nudges text to right so it doesn't appear on top of the bar
    size =20
).encode(
    alt.Text('PercentOfTotal:Q',
    format ='.0%')
)

#Radial chart
base2 = alt.Chart(omni_channel_reach).encode(
    theta=alt.Theta("Value:Q", stack=True),
    radius=alt.Radius("Value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color= alt.Color("Field metric:N")
)

c2 = base2.mark_arc(innerRadius=20, stroke="#fff")

c3 = base2.mark_text(radiusOffset=50, size=25).encode(alt.Text ("Percent:Q", format ='.0%'))



#Bar 4 - Email Coverage 
email_coverage = pd.read_csv('tableau_data/Email Coverage.csv', encoding='utf_16', sep = "\t"
                            ,names=['Universe', 'Type', 'Percent', 'Value']
                            , header=0 )

bars4=alt.Chart().transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size=45).encode(
    x=alt.X('PercentOfTotal:Q',stack='zero', axis=alt.Axis(format='.0%')),
    y=alt.Y('Universe:N', axis=alt.Axis(title=None)),
    color=alt.Color('Type:N',  scale=alt.Scale(scheme='dark2')
    ,legend=alt.Legend(
        orient='none',
        legendX=0, legendY=-33,
        direction='horizontal',
        titleAnchor='middle'))
).properties(
width=1000#alt.Step(1000) 
,height = 300
)

text4=alt.Chart().mark_text( dx=-15, dy=3 , color='black').encode(
    y=alt.Y('Universe:N'),
    x=alt.X('PercentOfTotal:Q',  stack='zero'),
    color=alt.Color('Type:N') ,
    text=alt.Text('Type:N')#,format='.0%')
)

#Bar 5 - Programmatic Coverage
prog_cove =  pd.read_csv('tableau_data/Programmatic Coverage.csv', encoding='utf_16', sep = "\t" 
                        ,names=['Channel', 'Type', 'Percent', 'Value']
                        , header=0 )

bars5=alt.Chart().transform_joinaggregate(
    TotalValue='sum(Value)',
).transform_calculate(
    PercentOfTotal="datum.Value / datum.TotalValue"
).mark_bar(size=45).encode(
    x=alt.X('PercentOfTotal:Q',stack='zero', axis=alt.Axis(format='.0%')),
    y=alt.Y('Channel:N', axis=alt.Axis(title=None)),
    color=alt.Color('Type:N',  scale=alt.Scale(scheme='viridis')
    ,legend=alt.Legend(
        orient='none',
        legendX=0, legendY=-33,
        direction='horizontal',
        titleAnchor='middle'))
).properties(
width=1020#width=alt.Step(1000) 
,height = 300
)

text5=alt.Chart().mark_text( dx=-15, dy=3 , color='black').encode(
    y=alt.Y('Channel:N'),
    x=alt.X('PercentOfTotal:Q',  stack='zero'),
    color=alt.Color('Type:N') ,
    text=alt.Text('Type:N')#,format='.0%')
)

##Fake graphs

#Hexbin Chart


size =45
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
source["month_name"] = source["LAST_CLICK_DATE"].apply(lambda x: cal.month_name[x] )
axis_labels = ( " datum.LAST_CLICK_DATE == 1.0 ? 'Jan' : datum.LAST_CLICK_DATE == 2.0 ? 'Feb'     : datum.LAST_CLICK_DATE == 3.0 ? 'Mar'    : datum.LAST_CLICK_DATE == 4.0 ? 'Apr'    : datum.LAST_CLICK_DATE == 5.0 ? 'May'     : datum.LAST_CLICK_DATE == 6.0 ? 'Jun'     : datum.LAST_CLICK_DATE == 7.0 ? 'Jul' : datum.LAST_CLICK_DATE == 8.0 ? 'Aug'     : datum.LAST_CLICK_DATE == 9.0 ? 'Sep'     : datum.LAST_CLICK_DATE == 10.0 ? 'Oct'     : datum.LAST_CLICK_DATE == 11.0 ? 'Nov' :  'Dec' ")


hexbin= alt.Chart(source).mark_point(size=size*(size/2), shape=hexagon).encode(
    x=alt.X('xFeaturePos:Q', axis=alt.Axis(title='Month', grid=False, tickOpacity=0, domainOpacity=0, labelExpr = axis_labels )),
    y=alt.Y('LAST_CLICK_DAY:O', axis=alt.Axis(title='Day of the week', labelPadding=20, tickOpacity=0, domainOpacity=0)),
    stroke=alt.value('black'),
    strokeWidth=alt.value(0.2),
    fill=alt.Color('mean(CLICK_COUNT):Q', scale=alt.Scale(scheme='darkblue')),
    tooltip=['month_name:O', 'LAST_CLICK_DAY:O', 'mean(CLICK_COUNT):Q']
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



#Heatmap
x, y = np.meshgrid(range(-5, 5), range(-5, 5))
z = x ** 2 + y ** 2

source = pd.DataFrame({'x': x.ravel(),
                     'y': y.ravel(),
                     'z': z.ravel()})

heat = alt.Chart(source).mark_rect().encode(
    x='x:O',
    y='y:O',
    color=alt.Color('z:Q')
).properties(
    height=400 
    , width = 800
)


#Diverging Stacked Bar Chart
source = alt.pd.DataFrame([
      {"question": "Question 1",        "type": "Strongly disagree",        "value": 24,        "percentage": 0.7,        "percentage_start": -19.1,        "percentage_end": -18.4      },
      {        "question": "Question 1",        "type": "Disagree",        "value": 294,        "percentage": 9.1,        "percentage_start": -18.4,        "percentage_end": -9.2      },
      {        "question": "Question 1",        "type": "Neither agree nor disagree",        "value": 594,        "percentage": 18.5,        "percentage_start": -9.2,        "percentage_end": 9.2      },
      {        "question": "Question 1",        "type": "Agree",        "value": 1927,        "percentage": 59.9,        "percentage_start": 9.2,        "percentage_end": 69.2      },
      {        "question": "Question 1",        "type": "Strongly agree",        "value": 376,        "percentage": 11.7,        "percentage_start": 69.2,        "percentage_end": 80.9      },
      {        "question": "Question 2",        "type": "Strongly disagree",        "value": 2,        "percentage": 18.2,        "percentage_start": -36.4,        "percentage_end": -18.2      },
      {        "question": "Question 2",        "type": "Disagree",        "value": 2,        "percentage": 18.2,        "percentage_start": -18.2,        "percentage_end": 0      },
      {        "question": "Question 2",        "type": "Neither agree nor disagree",        "value": 0,        "percentage": 0,        "percentage_start": 0,        "percentage_end": 0      },
      {        "question": "Question 2",        "type": "Agree",        "value": 7,        "percentage": 63.6,        "percentage_start": 0,        "percentage_end": 63.6      },
      {        "question": "Question 2",        "type": "Strongly agree",        "value": 11,        "percentage": 0,        "percentage_start": 63.6,        "percentage_end": 63.6      },
      {        "question": "Question 3",        "type": "Strongly disagree",        "value": 2,        "percentage": 20,        "percentage_start": -30,        "percentage_end": -10      },
      {        "question": "Question 3",        "type": "Disagree",        "value": 0,        "percentage": 0,        "percentage_start": -10,        "percentage_end": -10      },
      {
        "question": "Question 3",
        "type": "Neither agree nor disagree",
        "value": 2,
        "percentage": 20,
        "percentage_start": -10,
        "percentage_end": 10
      },
      {
        "question": "Question 3",
        "type": "Agree",
        "value": 4,
        "percentage": 40,
        "percentage_start": 10,
        "percentage_end": 50
      },
      {
        "question": "Question 3",
        "type": "Strongly agree",
        "value": 2,
        "percentage": 20,
        "percentage_start": 50,
        "percentage_end": 70
      },

      {
        "question": "Question 4",
        "type": "Strongly disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": -15.6,
        "percentage_end": -15.6
      },
      {
        "question": "Question 4",
        "type": "Disagree",
        "value": 2,
        "percentage": 12.5,
        "percentage_start": -15.6,
        "percentage_end": -3.1
      },
      {
        "question": "Question 4",
        "type": "Neither agree nor disagree",
        "value": 1,
        "percentage": 6.3,
        "percentage_start": -3.1,
        "percentage_end": 3.1
      },
      {
        "question": "Question 4",
        "type": "Agree",
        "value": 7,
        "percentage": 43.8,
        "percentage_start": 3.1,
        "percentage_end": 46.9
      },
      {
        "question": "Question 4",
        "type": "Strongly agree",
        "value": 6,
        "percentage": 37.5,
        "percentage_start": 46.9,
        "percentage_end": 84.4
      },

      {
        "question": "Question 5",
        "type": "Strongly disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": -10.4,
        "percentage_end": -10.4
      },
      {
        "question": "Question 5",
        "type": "Disagree",
        "value": 1,
        "percentage": 4.2,
        "percentage_start": -10.4,
        "percentage_end": -6.3
      },
      {
        "question": "Question 5",
        "type": "Neither agree nor disagree",
        "value": 3,
        "percentage": 12.5,
        "percentage_start": -6.3,
        "percentage_end": 6.3
      },
      {
        "question": "Question 5",
        "type": "Agree",
        "value": 16,
        "percentage": 66.7,
        "percentage_start": 6.3,
        "percentage_end": 72.9
      },
      {
        "question": "Question 5",
        "type": "Strongly agree",
        "value": 4,
        "percentage": 16.7,
        "percentage_start": 72.9,
        "percentage_end": 89.6
      },

      {
        "question": "Question 6",
        "type": "Strongly disagree",
        "value": 1,
        "percentage": 6.3,
        "percentage_start": -18.8,
        "percentage_end": -12.5
      },
      {
        "question": "Question 6",
        "type": "Disagree",
        "value": 1,
        "percentage": 6.3,
        "percentage_start": -12.5,
        "percentage_end": -6.3
      },
      {
        "question": "Question 6",
        "type": "Neither agree nor disagree",
        "value": 2,
        "percentage": 12.5,
        "percentage_start": -6.3,
        "percentage_end": 6.3
      },
      {
        "question": "Question 6",
        "type": "Agree",
        "value": 9,
        "percentage": 56.3,
        "percentage_start": 6.3,
        "percentage_end": 62.5
      },
      {
        "question": "Question 6",
        "type": "Strongly agree",
        "value": 3,
        "percentage": 18.8,
        "percentage_start": 62.5,
        "percentage_end": 81.3
      },

      {
        "question": "Question 7",
        "type": "Strongly disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": -10,
        "percentage_end": -10
      },
      {
        "question": "Question 7",
        "type": "Disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": -10,
        "percentage_end": -10
      },
      {
        "question": "Question 7",
        "type": "Neither agree nor disagree",
        "value": 1,
        "percentage": 20,
        "percentage_start": -10,
        "percentage_end": 10
      },
      {
        "question": "Question 7",
        "type": "Agree",
        "value": 4,
        "percentage": 80,
        "percentage_start": 10,
        "percentage_end": 90
      },
      {
        "question": "Question 7",
        "type": "Strongly agree",
        "value": 0,
        "percentage": 0,
        "percentage_start": 90,
        "percentage_end": 90
      },

      {
        "question": "Question 8",
        "type": "Strongly disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Question 8",
        "type": "Disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Question 8",
        "type": "Neither agree nor disagree",
        "value": 0,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Question 8",
        "type": "Agree",
        "value": 0,
        "percentage": 0,
        "percentage_start": 0,
        "percentage_end": 0
      },
      {
        "question": "Question 8",
        "type": "Strongly agree",
        "value": 2,
        "percentage": 100,
        "percentage_start": 0,
        "percentage_end": 100
      }
])

color_scale = alt.Scale(
    domain=[
        "Strongly disagree",
        "Disagree",
        "Neither agree nor disagree",
        "Agree",
        "Strongly agree"
    ],
    range=["#c30d24", "#f3a583", "#cccccc", "#94c6da", "#1770ab"]
)

y_axis = alt.Axis(
    title='Question',
    offset=5,
    ticks=False,
    minExtent=60,
    domain=False
)

divergin= alt.Chart(source).mark_bar().encode(
    x='percentage_start:Q',
    x2='percentage_end:Q',
    y=alt.Y('question:N', axis=y_axis),
    color=alt.Color(
        'type:N',
        legend=alt.Legend( title='Response')
    ,scale=color_scale)

).properties(
    height=400 
    , width =1000
)
 
#Trellis 
source = data.iowa_electricity()

trellis= alt.Chart(source).mark_area().encode(
    x="year:T",
    y="net_generation:Q",
    color="source:N",
    row="source:N"
).properties(
    height=80
    , width = 80
)

#Layered
source = data.iowa_electricity()

layered=alt.Chart(source).mark_area(opacity=0.3).encode(
    x="year:T",
    y=alt.Y("net_generation:Q", stack=None),
    color=alt.Color("source:N", legend=alt.Legend(
        orient='none',
        legendX=0, legendY=-33,
        direction='horizontal',
        titleAnchor='middle'))
).properties(
    height=400 
    ,width= 1000
)

#Scatterd 
source = data.iris()

scatered=alt.Chart(source).mark_circle().encode(
    alt.X('sepalLength', scale=alt.Scale(zero=False)),
    alt.Y('sepalWidth', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color('species')
    ,size='petalWidth'
).properties(
    height=400 
    ,width=900
)

#2D scattered
source = data.movies.url

s2d =alt.Chart(source).mark_circle().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    size=alt.Size('count()')
).properties(
    height=400 
    ,width=900
)


#Mosaic
source = data.cars()

base = (
    alt.Chart(source)
    .transform_aggregate(count_="count()", groupby=["Origin", "Cylinders"])
    .transform_stack(
        stack="count_",
        as_=["stack_count_Origin1", "stack_count_Origin2"],
        offset="normalize",
        sort=[alt.SortField("Origin", "ascending")],
        groupby=[],
    )
    .transform_window(
        x="min(stack_count_Origin1)",
        x2="max(stack_count_Origin2)",
        rank_Cylinders="dense_rank()",
        distinct_Cylinders="distinct(Cylinders)",
        groupby=["Origin"],
        frame=[None, None],
        sort=[alt.SortField("Cylinders", "ascending")],
    )
    .transform_window(
        rank_Origin="dense_rank()",
        frame=[None, None],
        sort=[alt.SortField("Origin", "ascending")],
    )
    .transform_stack(
        stack="count_",
        groupby=["Origin"],
        as_=["y", "y2"],
        offset="normalize",
        sort=[alt.SortField("Cylinders", "ascending")],
    )
    .transform_calculate(
        ny="datum.y + (datum.rank_Cylinders - 1) * datum.distinct_Cylinders * 0.01 / 3",
        ny2="datum.y2 + (datum.rank_Cylinders - 1) * datum.distinct_Cylinders * 0.01 / 3",
        nx="datum.x + (datum.rank_Origin - 1) * 0.01",
        nx2="datum.x2 + (datum.rank_Origin - 1) * 0.01",
        xc="(datum.nx+datum.nx2)/2",
        yc="(datum.ny+datum.ny2)/2",
    )
)


rect = base.mark_rect().encode(
    x=alt.X("nx:Q", axis=None),
    x2="nx2",
    y="ny:Q",
    y2="ny2",
    color=alt.Color("Origin:N", legend=None),
    opacity=alt.Opacity("Cylinders:Q", legend=None),
    tooltip=["Origin:N", "Cylinders:Q"],
)


textc = base.mark_text(baseline="middle").encode(
    x=alt.X("xc:Q", axis=None), y=alt.Y("yc:Q", title="Cylinders"), text="Cylinders:N"
)


mosaic = rect + textc

origin_labels = base.mark_text(baseline="middle", align="center").encode(
    x=alt.X(
        "min(xc):Q",
        axis=alt.Axis(title="Origin", orient="top"),
    ),
    color=alt.Color("Origin", legend=None),
    text="Origin",
)



font_css = """<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 24px;
}
</style>
"""

st.write(font_css, unsafe_allow_html=True)

#Option 2
tab1, tab2, tab3,tab4, tab5, tab6 = st.tabs(["Overall Coverage Analysis", "Email Match Analysis", "Direct Mail Match Analysis", "Example tab 1", "Example tab 2", "Example tab 3"])

with tab1:
   
    col1, col2= st.columns(2)
    with col1:
        #match rate
        st.text('match rate')
        st.altair_chart((pie+text), use_container_width=True)

    with col2:
        #match breakdown
        #data signal matches
        st.text('match breakdown')
        st.altair_chart((bars1 + text1), use_container_width=True)
        #st.pyplot(fig)  #, figsize=(4, 4))
        st.text('data signal matches')
        st.altair_chart((bars2 + text2), use_container_width=True)


with tab2:
    cols= st.columns([1,1,1,1,1,1,1,1,1,1,1])
    with cols[2]:
       st.text('omni-channel reach - Radial graph')
       st.altair_chart((c2 + c3))#,theme= "streamlit", use_container_width=True) 
    with cols[5]:
        st.text('Layered Area Chart')
        st.altair_chart(layered)
       
    


with tab3:
    
    cols= st.columns([1,1,1,1,1,1,1,1,1,1,1])
    with cols[0]:
        #st.selectbox("City", ["City1", "City2"])
        #st.text('Trellis Area Chart')
        #st.altair_chart(trellis, theme= "streamlit", use_container_width=True)
        st.text('Divergin')
        st.altair_chart(divergin, theme= "streamlit")
    with cols[6]:
        #st.selectbox("District", ["District1", "District2"])
        st.text('Heat Map')
        st.altair_chart(heat, theme= "streamlit")
        
        
    
        

with tab4:
    cols= st.columns([1,1,1,1,1,1,1,1,1,1,1])
    with cols[0]:
        #omni-channel reavh
        #email coverage
        #programmatic coverage
        st.text('omni-channel reach')
        st.altair_chart((bars3 + text3))#, use_container_width=True)
        
    with cols[5]:
        st.text('email coverage')
        st.altair_chart(alt.layer(bars4, text4, data=email_coverage))#, theme= "streamlit", use_container_width=True)
        st.text('programmatic coverage')
        st.altair_chart(alt.layer(bars5, text5, data=prog_cove))#, theme= "streamlit", use_container_width=True)



with tab5:
    cols = st.columns([1,1,1,1,1,1,1,1,1,1,1])
    with cols[0]:
        st.text('Multifeature Scatter Plot')
        st.altair_chart(scatered)#, theme= "streamlit", use_container_width=True)
        

    
    with cols[6]:
        
        #st.text('Mosaic Chart')
        #((origin_labels & mosaic).resolve_scale(x="shared").configure_view(stroke="").configure_concat(spacing=10).configure_axis(domain=False, ticks=False, labels=False, grid=False))
        st.text("2D Histogram Scatter Plot")
        st.altair_chart(s2d)#, theme= "streamlit", use_container_width=True)

with tab6:
    cols= st.columns([1,1])
    with cols[0]:
        st.text('Hexbin Chart')
        st.altair_chart(hexbin)# , use_container_width=True)#, theme= "streamlit", use_container_width=True)
