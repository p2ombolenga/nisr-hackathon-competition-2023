import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="RWANDA LABOR FORCE SURVEY ANALYSIS", page_icon=":briefcase:", layout="wide")

# Replace the file path with your actual path, and make sure to wrap it in double quotes.
# excel_file_path = r'C:\Users\CARDX LTD\Desktop\NISR COMPETITION\RLFS Tables_ Annual_2022.xlsx'

# Create a Pandas ExcelFile object to access the sheets in the Excel file.
# xls = pd.ExcelFile(excel_file_path)

# List all sheet names in the Excel file.
# sheet_names = xls.sheet_names
@st.cache_data
def get_data_from_excel():
    # Read data from a specific sheet (e.g., 'Sheet1') into a DataFrame.

    # SHEET TABLE 13-14
    dataframe1 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 13-14', 
        skiprows=1,
        usecols='A:I',
        nrows=6)


    dataframe2 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 4-5', 
        skiprows=11,
        usecols='A:H',
        nrows=7)

    dataframe3 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 6-7', 
        skiprows=8,
        usecols='A:H',
        nrows=6)

    dataframe4 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 15-16 ', 
        skiprows=21,
        usecols='A:H',
        nrows=10)


    # DATA FRAME FOR EMPLOYES AND Duration Employement Contract
    dataframe5 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 22-23-24', 
        skiprows=26,
        usecols='A:H',
        nrows=9)

    # UNMPLOYED PEOPLE BY AGE GROUP,SEX,GENDER AND AREA OF RESIDENCE
    dataframe6 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 38-39', 
        skiprows=1,
        usecols='A:H',
        nrows=7)
    # UNMPLOYED PEOPLE BY LEVEL OF EDUCATION,SEX,GENDER AND AREA OF RESIDENCE
    dataframe7 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 38-39', 
        skiprows=10,
        usecols='A:H',
        nrows=7)
    # UNMPLOYED PEOPLE BY DURATION OF SEEKING EMPLOYMENT,SEX,GENDER AND AREA OF RESIDENCE
    dataframe8 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 40-41', 
        skiprows=19,
        usecols='A:H',
        nrows=7)

    dataframe9 = pd.read_excel(
        io='RLFS Tables_ Annual_2022.xlsx',
        engine='openpyxl', 
        sheet_name='Table 53', 
        skiprows=1,
        usecols='A:J',
        nrows=36)
    return [
        dataframe1,
        dataframe2,
        dataframe3,
        dataframe4,
        dataframe5,
        dataframe6,
        dataframe7,
        dataframe8,
        dataframe9
        ]

dataframe1,dataframe2,dataframe3,dataframe4,dataframe5,dataframe6,dataframe7,dataframe8,dataframe9 = get_data_from_excel()
# Define the provinces
provinces = ['City of Kigali', 'South province', 'West Province', 'North Province', 'East province ']

# Create two separate DataFrames for provinces and districts
dataset_provinces = dataframe9[dataframe9['Area'].isin(provinces)]
dataset_districts = dataframe9[~dataframe9['Area'].isin(provinces)]

# data1 = population_education.iloc[:, :]
# data2 = df_sheet2.iloc[:, 3:]

# st.dataframe(population_education)

st.sidebar.header("Apply Filters: ")
st.sidebar.subheader("All Working Age Population 16+ :")
# Get unique education options excluding "Population 16 yrs and over"
education_options = dataframe1["Education"].unique()
education_options = [edu for edu in education_options if edu != "Population 16 yrs and over"]

# Multiselect with the filtered options
education = st.sidebar.multiselect(
    "Select Level Of Education:",
    options=education_options,
    default=education_options  # You can set a default selection if needed
)


# dataframe 1
data1_selection = dataframe1.query("Education == @education")
# dataframe 3
data3_selection = dataframe3.query("Education == @education")
# DISPLAY DATASET AFTER SELECTION BY DEFAULT ALL OPTIONS ARE SELECTED
# st.dataframe(data1_selection)


