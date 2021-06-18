 #Academic Project done by Vinamra Bharadwaj and Saransh Raghav

#Importing necssary libraries
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
import imageio
import urllib.request as ulr
import os


#Adding title, cover picture and background color to the interface
st.title("COVID-19 DATA STATISTICS")
st.text("Based on COVID-19 Data Compiled by Oxford Martin School")
st.sidebar.title("COVID-19 Data Visualization")

imageurl = 'https://raw.githubusercontent.com/VinamraBharadwaj/COVID19WebApp/main/covidimage.jpg'
img = ulr.urlopen(imageurl)

image = Image.open(img)
st.image(image,use_column_width=True)
st.markdown('<style>body{background-color: black;}</style>',unsafe_allow_html=True)


#Importing and adding csv data to cache
@st.cache()
def long_running_function():
    return 1
covid_df = pd.read_csv(r'https://raw.githubusercontent.com/VinamraBharadwaj/COVID19WebApp/main/covidmaster.csv')


#Seperating World Data from compiled csv
world_csv = covid_df[covid_df['RegionID'] == 'World']
world_csv.reset_index(inplace = True)
world_csv = world_csv.rename(columns={"Country/Region":"Country"})


#Seperating World Data for latest data i.e. 29-May-21
graph_csv = world_csv[world_csv['Date'] == '29-May-21']
graph_csv.reset_index(inplace = True)
graph_csv = graph_csv.rename(columns={"Country/Region":"Country"})


#Seperating India Data from compiled csv
india_csv = covid_df[covid_df['RegionID'] == 'India']
india_csv.reset_index(inplace = True)
india_csv = india_csv.rename(columns={"Country/Region":"State"})


#Adding sections and headings for sidebar
st.sidebar.header("Let's Visualize!!")
st.sidebar.subheader("Visualization with Chart")
chart_selection = st.sidebar.selectbox("Choose the Chart Type", ['Pie Chart','Line Chart'], key=1)
select_status = st.sidebar.radio("Covid-19 patient's status", ('Confirmed Cases',
                                                               'Recovered Patients', 'Deaths'),key = 1)


#Adding section and setting up conditions using if-else
st.header("Visualization With Chart")
if not st.checkbox("Hide Chart Visualization", False):
    if chart_selection == 'Pie Chart':
        if select_status == 'Confirmed Cases':
            st.title("Total Confirmed Cases")
            fig = px.pie(graph_csv, values= graph_csv['Confirmed Cases'], names= graph_csv['Country'],
                            labels={'Confirmed Cases':'Confirmed Cases'})
            fig.update_traces(textposition='inside', textinfo='label')
            st.plotly_chart(fig)
        elif select_status == 'Recovered Patients':
            st.title("Total Recovered Cases")
            fig = px.pie(graph_csv, values= graph_csv['Recovered Patients'], names= graph_csv['Country'],
                            labels={'Recovered Patients':'Recovered Patients'})
            fig.update_traces(textposition='inside', textinfo='label')
            st.plotly_chart(fig)
        else: 
            st.title("Total Dead Cases")
            fig = px.pie(graph_csv, values= graph_csv['Deaths'], names= graph_csv['Country'],
                             labels={'Deaths':'Deaths'})
            fig.update_traces(textposition='inside', textinfo='label')
            st.plotly_chart(fig)
    elif chart_selection == 'Line Chart':
        if select_status == 'Confirmed Cases':
            st.title("Total Confirmed Population")
            fig = px.line(graph_csv, x= graph_csv['Country'], y= graph_csv['Confirmed Cases'])
            st.plotly_chart(fig)
        elif select_status == 'Recovered Patients':
            st.title("Total Recovered Cases")
            fig = px.line(graph_csv, x= graph_csv['Country'], y= graph_csv['Recovered Patients'])
            st.plotly_chart(fig)
        else: 
            st.title("Total Deceased Cases")
            fig = px.line(graph_csv, x = graph_csv['Country'], y = graph_csv['Deaths'])
            st.plotly_chart(fig)
        
        
#Adding section
st.sidebar.header("Bar Plot Visualization")
st.sidebar.checkbox("Bar Plot", False, key=2)
select = st.sidebar.selectbox("Select the Country",graph_csv['Country'].unique())

st.header("Bar Plot Visualization")
Country_data = graph_csv[graph_csv['Country'] == select]
def complete_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Status':['Confirmed Cases', 'Deaths', 'Recovered Patients'],
    'Number of Cases':(dataset.iloc[0]['Confirmed Cases'],
    dataset.iloc[0]['Deaths'], 
    dataset.iloc[0]['Recovered Patients'])})
    return total_dataframe

country_total = complete_dataframe(Country_data)

if not st.checkbox('Hide Bar Graph', False, key=2):
    st.markdown("### Overall Confirmed, Recovered and " +
    "Deceased Cases in %s yet" % (select))
    country_selection_graph = px.bar(country_total, x ='Status', y = "Number of Cases",
                                   labels = {'Number of Cases': 'Number of Cases in %s' %(select)}, color = 'Status')
    st.plotly_chart(country_selection_graph)

      
