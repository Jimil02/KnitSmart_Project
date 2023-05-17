import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
# from streamlit_echarts import st_echarts

st.set_page_config(page_title='Knitting Machines Analysis')
st.header('Knitting Machine Analysis: Maximizing Efficiency and Productivity')
st.subheader('Unlocking Insights and Optimizing Performance for Knitting Machines')

file = 'DataSet1.csv'
df = pd.read_csv(file)

machines = df['Device_id'].unique().tolist()

time_selection = st.slider('Time_Stamp(at minute):',
                        min_value= 1,
                        max_value= 156,
                        value=(1,156))

machine_selection = st.selectbox('Machines:',
                                    machines)

# --- FILTERING DATAFRAME BASED ON SELECTION
mask = (df['time_stamp'].between(*time_selection)) & (df['Device_id'] == machine_selection)
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

col1,col2 = st.columns([2,3])
image = Image.open('image02.jpg')
col1.image(image,
        caption='Image from knitsmart.in',
        use_column_width=True)
col2.dataframe(df[mask])

df_time_rpm = df[mask]
df_mask = df[mask]
# --- PLOT line CHART
fig = px.line(df_time_rpm, x="time_stamp", y="RPM", title='RPM of Machine '+str(machine_selection)+' at different time intervals', template= 'plotly_white')
st.plotly_chart(fig)
rpm = df_mask[['RPM']]
ot = df_mask[['On_time']]
oft = df_mask[['Off_time']]
max_rpm = rpm.max()
on_time_total = ot.max()
off_time_total = oft.max()
mode_rpm = rpm.mode()

with st.expander("Analysis for Machine "+str(machine_selection)+" for selected interval"):
    st.write("""
        Maximum *RPM* achieved:     """ +str(max_rpm[0]))
    st.write("""
        Total time machine was *on*:    """ +str(on_time_total[0])+" mins")
    st.write("""
        Total time machine was *off*:   """ +str(off_time_total[0])+" mins")
    st.write("""
        *RPM* achieved for longest period:  """+str(mode_rpm["RPM"].values[0]))

mask1 = (df['Device_id'] == machine_selection)

# df_time_rpm1 = df[mask1]
# fig1 = px.line(df_time_rpm1, x="time_stamp", y="On_time", title='RPM at different time intervals', template= 'plotly_white')
# fig1.add_scatter(x=df_time_rpm1['time_stamp'], y=df_time_rpm1['Off_time'])


df_mask1 = df[mask1]

fig1 = px.line(title='Time at which machine '+str(machine_selection)+' was "On" or "Off"', template= 'plotly_white')
fig1.add_trace(go.Scatter(x=df_mask1['time_stamp'], y=df_mask1['On_time'], name="On Time"))

# Change the name of the x-axis
fig1.update_xaxes(title_text="Time Stamp (at minute)")

# Change the name of the y-axis for On_time
fig1.update_yaxes(title_text="On/Off at minute")

# Add a scatter trace for Off_time
fig1.add_trace(go.Scatter(x=df_mask1['time_stamp'], y=df_mask1['Off_time'], name="Off Time"))
st.plotly_chart(fig1)

# col1, col2 = st.columns([5,1])

on_time_uni = df_mask1['On_time'].unique().tolist()
total_on_time = int(len(on_time_uni))
# st.markdown(total_on_time)
mu = float((total_on_time/156)*100)
mu = round(mu,2)

fig2 = go.Figure()
fig2.add_trace(go.Indicator(
                    mode = "gauge+number",
                    value=mu,
                    title={'text':'Machine '+str(machine_selection)+' Utilization in %'},
                    domain = {'row': 0, 'column': 0},
                    # number={'font_color':'red'},
                    gauge={'bar':{'color':'blue'}}
                ))
# st.plotly_chart(mu_fig)

# avg. RPM = total_rotation/total_on_time
tr = df_mask1[['Total_rotations']]
total_rotations = tr.max()
# st.markdown(total_rotations[0])
# st.markdown(total_on_time)
avg_rpm = float(total_rotations[0]/total_on_time)
avg_rpm = round(avg_rpm,2)
# avg_rpm_fig = go.Figure()
fig2.add_trace(go.Indicator(
                    mode = "gauge+number",
                    value=avg_rpm,
                    title={'text':'Machine '+str(machine_selection)+' Average RPM'},
                    domain = {'row': 0, 'column': 1},
                    # number={'font_color':'red'},
                    gauge={'bar':{'color':'green'}}
                ))

fig2.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"}
    )

st.plotly_chart(fig2)

with st.expander("Formulas used"):
    st.write("avg. RPM = total_rotation/total_on_time")
    st.write("machine_utilisation = (On_time / (On_time + Off_time)) * 100")

with st.expander("What we can interpret from above representations ?"):
    st.write("""*1.* Analyzing RPM and total rotations can help identify 
                peak production periods, measure the machine's productivity, and identify any deviations or abnormalities.
            """)
    st.write("""*2.* Comparing on_time and off_time can provide 
                insights into the machine's utilization and identify potential downtime or maintenance patterns.
            """)
    st.write("""*3.* Tracking time-based trends and patterns can help optimize scheduling, 
                identify bottlenecks, or plan maintenance activities.
            """)
    st.write("""*4.* We can also compare performance of different machines.
            """)