# ------------ MAIN PAGE -------------------

st.subheader(":briefcase: RWANDA LABOR FORCE 2022 DASHBOARD")
st.markdown("##")
st.write("OverView For All Working Age Population 16+")

# OVERVIEW KPI'S

working_age_population = 0
labor_force = 0
employed = 0
un_employed = 0
outside_labour_force = 0
average_employment_rate = 0
average_unemployment_rate = 0
# Calculate the average unemployment rate
if len(education) > 0:
    working_age_population = int(data1_selection['Total'].sum())
    labor_force = int(data1_selection['Labour force'].sum())
    employed = int(data1_selection['Employed'].sum())
    un_employed = int(data1_selection['Unemployed'].sum())
    outside_labour_force = int(data1_selection['Outside labour force'].sum())
    average_employment_to_population = data1_selection['Employment-to population ratio'].mean()
    average_unemployment_rate = data1_selection['Unemployment rate'].mean()

    column_one,column_two,column_three,column_four, column_five,column_six = st.columns(6)

    with column_one:
        st.write("Age 16+ Population")
        st.subheader(f"{working_age_population:,}")
    with column_two:
        st.write("Labour Force")
        st.subheader(f"{labor_force:,}")
    with column_three:
        st.write("Employed")
        st.subheader(f"{employed:,}")
    with column_four:
        st.write("Unemployed")
        st.subheader(f"{un_employed:,}")
    with column_five:
        st.write("Employement To Population")
        st.subheader(f"{average_employment_to_population:.1f}%")
    with column_six:
        st.write("Unemployement Rate")
        st.subheader(f"{average_unemployment_rate:.1f}%")
else:
    st.warning("Select A level of Education to view Overview Of Rwanda Labour Force Data")


# Calculate sums
total_male = data3_selection['Male'].sum()
total_female = data3_selection['Female'].sum()
total_urban = data3_selection['Urban'].sum()
total_rural = data3_selection['Rural'].sum()
total_participated = data3_selection['Participated in  subsistence agriculture'].sum()
total_not_participated = data3_selection['Not participated in subsistence agriculture'].sum()


pie_gender, pie_residence, pie_agriculture = st.columns(3)

if len(education) > 0:

    with pie_gender:
        # Pie chart for Gender distribution
        fig_gender = px.pie(names=['Male', 'Female'], values=[total_male, total_female], title='Gender')
        fig_gender.update_layout(height=300, width=300)
        st.plotly_chart(fig_gender)
    with pie_residence:
        # Pie chart for Area of residence distribution
        fig_location = px.pie(names=['Urban', 'Rural'], values=[total_urban, total_rural], title='Area Of Residence')
        fig_location.update_layout(height=300, width=300)
        st.plotly_chart(fig_location)
    with pie_agriculture:
        # Pie chart for Participation in subsistence agriculture
        fig_agriculture = px.pie(names=['Participated', 'Not Participated'], values=[total_participated, total_not_participated], title='Participation in Subsistence Agriculture')
        fig_agriculture.update_layout(height=300, width=300)
        st.plotly_chart(fig_agriculture)

else:
    pass


# Exclude 'Disabled Working Age Persons (16+ yrs)'
dataframe2_filtered = dataframe2[dataframe2['Type of disability'] != 'Disabled working age persons (16+ yrs)']

# Get user input for employment status
selected_status = st.sidebar.radio("Filter Disabled working age persons (16+ yrs) By:", ["All", "Employed", "Unemployed", "Unemployment Rate", "Outside labour force", "Employment Rate", "Labour Force Participation Rate"])

# Filter the DataFrame based on the selected status
if selected_status == "Employed":
    df_filtered = dataframe2_filtered[['Type of disability', 'Employed']]
    title = 'Employed Disabled working age persons'