#Adding section for Visualizing Time Series Data of COVID-19 on Global Level 
st.sidebar.header("Map Animation")
st.sidebar.checkbox('Map Animation', True, key =3)
st.header("Map Animation")

if not st.checkbox('Hide Animation', False, key = 3):
    world_map = px.choropleth(world_csv, locations = 'Country',
                              color="New Confirmed Cases", animation_frame="Date",
                              color_continuous_scale="portland", locationmode='country names',
                              scope="world", range_color=(0,150000),
                              title='New Confirmed Cases of COVID-19',
                              height=600
                             )
    world_map.update_geos(showcountries=True, countrycolor="lightgrey",showland=True, landcolor="white",
                          showocean=True, oceancolor='lightblue')
    world_map.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    world_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.000000000000001
    world_map.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0.000000000000001
    st.plotly_chart(world_map)
    
    
#Adding section for Visualizing Time Series Data of COVID-19 on Global Level in a Virtual 3D Globe
st.sidebar.header("Globe Animation")
st.sidebar.checkbox('Globe Animation', True, key =4)
st.header("Globe Animation")  

if not st.checkbox('Hide Animation', False, key = 4):
    world_globe = px.choropleth(world_csv, locations = 'Country',
                              color="Deaths", animation_frame="Date",
                              color_continuous_scale="portland", locationmode='country names',
                              scope="world", range_color=(0,200000),
                              title='Total Deaths due to COVID-19',
                              height=600
                             )
    world_globe.update_geos(showcountries=True, countrycolor="lightgrey",showland=True, landcolor="white",
                            showocean=True, oceancolor='lightblue')
    world_globe.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    world_globe.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.000000000000001
    world_globe.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0.000000000000001
    world_globe.update_geos(projection_type="orthographic")
    st.plotly_chart(world_globe)
    

#Adding section for Visualizing Time Series Data of COVID-19 on Global Level in a Natural Earth Projection  
st.sidebar.header("Bubble Animation")
st.sidebar.checkbox('Bubble Animation', True, key =5)
st.header("Bubble Animation")  

if not st.checkbox('Hide Animation', False, key = 5):
    world_bubble = px.scatter_geo(world_csv, locations="Country", size="Confirmed Cases",
                                  title='Total Confirmed Cases of COVID-19 ', animation_frame="Date", 
                                  locationmode='country names', projection="natural earth", height = 600
                                 )
    world_bubble.update_geos(showcountries=True, countrycolor="lightgrey",showland=True, 
                             landcolor="white",showocean=True, oceancolor='lightblue')
    world_bubble.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    world_bubble.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.000000000000001
    world_bubble.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0.000000000000001
    st.plotly_chart(world_bubble)

    
#Code for making Animated GIF to show COVID-19 Time Series Data for India
#Commented out due to slow rendering process in the looped export
    
#response = ulr.urlopen('https://raw.github.com/VinamraBharadwaj/COVID19WebApp/main/india.geojson')
#india_ds = json.loads(response.read())

#m = {}
#for f in india_ds['features']:
#    f['id'] = f['properties']['st_nm']
#    m[f['properties']['st_nm']] = f['id']
#
#warnings.filterwarnings("ignore")
#india_csv['id'] = india_csv['Country/Region'].apply(lambda x: m[x])

#lst = list(set(india_csv['DateCode']))
#lst.sort()

#for j in lst:
    
#    ds = india_csv[india_csv['DateCode'] == j]
#    ds.reset_index(inplace = True)
    
#    mapc = px.choropleth(ds, title='Active COVID-19 Cases as of '+ ds['Date'][0], locations = 'Country/Region',
#                         geojson = india_ds,color = 'Active Cases', color_continuous_scale = "portland", 
#                         range_color = (0,150000), fitbounds='geojson')
#    mapc.update_geos(visible=False)
#    mapc.write_image('D:/COVID19'+str(j)+'VS.png')


#export_dir = 'D:/'
#images = []
#for fn in sorted(os.listdir(export_dir)):
#    if fn.endswith('VS.png'):
#        file_path = os.path.join(export_dir, fn)
#        images.append(imageio.imread(file_path))
#
#gif_india = (export_dir + '/COVID-19 India.gif')
#imageio.mimsave(gif_india, images, duration  = 0.7)



#Adding section to show COVID-19 Time Series Data for India as an Animated GIF
st.sidebar.header("GIF Animation - India")
st.sidebar.checkbox('GIF Animation - India', True, key =6)
st.header("GIF Animation - India")

if not st.checkbox('Hide Animation', False, key = 6):
    st.markdown("![Alt Text](https://raw.githubusercontent.com/VinamraBharadwaj/COVID19WebApp/main/COVID_India.gif)")