elif selected_status == "Unemployed":
    df_filtered = dataframe2_filtered[['Type of disability', 'Unemployed']]
    title = 'Unemployed Disabled working age persons'
elif selected_status == "Unemployment Rate":
    df_filtered = dataframe2_filtered[['Type of disability', 'UR']]
    title = 'Unemployment Rate In Disabled working age persons'
elif selected_status == "Outside labour force":
    df_filtered = dataframe2_filtered[['Type of disability', 'Outside labour force']]
    title = 'Disabled working age persons Outside labour force'
elif selected_status == "Employment Rate":
    df_filtered = dataframe2_filtered[['Type of disability', 'Emp-Pop']]
    title = 'Employment Rate in Disabled working age persons'
elif selected_status == "Labour Force Participation Rate":
    df_filtered = dataframe2_filtered[['Type of disability', 'LFPR']]
    title = 'Labour Force Participation Rate in Disabled working age persons'
else:
    df_filtered = dataframe2_filtered[['Type of disability', 'Total']]
    title = 'Total Disabled working age persons'

# Create a bar chart
fig = px.bar(
    df_filtered,
    x='Type of disability',
    y=df_filtered.columns[1],  # Either 'Employed', 'Unemployed', or 'Total'
    title=title,
    labels={'Type of disability': 'Disability Type', df_filtered.columns[1]: 'Population'},
)

employed_population, people_with_disability = st.columns(2)

with employed_population:
    # -----------------------------------------------------
    # LINE CHART ==> EMPLOYED POPULATION BY SEX,AREA OF RESIDENCE AND OCCUPATION GROUP
    figline = px.line(
        dataframe4[dataframe4['Occupation Group'] != 'Occupation group (ISCO High level)'],
        x='Occupation Group',
        y=['Male', 'Female', 'Urban', 'Rural'],
        title='Employed By Occupation Gender and residence',
        labels={'Occupation Group': 'Occupation Group', 'value': 'Population'},
        line_shape="linear",  # Use "linear" for straight lines
    )

    figline.update_layout(
        height=500,
        width=400,
        legend_title_text='Category',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Show the line chart
    st.plotly_chart(figline)

with people_with_disability:
    # GRAPH FOR WORKING AGE PERSONS WITH DISABILITY Filters can be used
    fig.update_layout(
    bargap=0.2,
    bargroupgap=0.2,
    height=500,  # Set the height
    width=400    # Set the width
    )
    # Show the chart
    st.plotly_chart(fig)


# CHOOSE FILTER FOR EMPLOYES BY Duration Employmnent Contract
selected_column = st.sidebar.radio("Filter Employees Contract Duration By:", ['Total', 'Male', 'Female', 'Urban', 'Rural'])
employees_contract_duration, unemplyed_population_stats = st.columns(2)
with employees_contract_duration:
    # Exclude "Total employees/paid apprentices 16+" row
    dataframe5_filtered = dataframe5[dataframe5['Duration Employment Contract'] != 'Total employees/paid apprentices 16 +']
    # Create a horizontal bar chart
    fig = px.bar(
        dataframe5_filtered,
        x=selected_column,
        y='Duration Employment Contract',
        orientation='h',  # Set orientation to horizontal
        title=f'Duration of Employees Contract by {selected_column}',
        labels={selected_column: 'Population', 'Duration Employment Contract': 'Contract Duration'},
    )

    # Customize the layout if needed
    fig.update_layout(
        bargap=0.3,
        bargroupgap=0.1,
        height=500,
        width=400,
        xaxis_title='Population',
        yaxis_title='Contract Duration',
        yaxis=dict(tickangle=-45),  # Rotate the y-axis labels
    )
    # Show the chart
    st.plotly_chart(fig)
with unemplyed_population_stats:
        # List of common columns
    common_columns = ['Total', 'Male', 'Female', 'Urban', 'Rural', 'Participated in subsistence agriculture', 'Not participated  in subsistence agriculture']
    st.sidebar.subheader("Unemployement stats Filters: ")
    unemployment_dataframe = st.sidebar.radio("Choose Graph to View", ["By Age Group", "By Education", "By Duration of seeking employment"])

    # Function to filter and create the bar chart
    def create_bar_chart(dataframe, x_axis_column, y_axis_column):
        # Exclude 'Unemployed population 16+' rows
        filtered_dataframe = dataframe[dataframe[x_axis_column] != 'Unemployed population 16+']

        # Create a bar chart
        fig = px.bar(
            filtered_dataframe,
            x=x_axis_column,
            y=y_axis_column,
            title=f'Unemployed {y_axis_column} Population and {x_axis_column}',
            labels={x_axis_column: x_axis_column, y_axis_column: 'Population'},
        )

        # Customize the layout if needed
        fig.update_layout(
            bargap=0.3,
            bargroupgap=0.1,
            height=500,
            width=400,
            xaxis_title=x_axis_column,
            yaxis_title='Population',
        )

        return fig

    if unemployment_dataframe == "By Age Group":
        selected_column = st.selectbox("Select column for Y-axis:", common_columns, index=0)  # Default to 'Total'
        st.plotly_chart(create_bar_chart(dataframe6, 'Age Group', selected_column))

    elif unemployment_dataframe == "By Education":
        selected_column = st.selectbox("Select column for Y-axis:", common_columns, index=0)  # Default to 'Total'
        st.plotly_chart(create_bar_chart(dataframe7, 'Education', selected_column))

    else:
        selected_column = st.selectbox("Select column for Y-axis:", common_columns, index=0)  # Default to 'Total'
        st.plotly_chart(create_bar_chart(dataframe8, 'Duration', selected_column))



# LINE CHART FROM LABOUR FORCE INDICATORS BY DISTRICTS OR PROVINCES
# Multiselect box for selecting columns
selected_columns = st.multiselect("Select Labour Force Indicators To View Summary: ", dataframe9.columns[1:4])

# Selectbox for choosing between provinces and districts
selected_area_type = st.selectbox("Select Area Type", ['Provinces', 'Districts'])

# Filter data based on the selected area type
if selected_area_type == 'Provinces':
    selected_data = dataset_provinces
else:
    selected_data = dataset_districts

# Line chart
if selected_columns and not selected_data.empty:
    fig_line = px.line(
        selected_data,
        x='Area',
        y=selected_columns,
        title=f'Line Chart for {", ".join(selected_columns)} in {selected_area_type}',
        labels={'Area': 'Area', 'value': 'Value'},
    )

    # Customize the layout if needed
    fig_line.update_layout(
        height=500,
        width=800,
        legend_title_text='Category',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Show the line chart
    st.plotly_chart(fig_line)
else:
    st.warning("Select at least one column and make sure the dataset is not empty.")



remaining_columns = st.multiselect("Select Other Labour force indicators: ", dataframe9.columns[4:])

# Line chart for other labour force indicators
if remaining_columns and not selected_data.empty:
    fig_remaining_columns = px.line(
        selected_data,
        x='Area',
        y=remaining_columns,
        title=f'Line Chart for {", ".join(remaining_columns)} in {selected_area_type}',
        labels={'Area': 'Area', 'value': 'Value'},
    )

    # Customize the layout if needed
    fig_remaining_columns.update_layout(
        height=500,
        width=800,
        legend_title_text='Category',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Show the line chart for remaining columns
    st.plotly_chart(fig_remaining_columns)
else:
    st.warning("Select at least one column and make sure the dataset is not empty.")


st.write("Copyright © Peter NSABIMANA & Eric SIBOMANA")

# HIDE STREAMLIT STYLES
our_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* body {zoom: 90%;} */ /* Zoom out the body to 90% */
</style>
</style>
"""

st.markdown(our_style, unsafe_allow_html=True)
