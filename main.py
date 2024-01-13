import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from warnings import simplefilter # suppresses warning, allows > 100 columns to be created in new dataframe
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


general_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='General')
finance_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='Finance')
ela_math_science_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx',sheet_name='ELA Math Science')
iar_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='IAR')
iar_2_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='IAR (2)')
sat_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='SAT')
isa_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='ISA')
dlm_aa_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='DLM-AA')
dlm_aa_2_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='DLM-AA (2)')
cte_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='CTE')
teacher_out_to_field_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='TeacherOutofField')
discipline_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='Discipline')

print(general_df)

# create condensed version of discipline data sheet
discipline_condensed_df = pd.DataFrame()
rcdts = discipline_df.iloc[:,0]
discipline_condensed_df['RCDTS'] = rcdts.copy()
school_name = discipline_df.iloc[:,2]
discipline_condensed_df['School Name'] = school_name.copy() # school name
city = discipline_df.iloc[:,4]
discipline_condensed_df['City'] = city.copy() # city
school_type = discipline_df.iloc[:,8]
discipline_condensed_df['School Type'] = school_type.copy() # school type
number_of_discipline_incidents = discipline_df.iloc[:,11]
discipline_condensed_df['# of Discipline Incidents'] = \
    number_of_discipline_incidents.copy() # school type

# delete empty rows
def delete_row(df): # find all the non-missing values ONLY
    try:
        return df[df['School Name'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing school names')

# delete rows with empty cell under School Name
finance_condensed_df = delete_row(discipline_condensed_df)

# discipline condensed excel file xlsx
discipline_condensed_df.to_excel('discipline_condensed.xlsx', index=False)

# sort by alphabetical order
discipline_condensed_df = discipline_condensed_df.sort_values(
    by='School Name',
    ascending=True
)

discipline_condensed_df.to_excel('discipline_condensed.xlsx', index=False)

# create condensed version of finance data sheet
finance_condensed_df = pd.DataFrame()
rcdts = finance_df.iloc[:,0]
finance_condensed_df['RCDTS'] = rcdts.copy()
school_name = finance_df.iloc[:,2]
finance_condensed_df['School Name'] = school_name.copy() # school name
city = finance_df.iloc[:,4]
finance_condensed_df['City'] = city.copy() # city
school_type = finance_df.iloc[:,8]
finance_condensed_df['School Type'] = school_type.copy() # school type
total_per_pupil_expenditures_subtotal = finance_df.iloc[:,26]
finance_condensed_df['$ Total Per-Pupil Expenditures - Subtotal'] = \
    total_per_pupil_expenditures_subtotal.copy() # school name

# finance condensed file
finance_condensed_df.to_excel('finance_condensed.xlsx', index=False)
# delete rows with emtpy cell under School Name
finance_condensed_df = delete_row(finance_condensed_df)

finance_condensed_df.to_excel('finance_condensed.xlsx', index=False)

# lookup name of school, name of school column, $ Total Per-Pupil Expenditures - Subtotal column, false
discipline_finance_condensed_df = pd.merge(
    discipline_condensed_df,
    finance_condensed_df.iloc[:,4],
    left_index=True,
    right_index=True,
    how='outer'
)

# delete rows with emtpy cell under School Name
discipline_finance_condensed_df = delete_row(discipline_finance_condensed_df)

discipline_finance_condensed_df.to_excel('discipline_finance_condensed.xlsx', index=False)

discipline_finance_condensed_df = discipline_finance_condensed_df.sort_values(
    by='$ Total Per-Pupil Expenditures - Subtotal',
    ascending=True
)

discipline_finance_condensed_df.to_excel('discipline_finance_condensed.xlsx', index=False)

def incident_numbers_reported(df):
    # conversion of non-numeric values to NaN and then filtering rows based on those values
    numeric_mask = pd.to_numeric(df['# of Discipline Incidents'],
                                 errors='coerce').notna()
    if numeric_mask is None:
        raise ValueError
    return df[numeric_mask]

incident_numbers_df = incident_numbers_reported(discipline_condensed_df)

incident_numbers_df.to_excel('incident_numbers_reported.xlsx', index=False)


# pivot table - total student incident numbers of each city
total_incident_num_per_city_df = pd.pivot_table(incident_numbers_df,
                                                values='# of Discipline Incidents',
                                                columns='City',
                                                aggfunc='sum'
                                                )
total_incident_num_per_city_df.to_excel('sum_of_incidents_per_city_pivot_table.xlsx')

# pivot table - total student incident numbers per school type
total_incident_num_per_city_df = pd.pivot_table(incident_numbers_df,
                                                values='# of Discipline Incidents',
                                                columns='School Type',
                                                aggfunc='sum'
                                                )
total_incident_num_per_city_df.to_excel('sum_of_incidents_per_school_type_pivot_table.xlsx')

# highlight the lowest number of incidents
def highlight_min(data, color='#1dd7f3'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_min = data == data.min()
        return [attr if v else '' for v in is_min]
    else:  # from .apply(axis=None)
        is_min = data == data.min().min()
        return pd.DataFrame(np.where(is_min, attr, ''),
                            index=data.index, columns=data.columns)

incident_numbers_df = incident_numbers_df.style.apply(highlight_min, subset=['# of Discipline Incidents'])

incident_numbers_df.to_excel('incident_numbers_reported.xlsx', index=False)

# SAT Math Average Score (High Schools only and eventually calculate its averages of each county)
sat_condensed_df = pd.DataFrame()
rcdts = sat_df.iloc[:,0]
sat_condensed_df['RCDTS'] = rcdts.copy()
school_name = sat_df.iloc[:,2]
sat_condensed_df['School Name'] = school_name.copy() # school name
city = sat_df.iloc[:,4]
sat_condensed_df['City'] = city.copy()
county = sat_df.iloc[:,5]
sat_condensed_df['County'] = county.copy()
school_type = sat_df.iloc[:,8]
sat_condensed_df['School Type'] = school_type.copy() # school type
sat_reading_average_score = sat_df.iloc[:,10]
sat_condensed_df['SAT Reading Average Score'] = sat_reading_average_score.copy()
sat_math_average_score = sat_df.iloc[:,11]
sat_condensed_df['SAT Math Average Score'] = sat_math_average_score.copy()

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# filter data to only high schools
sat_condensed_df = sat_condensed_df.loc[(sat_condensed_df['School Type'] == 'HIGH SCHOOL')]

# delete empty rows
def empty_grade_value(df): # removes rows that have at least 1 average score null
    try:
        return df[df['SAT Reading Average Score'].notna() | df['SAT Math Average Score'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing SAT Reading Average Score or SAT Math Average Score values')

sat_condensed_df = empty_grade_value(sat_condensed_df)

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# create new columns -> Total Score, Average Score (Total Score / 1600), and Percentage
sat_condensed_df['Total SAT Score'] = sat_condensed_df['SAT Reading Average Score'] + \
                                            sat_condensed_df['SAT Math Average Score']
sat_condensed_df['SAT Score Percentage'] = sat_condensed_df['Total SAT Score'] / 1600
sat_condensed_df['SAT Score Percentage'] = sat_condensed_df['SAT Score Percentage']\
                                               .astype(str)\
                                               .str[2:4]\
                                               + '%'
sat_condensed_df['SAT Grade Status'] = [''] * len(sat_condensed_df)

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)
#sat_condensed_df.to_csv('sat_condensed.csv', index=False)

sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '9%', 'SAT Score Percentage'] = '90%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '8%', 'SAT Score Percentage'] = '80%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '7%', 'SAT Score Percentage'] = '70%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '6%', 'SAT Score Percentage'] = '60%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '5%', 'SAT Score Percentage'] = '50%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '4%', 'SAT Score Percentage'] = '40%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '3%', 'SAT Score Percentage'] = '30%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '2%', 'SAT Score Percentage'] = '20%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '1%', 'SAT Score Percentage'] = '10%'

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# values in 'SAT Grade Status' -> Low, Mediocre, Decent, Good, Excellent
status = []
for grade in sat_condensed_df['Total SAT Score']:
    try:
        if grade >= 1400:
            status.append('Excellent')
        elif grade >= 1000 and grade < 1400:
            status.append('Proficient')
        elif grade >= 800 and grade < 1000:
            status.append('Decent')
        elif grade >= 600 and grade < 800:
            status.append('Mediocre')
        else:
            status.append('Low')
            raise ValueError
    except:
        status.append('Not an appropriate value')

sat_condensed_df['SAT Grade Status'] = status

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# top 5 total sat scores
sat_condensed_top_five_high_total_scores_df = sat_condensed_df['Total SAT Score'].\
    sort_values(ascending=False).head()

sat_condensed_top_five_high_total_scores_df.to_excel('sat_condensed_top_five_total_scores.xlsx',
                                                    index=False)

# bottom 5 total sat scores
sat_condensed_bot_five_low_total_scores_df = sat_condensed_df['Total SAT Score'].\
    sort_values(ascending=False).tail()

sat_condensed_bot_five_low_total_scores_df.to_excel('sat_condensed_bottom_five_total_scores.xlsx',
                                                    index=False)

# list of schools with sat grade status = 'excellent'
sat_condensed_excellent_total_scores_df =  \
    sat_condensed_df.loc[(sat_condensed_df['SAT Grade Status'] == 'Excellent')]

sat_condensed_excellent_total_scores_df.to_excel('sat_condensed_total_scores_excellent.xlsx',
                                                 index=False)

# list of schools with sat grade status = 'proficient'
sat_condensed_proficient_total_scores_df =  \
    sat_condensed_df.loc[(sat_condensed_df['SAT Grade Status'] == 'Proficient')]

sat_condensed_proficient_total_scores_df.to_excel('sat_condensed_total_scores_proficient.xlsx',
                                                 index=False)

# list of schools with sat grade status = 'decent'
sat_condensed_decent_total_scores_df =  \
    sat_condensed_df.loc[(sat_condensed_df['SAT Grade Status'] == 'Decent')]

sat_condensed_decent_total_scores_df.to_excel('sat_condensed_total_scores_decent.xlsx',
                                                 index=False)

# list of schools with sat grade status = 'mediocre'
sat_condensed_mediocre_total_scores_df =  \
    sat_condensed_df.loc[(sat_condensed_df['SAT Grade Status'] == 'Mediocre')]

sat_condensed_mediocre_total_scores_df.to_excel('sat_condensed_total_scores_mediocre.xlsx',
                                                 index=False)

# list of schools with sat grade status = 'low'
sat_condensed_low_total_scores_df =  \
    sat_condensed_df.loc[(sat_condensed_df['SAT Grade Status'] == 'Low')]

sat_condensed_low_total_scores_df.to_excel('sat_condensed_total_scores_low.xlsx',
                                                 index=False)

# highlight the highest Total SAT Score value
def highlight_max(data, color='green'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)

sat_condensed_highlight_max_total_sat_score_value_df = sat_condensed_df.style.apply(
    highlight_max,
    subset=['Total SAT Score']
)

sat_condensed_highlight_max_total_sat_score_value_df.to_excel(
    'sat_condensed_highlighted_top_total_score.xlsx',
    index=False
)

# create pivot table with SAT score average per county
sat_condensed_avg_score_per_county_pivot_table = pd.pivot_table(
    sat_condensed_df,
    index='City',
    columns='County',
    values='Total SAT Score',
    aggfunc='mean'
)

sat_condensed_avg_score_per_county_pivot_table.to_excel('sat_condensed_avg_score_per_county_pivot_table.xlsx')

'''
# creating a bar chart of total SAT scores per county
file = pd.read_excel('sat_condensed.xlsx')

x_axis = file['County']
y_axis = file['Total SAT Score']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("County")
plt.ylabel("Total SAT Score Per County")
plt.show()
'''

'''
# creating a pie chart of total SAT scores per county
fig = px.bar(sat_condensed_df, x='County', y='Total SAT Score', title='Total SAT Score Per County')

# set the border and background color of the chart area
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='lightgray',
    width=800,
    height=500,
    shapes=[dict(type='rect', xref='paper',
            yref='paper',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            line=dict(
                color='black',
                width=2,
            ),
        )
    ]
)
#display the graph
fig.show()
# Alternatively you can save the bar graph to an image using below line of code
pio.write_image(fig, 'bar_graph.png')
'''

# isa proficiency
isa_condensed_df = pd.DataFrame()
rcdts = isa_df.iloc[:,0]
isa_condensed_df['RCDTS'] = rcdts.copy()
school_name = isa_df.iloc[:,2]
isa_condensed_df['School Name'] = school_name.copy() # school name
city = isa_df.iloc[:,4]
isa_condensed_df['City'] = city.copy()
county = isa_df.iloc[:,5]
isa_condensed_df['County'] = county.copy()
district_size = isa_df.iloc[:,7]
isa_condensed_df['District Size'] = district_size.copy()
school_type = isa_df.iloc[:,8]
isa_condensed_df['School Type'] = school_type.copy()
isa_proficiency_total_student = isa_df.iloc[:,10]
isa_condensed_df['# ISA Proficiency Total Student'] = isa_proficiency_total_student.copy()
isa_proficiency_male = isa_df.iloc[:,11]
isa_condensed_df['# ISA Proficiency - Male'] = isa_proficiency_male.copy()
isa_proficiency_female = isa_df.iloc[:,12]
isa_condensed_df['# ISA Proficiency - Female'] = isa_proficiency_female.copy()
isa_proficiency_white = isa_df.iloc[:,13]
isa_condensed_df['# ISA Proficiency - White'] = isa_proficiency_white.copy()
isa_proficiency_black_or_african_american = isa_df.iloc[:,14]
isa_condensed_df['# ISA Proficiency - Black or African American'] = \
    isa_proficiency_black_or_african_american.copy()
isa_proficiency_hispanic_or_latino = isa_df.iloc[:,15]
isa_condensed_df['# ISA Proficiency - Hispanic or Latino'] = \
    isa_proficiency_hispanic_or_latino.copy()
isa_proficiency_asian = isa_df.iloc[:,16]
isa_condensed_df['# ISA Proficiency - Asian'] = isa_proficiency_asian.copy()
isa_proficiency_native_hawaiian_or_other_pacific_islander = isa_df.iloc[:,17]
isa_condensed_df['# ISA Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    isa_proficiency_native_hawaiian_or_other_pacific_islander.copy()
isa_proficiency_american_indian_or_alaska_native = isa_df.iloc[:,18]
isa_condensed_df['# ISA Proficiency - American Indian or Alaska Native'] = \
    isa_proficiency_american_indian_or_alaska_native.copy()
isa_proficiency_two_or_more_races = isa_df.iloc[:,19]
isa_condensed_df['# ISA Proficiency - Two or More Races'] = isa_proficiency_two_or_more_races.copy()
isa_proficiency_children_with_disabilities = isa_df.iloc[:,20]
isa_condensed_df['# ISA Proficiency - Children with Disabilities'] = \
    isa_proficiency_children_with_disabilities.copy()

isa_condensed_df.to_excel('isa_condensed.xlsx', index=False)

# if school name AND proficiency values for total student, male, and female are blank for each column, REMOVE row
def grab_isa_gender_data(df): # find all the non-missing values ONLY
    try:
        return df[df['School Name'].notna() &
                  df['# ISA Proficiency Total Student'].notna() &
                  df['# ISA Proficiency - Male'].notna() &
                  df['# ISA Proficiency - Female'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete certain rows within grab_isa_gender_data().')

# delete rows with empty cell under proficiency columns in grab_isa_gender_data()
isa_condensed_gender_df = grab_isa_gender_data(isa_condensed_df)

# create updated version of isa condensed gender (male/female) data
isa_condensed_gender_df.to_excel('isa_condensed_gender_data.xlsx', index=False)

# if the # isa proficiency values of white students is blank, remove row
def grab_isa_white_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - White'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_white_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_white_students_data()
isa_condensed_white_students_data_df = grab_isa_white_students_data(isa_condensed_gender_df)

# create updated version of isa condensed white students data
isa_condensed_white_students_data_df.to_excel('isa_condensed_white_students_data.xlsx', index=False)

# drop # isa columns that are not relative to black students in the dataframe
isa_condensed_white_students_data_df = isa_condensed_white_students_data_df.\
    drop(['# ISA Proficiency - Black or African American',
          '# ISA Proficiency - Hispanic or Latino',
          '# ISA Proficiency - Asian',
          '# ISA Proficiency - Native Hawaiian or Other Pacific Islander',
          '# ISA Proficiency - American Indian or Alaska Native',
          '# ISA Proficiency - Two or More Races',
          '# ISA Proficiency - Children with Disabilities'],
         axis=1)

isa_condensed_white_students_data_df.to_excel('isa_condensed_white_students_data.xlsx', index=False)
# add percentage column to dataframe
isa_condensed_white_students_data_df['White Students %'] =\
    isa_condensed_white_students_data_df['# ISA Proficiency - White'] / \
    isa_condensed_white_students_data_df['# ISA Proficiency Total Student']

isa_condensed_white_students_data_df.to_excel('isa_condensed_white_students_data.xlsx', index=False)

# if the # isa proficiency values of black students is blank, remove row
def grab_isa_black_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Black or African American'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_black_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_black_students_data()
isa_condensed_black_students_data_df = grab_isa_black_students_data(isa_condensed_gender_df)

# create updated version of isa condensed black students data
isa_condensed_black_students_data_df.to_excel('isa_condensed_black_students_data.xlsx', index=False)
# drop # isa columns that are not relative to black students in the dataframe
isa_condensed_black_students_data_df = isa_condensed_black_students_data_df.\
    drop(['# ISA Proficiency - White',
          '# ISA Proficiency - Hispanic or Latino',
          '# ISA Proficiency - Asian',
          '# ISA Proficiency - Native Hawaiian or Other Pacific Islander',
          '# ISA Proficiency - American Indian or Alaska Native',
          '# ISA Proficiency - Two or More Races',
          '# ISA Proficiency - Children with Disabilities'],
         axis=1)

isa_condensed_black_students_data_df.to_excel('isa_condensed_black_students_data.xlsx', index=False)

# add percentage column to dataframe
isa_condensed_black_students_data_df['Black or African American Students %'] =\
    isa_condensed_black_students_data_df['# ISA Proficiency - Black or African American'] / \
    isa_condensed_black_students_data_df['# ISA Proficiency Total Student']

isa_condensed_black_students_data_df.to_excel('isa_condensed_black_students_data.xlsx', index=False)

# if the # isa proficiency values of hispanic students is blank, remove row
def grab_isa_hispanic_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Hispanic or Latino'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_hispanic_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_hispanic_students_data()
isa_condensed_hispanic_students_data_df = grab_isa_hispanic_students_data(isa_condensed_gender_df)

# create updated version of isa condensed hispanic students data
isa_condensed_hispanic_students_data_df.to_excel('isa_condensed_hispanic_students_data.xlsx',
                                                 index=False)
# drop # isa columns that are not relative to hispanic students in the dataframe
isa_condensed_hispanic_students_data_df = isa_condensed_hispanic_students_data_df.\
    drop(['# ISA Proficiency - White',
          '# ISA Proficiency - Black or African American',
          '# ISA Proficiency - Asian',
          '# ISA Proficiency - Native Hawaiian or Other Pacific Islander',
          '# ISA Proficiency - American Indian or Alaska Native',
          '# ISA Proficiency - Two or More Races',
          '# ISA Proficiency - Children with Disabilities'],
         axis=1)

isa_condensed_hispanic_students_data_df.to_excel('isa_condensed_hispanic_students_data.xlsx',
                                                 index=False)

# add percentage column to dataframe
isa_condensed_hispanic_students_data_df['Hispanic Students %'] =\
    isa_condensed_hispanic_students_data_df['# ISA Proficiency - Hispanic or Latino'] / \
    isa_condensed_hispanic_students_data_df['# ISA Proficiency Total Student']

isa_condensed_hispanic_students_data_df.to_excel('isa_condensed_hispanic_students_data.xlsx', index=False)

# if the # isa proficiency values of asian students is blank, remove row
def grab_isa_asian_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Asian'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_asian_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_asian_students_data()
isa_condensed_asian_students_data_df = grab_isa_asian_students_data(isa_condensed_gender_df)

# create updated version of isa condensed asian students data
isa_condensed_asian_students_data_df.to_excel('isa_condensed_asian_students_data.xlsx', index=False)

# add percentage column to dataframe

# if the # isa proficiency values of hawaiian and other pacific islander students is blank, remove row
def grab_isa_pacific_islander_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Native Hawaiian or Other Pacific Islander'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_pacific_islander_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_pacific_islander_students_data()
isa_condensed_pacific_islander_students_data_df = \
    grab_isa_pacific_islander_students_data(isa_condensed_gender_df)

# create updated version of isa condensed hawaiian and other pacific islander students data
isa_condensed_pacific_islander_students_data_df.to_excel\
    ('isa_condensed_pacific_islander_students_data.xlsx', index=False)

# if the # isa proficiency values of alaskan or american indian students is blank, remove row
def grab_isa_american_indian_or_alaskan_native_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - American Indian or Alaska Native'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_american_indian_or_alaskan_native_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_american_indian_or_alaskan_native_students_data()
isa_condensed_american_indian_or_alaskan_native_students_data_df = \
    grab_isa_american_indian_or_alaskan_native_students_data(isa_condensed_gender_df)

# create updated version of isa condensed alaskan or american indian students data
isa_condensed_american_indian_or_alaskan_native_students_data_df.to_excel\
    ('isa_condensed_alaskan_or_american_indian_students_data.xlsx', index=False)

# if the # isa proficiency values of multiracial students is blank, remove row
def grab_isa_multiracial_students_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Two or More Races'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_multiracial_students_data()')

# delete rows with empty cell under proficiency columns in grab_isa_multiracial_students_data()
isa_condensed_isa_multiracial_students_data_df = \
    grab_isa_multiracial_students_data(isa_condensed_gender_df)

# create updated version of isa condensed multiracial students data
isa_condensed_isa_multiracial_students_data_df.to_excel\
    ('isa_condensed_multiracial_students_data.xlsx', index=False)

# if the # isa proficiency values of children with disabilities students is blank, remove row
def grab_isa_children_with_disabilities_data(df): # find all the non-missing values ONLY
    try:
        return df[df['# ISA Proficiency - Children with Disabilities'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing data within grab_isa_children_with_disabilities_data()')

# delete rows with empty cell under proficiency columns in grab_isa_children_with_disabilities_data()
isa_condensed_isa_children_with_disabilities_data_df = \
    grab_isa_children_with_disabilities_data(isa_condensed_gender_df)

# create updated version of isa condensed children with disabilities students data
isa_condensed_isa_children_with_disabilities_data_df.to_excel\
    ('isa_condensed_children_with_disabilities_data.xlsx', index=False)

# isa white students pivot table
isa_condensed_white_students_table = pd.pivot_table(
    isa_condensed_white_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - White',
    aggfunc='sum'
)

# isa white students pivot table
isa_condensed_white_students_table.to_excel('isa_condensed_white_student_num_pivot_table.xlsx')

# isa black students pivot table
isa_condensed_black_students_table = pd.pivot_table(
    isa_condensed_black_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Black or African American',
    aggfunc='sum'
)

# isa black students pivot table
isa_condensed_black_students_table.to_excel('isa_condensed_black_student_num_pivot_table.xlsx')

# isa hispanic students pivot table
isa_condensed_hispanic_students_table = pd.pivot_table(
    isa_condensed_hispanic_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Hispanic or Latino',
    aggfunc='sum'
)

# isa hispanic students pivot table
isa_condensed_hispanic_students_table.to_excel('isa_condensed_hispanic_student_num_pivot_table.xlsx')

# isa asian students pivot table
isa_condensed_asian_students_table = pd.pivot_table(
    isa_condensed_asian_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Asian',
    aggfunc='sum'
)

# isa asian students pivot table
isa_condensed_asian_students_table.to_excel('isa_condensed_asian_student_num_pivot_table.xlsx')

# isa pacific islander students pivot table
isa_condensed_pacific_islander_students_table = pd.pivot_table(
    isa_condensed_pacific_islander_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Native Hawaiian or Other Pacific Islander',
    aggfunc='sum'
)

# isa pacific islander students pivot table
isa_condensed_pacific_islander_students_table.\
    to_excel('isa_condensed_pacific_islander_student_num_pivot_table.xlsx')

# isa american indian or alaska native students pivot table
isa_condensed_american_indian_or_alaska_native_students_table = pd.pivot_table(
    isa_condensed_american_indian_or_alaskan_native_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - American Indian or Alaska Native',
    aggfunc='sum'
)

# isa american indian or alaska native students pivot table
isa_condensed_american_indian_or_alaska_native_students_table\
    .to_excel('isa_condensed_american_indian_or_alaska_native_student_num_pivot_table.xlsx')

# isa multiracial students pivot table
isa_condensed_multiracial_students_table = pd.pivot_table(
    isa_condensed_isa_multiracial_students_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Two or More Races',
    aggfunc='sum'
)

# isa multiracial students pivot table
isa_condensed_multiracial_students_table\
    .to_excel('isa_condensed_multiracial_student_num_pivot_table.xlsx')

# isa children with disabilities pivot table
isa_condensed_children_with_disabilities_table = pd.pivot_table(
    isa_condensed_isa_children_with_disabilities_data_df,
    index='City',
    columns='County',
    values='# ISA Proficiency - Children with Disabilities',
    aggfunc='sum'
)

# children with disabilities pivot table
isa_condensed_children_with_disabilities_table\
    .to_excel('isa_condensed_children_with_disabilities_num_pivot_table.xlsx')

# concat isa white and black student pivot tables via keys
isa_pivot_table_white_and_black_student_frames = \
    [
        isa_condensed_white_students_table,
        isa_condensed_black_students_table
    ]

isa_pivot_table_white_and_black_student_concat = pd.concat(
    isa_pivot_table_white_and_black_student_frames,
    keys=['White Students','Black Students']
)

isa_pivot_table_white_and_black_student_concat.\
    to_excel('pivot_table_white_and_black_student_concat.xlsx')

# concat all isa students (race only) pivot tables via keys
isa_pivot_table_all_races_frames = \
    [
        isa_condensed_white_students_table,
        isa_condensed_black_students_table,
        isa_condensed_hispanic_students_table,
        isa_condensed_asian_students_table,
        isa_condensed_pacific_islander_students_table,
        isa_condensed_american_indian_or_alaska_native_students_table,
        isa_condensed_multiracial_students_table,
    ]

isa_pivot_table_all_races_concat = pd.concat(
    isa_pivot_table_all_races_frames,
    keys=[
        'White Students',
        'Black Students',
        'Hispanic or Latino Students',
        'Asian Students',
        'Native Hawaiian or Other Pacific Islander Students',
        'American Indian or Alaska Native Students',
        'Two or More Races Students'
        ]
)

isa_pivot_table_all_races_concat.to_excel('isa_pivot_table_all_races_concat.xlsx')

# creating a bar chart of isa proficiency pertaining to white students per school
file = pd.read_excel('isa_condensed_white_students_data.xlsx')

x_axis = file['# ISA Proficiency - White']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("White Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to black students per school
file = pd.read_excel('isa_condensed_black_students_data.xlsx')

x_axis = file['# ISA Proficiency - Black or African American']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Black or African American Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to hispanic students per school
file = pd.read_excel('isa_condensed_hispanic_students_data.xlsx')

x_axis = file['# ISA Proficiency - Hispanic or Latino']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Hispanic or Latino Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to asian students per school
file = pd.read_excel('isa_condensed_asian_students_data.xlsx')

x_axis = file['# ISA Proficiency - Asian']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Asian Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to pacific islander students per school
file = pd.read_excel('isa_condensed_pacific_islander_students_data.xlsx')

x_axis = file['# ISA Proficiency - Native Hawaiian or Other Pacific Islander']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Native Hawaiian or Other Pacific Islander Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to alaskan or american indian students per school
file = pd.read_excel('isa_condensed_alaskan_or_american_indian_students_data.xlsx')

x_axis = file['# ISA Proficiency - American Indian or Alaska Native']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("American Indian or Alaska Native Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to multiracial students per school
file = pd.read_excel('isa_condensed_multiracial_students_data.xlsx')

x_axis = file['# ISA Proficiency - Two or More Races']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Multiracial Students Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# creating a bar chart of isa proficiency pertaining to students with disabilities per school
file = pd.read_excel('isa_condensed_multiracial_students_data.xlsx')

x_axis = file['# ISA Proficiency - Children with Disabilities']
y_axis = file['# ISA Proficiency Total Student']

plt.bar(x_axis, y_axis, width=5)
plt.xlabel("Students w/Disabilities Per School")
plt.ylabel("# ISA Proficiency Total Student")
plt.show()

# create new spreadsheet with ELA scores (ELA first, followed by math, and then science)
ela_math_science_condensed_df = pd.DataFrame()
rcdts = ela_math_science_df.iloc[:,0]
ela_math_science_condensed_df['RCDTS'] = rcdts.copy()
school_name = ela_math_science_df.iloc[:,2]
ela_math_science_condensed_df['School Name'] = school_name.copy() # school name
city = ela_math_science_df.iloc[:,4]
ela_math_science_condensed_df['City'] = city.copy()
county = ela_math_science_df.iloc[:,5]
ela_math_science_condensed_df['County'] = county.copy()
district_size = ela_math_science_df.iloc[:,7]
ela_math_science_condensed_df['District Size'] = district_size.copy()
school_type = ela_math_science_df.iloc[:,8]
ela_math_science_condensed_df['School Type'] = school_type.copy()
ela_math_science_proficiency_total_student = ela_math_science_df.iloc[:,10]
ela_math_science_condensed_df['# ELA Proficiency Total Student'] = \
    ela_math_science_proficiency_total_student.copy()
ela_math_science_proficiency_male = ela_math_science_df.iloc[:,11]
ela_math_science_condensed_df['# ELA Proficiency - Male'] = \
    ela_math_science_proficiency_male.copy()
ela_math_science_proficiency_female = ela_math_science_df.iloc[:,12]
ela_math_science_condensed_df['# ELA Proficiency - Female'] = \
    ela_math_science_proficiency_female.copy()
ela_math_science_proficiency_white = ela_math_science_df.iloc[:,13]
ela_math_science_condensed_df['# ELA Proficiency - White'] = \
    ela_math_science_proficiency_white.copy()
ela_math_science_proficiency_black_or_african_american = ela_math_science_df.iloc[:,14]
ela_math_science_condensed_df['# ELA Proficiency - Black or African American'] = \
    ela_math_science_proficiency_black_or_african_american.copy()
ela_math_science_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,15]
ela_math_science_condensed_df['# ELA Proficiency - Hispanic or Latino'] = \
    ela_math_science_proficiency_hispanic_or_latino.copy()
ela_math_science_proficiency_asian = ela_math_science_df.iloc[:,16]
ela_math_science_condensed_df['# ELA Proficiency - Asian'] = \
    ela_math_science_proficiency_asian.copy()
ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,17]
ela_math_science_condensed_df['# ELA Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander.copy()
ela_math_science_proficiency_american_indian_or_alaska_native = \
    ela_math_science_df.iloc[:,18]
ela_math_science_condensed_df['# ELA Proficiency - American Indian or Alaska Native'] = \
    ela_math_science_proficiency_american_indian_or_alaska_native.copy()
ela_math_science_proficiency_two_or_more_races = ela_math_science_df.iloc[:,19]
ela_math_science_condensed_df['# ELA Proficiency - Two or More Races'] = \
    ela_math_science_proficiency_two_or_more_races.copy()
ela_math_science_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,20]
ela_math_science_condensed_df['# ELA Proficiency - Children with Disabilities'] = \
    ela_math_science_proficiency_children_with_disabilities.copy()
ela_math_science_proficiency_total_student = ela_math_science_df.iloc[:,46]
ela_math_science_condensed_df['# Math Proficiency Total Student'] = \
    ela_math_science_proficiency_total_student.copy()
ela_math_science_proficiency_male = ela_math_science_df.iloc[:,47]
ela_math_science_condensed_df['# Math Proficiency - Male'] = \
    ela_math_science_proficiency_male.copy()
ela_math_science_proficiency_female = ela_math_science_df.iloc[:,48]
ela_math_science_condensed_df['# Math Proficiency - Female'] = \
    ela_math_science_proficiency_female.copy()
ela_math_science_proficiency_white = ela_math_science_df.iloc[:,49]
ela_math_science_condensed_df['# Math Proficiency - White'] = \
    ela_math_science_proficiency_white.copy()
ela_math_science_proficiency_black_or_african_american = \
    ela_math_science_df.iloc[:,50]
ela_math_science_condensed_df['# Math Proficiency - Black or African American'] = \
    ela_math_science_proficiency_black_or_african_american.copy()
ela_math_science_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,51]
ela_math_science_condensed_df['# Math Proficiency - Hispanic or Latino'] = \
    ela_math_science_proficiency_hispanic_or_latino.copy()
ela_math_science_proficiency_asian = ela_math_science_df.iloc[:,52]
ela_math_science_condensed_df['# Math Proficiency - Asian'] = \
    ela_math_science_proficiency_asian.copy()
ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,53]
ela_math_science_condensed_df['# Math Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander.copy()
ela_math_science_proficiency_american_indian_or_alaska_native = ela_math_science_df.iloc[:,54]
ela_math_science_condensed_df['# Math Proficiency - American Indian or Alaska Native'] = \
    ela_math_science_proficiency_american_indian_or_alaska_native.copy()
ela_math_science_proficiency_two_or_more_races = ela_math_science_df.iloc[:,55]
ela_math_science_condensed_df['# Math Proficiency - Two or More Races'] = \
    ela_math_science_proficiency_two_or_more_races.copy()
ela_math_science_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,56]
ela_math_science_condensed_df['# Math Proficiency - Children with Disabilities'] = \
    ela_math_science_proficiency_children_with_disabilities.copy()
ela_math_science_proficiency_total_student = ela_math_science_df.iloc[:,208]
ela_math_science_condensed_df['# Science Proficiency Total Student'] = \
    ela_math_science_proficiency_total_student.copy()
ela_math_science_proficiency_male = ela_math_science_df.iloc[:,209]
ela_math_science_condensed_df['# Science Proficiency - Male'] = \
    ela_math_science_proficiency_male.copy()
ela_math_science_proficiency_female = ela_math_science_df.iloc[:,210]
ela_math_science_condensed_df['# Science Proficiency - Female'] = \
    ela_math_science_proficiency_female.copy()
ela_math_science_proficiency_white = ela_math_science_df.iloc[:,211]
ela_math_science_condensed_df['# Science Proficiency - White'] = \
    ela_math_science_proficiency_white.copy()
ela_math_science_proficiency_black_or_african_american = \
    ela_math_science_df.iloc[:,212]
ela_math_science_condensed_df['# Science Proficiency - Black or African American'] = \
    ela_math_science_proficiency_black_or_african_american.copy()
ela_math_science_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,213]
ela_math_science_condensed_df['# Science Proficiency - Hispanic or Latino'] = \
    ela_math_science_proficiency_hispanic_or_latino.copy()
ela_math_science_proficiency_asian = ela_math_science_df.iloc[:,214]
ela_math_science_condensed_df['# Science Proficiency - Asian'] = \
    ela_math_science_proficiency_asian.copy()
ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,215]
ela_math_science_condensed_df['# Science Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    ela_math_science_proficiency_native_hawaiian_or_other_pacific_islander.copy()
ela_math_science_proficiency_american_indian_or_alaska_native = \
    ela_math_science_df.iloc[:,216]
ela_math_science_condensed_df['# Science Proficiency - American Indian or Alaska Native'] = \
    ela_math_science_proficiency_american_indian_or_alaska_native.copy()
ela_math_science_proficiency_two_or_more_races = ela_math_science_df.iloc[:,217]
ela_math_science_condensed_df['# Science Proficiency - Two or More Races'] = \
    ela_math_science_proficiency_two_or_more_races.copy()
ela_math_science_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,218]
ela_math_science_condensed_df['# Science Proficiency - Children with Disabilities'] = \
    ela_math_science_proficiency_children_with_disabilities.copy()

ela_math_science_condensed_df.to_excel('ela_math_science_condensed.xlsx', index=False)

# delete rows with empty cell under School Name
ela_math_science_condensed_df = delete_row(ela_math_science_condensed_df)

ela_math_science_condensed_df.to_excel('ela_math_science_condensed.xlsx', index=False)

def high_schools(df):
    try:
        return df[df['School Type'] == 'HIGH SCHOOL']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot filter rows')
              
ela_math_science_condensed_high_schools_df = high_schools(ela_math_science_condensed_df)

# high schools only
ela_math_science_condensed_high_schools_df.to_excel(
    'ela_math_science_condensed_high_schools.xlsx',
    index=False
)

def charter_schools(df):
    try:
        return df[df['School Type'] == 'CHARTER SCH']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot filter rows')
              
ela_math_science_condensed_charter_schools_df = charter_schools(ela_math_science_condensed_df)

# charter schools only
ela_math_science_condensed_charter_schools_df.to_excel(
    'ela_math_science_condensed_charter_schools.xlsx',
    index=False
)

def elementary_schools(df):
    try:
        return df[df['School Type'] == 'ELEMENTARY']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot filter rows')
              
ela_math_science_condensed_elementary_schools_df = elementary_schools(ela_math_science_condensed_df)

# elementary schools only
ela_math_science_condensed_elementary_schools_df.to_excel(
    'ela_math_science_condensed_elementary_schools.xlsx',
    index=False
)

def middle_schools(df):
    try:
        return df[df['School Type'] == 'MIDDLE SCHL']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot filter rows')
              
ela_math_science_condensed_middle_schools_df = middle_schools(ela_math_science_condensed_df)

# middle schools only
ela_math_science_condensed_middle_schools_df.to_excel(
    'ela_math_science_condensed_middle_schools.xlsx',
    index=False
)

def preschools(df):
    try:
        return df[df['School Type'] == 'PreK']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot filter rows')
              
ela_math_science_condensed_preschools_df = preschools(ela_math_science_condensed_df)

# preschools only
ela_math_science_condensed_preschools_df.to_excel(
    'ela_math_science_condensed_preschools.xlsx',
    index=False
)

'''
# filter data to only high schools
ela_math_science_condensed_high_schools_df = \
    ela_math_science_condensed_df.loc[
        (ela_math_science_condensed_df['School Type'] == 'HIGH SCHOOL')
    ]
# filter data to only charter schools
ela_math_science_condensed_charter_schools_df = \
    ela_math_science_condensed_df.loc[
        (ela_math_science_condensed_df['School Type'] == 'CHARTER SCH')
    ]
# filter data to only elementary schools
ela_math_science_condensed_elementary_schools_df = \
    ela_math_science_condensed_df.loc[
        (ela_math_science_condensed_df['School Type'] == 'ELEMENTARY')
    ]
# filter data to only middle schools
ela_math_science_condensed_middle_schools_df = \
    ela_math_science_condensed_df.loc[
        (ela_math_science_condensed_df['School Type'] == 'MIDDLE SCHL')
    ]
# filter data to only preschools
ela_math_science_condensed_preschools_df = \
    ela_math_science_condensed_df.loc[
        (ela_math_science_condensed_df['School Type'] == 'PreK')
    ]

# high schools only
ela_math_science_condensed_high_schools_df.to_excel(
    'ela_math_science_condensed_high_schools.xlsx',
    index=False
)
# charter schools only
ela_math_science_condensed_charter_schools_df.to_excel(
    'ela_math_science_condensed_charter_schools.xlsx',
    index=False
)
# elementary schools only
ela_math_science_condensed_elementary_schools_df.to_excel(
    'ela_math_science_condensed_elementary_schools.xlsx',
    index=False
)
# middle schools only
ela_math_science_condensed_middle_schools_df.to_excel(
    'ela_math_science_condensed_middle_schools.xlsx',
    index=False
)
# preschools only
ela_math_science_condensed_preschools_df.to_excel(
    'ela_math_science_condensed_preschools.xlsx',
    index=False
)
'''

# creating dataframes for ela, math, and science each
# ela only
ela_only_df = pd.DataFrame()
rcdts = ela_math_science_df.iloc[:,0]
ela_only_df['RCDTS'] = rcdts.copy()
school_name = ela_math_science_df.iloc[:,2]
ela_only_df['School Name'] = school_name.copy() # school name
city = ela_math_science_df.iloc[:,4]
ela_only_df['City'] = city.copy()
county = ela_math_science_df.iloc[:,5]
ela_only_df['County'] = county.copy()
district_size = ela_math_science_df.iloc[:,7]
ela_only_df['District Size'] = district_size.copy()
school_type = ela_math_science_df.iloc[:,8]
ela_only_df['School Type'] = school_type.copy()
ela_proficiency_total_student = ela_math_science_df.iloc[:,10]
ela_only_df['# ELA Proficiency Total Student'] = \
    ela_proficiency_total_student.copy()
ela_proficiency_male = ela_math_science_df.iloc[:,11]
ela_only_df['# ELA Proficiency - Male'] = \
    ela_proficiency_male.copy()
ela_proficiency_female = ela_math_science_df.iloc[:,12]
ela_only_df['# ELA Proficiency - Female'] = \
    ela_proficiency_female.copy()
ela_proficiency_white = ela_math_science_df.iloc[:,13]
ela_only_df['# ELA Proficiency - White'] = \
    ela_proficiency_white.copy()
ela_proficiency_black_or_african_american = \
    ela_math_science_df.iloc[:,14]
ela_only_df['# ELA Proficiency - Black or African American'] = \
    ela_proficiency_black_or_african_american.copy()
ela_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,15]
ela_only_df['# ELA Proficiency - Hispanic or Latino'] = \
    ela_proficiency_hispanic_or_latino.copy()
ela_proficiency_asian = ela_math_science_df.iloc[:,16]
ela_only_df['# ELA Proficiency - Asian'] = \
    ela_proficiency_asian.copy()
ela_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,17]
ela_only_df['# ELA Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    ela_proficiency_native_hawaiian_or_other_pacific_islander.copy()
ela_proficiency_american_indian_or_alaska_native = ela_math_science_df.iloc[:,18]
ela_only_df['# ELA Proficiency - American Indian or Alaska Native'] = \
    ela_proficiency_american_indian_or_alaska_native.copy()
ela_proficiency_two_or_more_races = ela_math_science_df.iloc[:,19]
ela_only_df['# ELA Proficiency - Two or More Races'] = \
    ela_proficiency_two_or_more_races.copy()
ela_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,20]
ela_only_df['# ELA Proficiency - Children with Disabilities'] = \
    ela_proficiency_children_with_disabilities.copy()
# data of all school types in one doc
ela_only_df.to_excel('ela_only.xlsx', index=False)
# delete row not containing name of school
ela_only_df = delete_row(ela_only_df)

ela_only_df.to_excel('ela_only.xlsx', index=False)
ela_only_df.to_csv('ela_only.csv', index=False)

# filter out all rows except high schools
ela_proficiency_high_schools_only_df = high_schools(ela_only_df)

# high schools only
ela_proficiency_high_schools_only_df.to_excel(
    'ela_proficiency_high_schools_only.xlsx',
    index=False
)

# filter out all rows except charter schools
ela_proficiency_charter_schools_only_df = charter_schools(ela_only_df)

# charter schools only
ela_proficiency_charter_schools_only_df.to_excel(
    'ela_proficiency_charter_schools_only.xlsx',
    index=False
)

# filter out all rows except elementary schools
ela_proficiency_elementary_schools_only_df = elementary_schools(ela_only_df)

# elementary schools only
ela_proficiency_elementary_schools_only_df.to_excel(
    'ela_proficiency_elementary_schools_only.xlsx',
    index=False
)

# filter out all rows except middle schools
ela_proficiency_middle_schools_only_df = middle_schools(ela_only_df)

# middle schools only
ela_proficiency_middle_schools_only_df.to_excel(
    'ela_proficiency_middle_schools_only.xlsx',
    index=False
)

# filter out all rows except preschools
ela_proficiency_preschools_only_df = preschools(ela_only_df)

# preschools only
ela_proficiency_preschools_only_df.to_excel(
    'ela_proficiency_preschools_only.xlsx',
    index=False
)

# populate missing values to = 0
ela_proficiency_charter_schools_only_df = \
    ela_proficiency_charter_schools_only_df.fillna(0)
ela_proficiency_elementary_schools_only_df = \
    ela_proficiency_elementary_schools_only_df.fillna(0)
ela_proficiency_high_schools_only_df = \
    ela_proficiency_high_schools_only_df.fillna(0)
ela_proficiency_middle_schools_only_df = \
    ela_proficiency_middle_schools_only_df.fillna(0)
ela_proficiency_preschools_only_df = \
    ela_proficiency_preschools_only_df.fillna('0')

# empty cells populated to = 0
ela_proficiency_charter_schools_only_df.\
    to_excel('ela_proficiency_charter_schools_only.xlsx', index=False)
ela_proficiency_elementary_schools_only_df.\
    to_excel('ela_proficiency_elementary_schools_only.xlsx', index=False)
ela_proficiency_high_schools_only_df.\
    to_excel('ela_proficiency_high_schools_only.xlsx', index=False)
ela_proficiency_middle_schools_only_df.\
    to_excel('ela_proficiency_middle_schools_only.xlsx', index=False)
ela_proficiency_preschools_only_df.\
    to_excel('ela_proficiency_preschools_only.xlsx', index=False) # all # isa proficiency values expected to be 0

# *TO BE DEVELOPED* - IN PROGRESS
# 1. create sheets per district size -> small, medium, large (create functions for each district size)
# 2. for loop to create extra status column (exclude preschools) for each district doc (ELA/MATH/SCIENCE)
def large_district_size(df):
    try:
        return df[df['District Size'] == 'LARGE']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with data not compliant to large_district_size()')

def medium_district_size(df):
    try:
        return df[df['District Size'] == 'MEDIUM']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with data not compliant to medium_district_size()')

def small_district_size(df):
    try:
        return df[df['District Size'] == 'SMALL']
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with data not compliant to small_district_size()')
#charter schools
ela_proficiency_charter_schools_large_district_size_only_df = \
    large_district_size(ela_proficiency_charter_schools_only_df)

ela_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

ela_proficiency_charter_schools_medium_district_size_only_df = \
    medium_district_size(ela_proficiency_charter_schools_only_df)

ela_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

ela_proficiency_charter_schools_small_district_size_only_df = \
    small_district_size(ela_proficiency_charter_schools_only_df)

ela_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_small_district_size_only.xlsx', index=False)
#elementary schools
ela_proficiency_elementary_schools_large_district_size_only_df = \
    large_district_size(ela_proficiency_elementary_schools_only_df)

ela_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

ela_proficiency_elementary_schools_medium_district_size_only_df = \
    medium_district_size(ela_proficiency_elementary_schools_only_df)

ela_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

ela_proficiency_elementary_schools_small_district_size_only_df = \
    small_district_size(ela_proficiency_elementary_schools_only_df)

ela_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)
#high schools
ela_proficiency_high_schools_large_district_size_only_df = \
    large_district_size(ela_proficiency_high_schools_only_df)

ela_proficiency_high_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_large_district_size_only.xlsx', index=False)

ela_proficiency_high_schools_medium_district_size_only_df = \
    medium_district_size(ela_proficiency_high_schools_only_df)

ela_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

ela_proficiency_high_schools_small_district_size_only_df = \
    small_district_size(ela_proficiency_high_schools_only_df)

ela_proficiency_high_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_small_district_size_only.xlsx', index=False)
#middle schools
ela_proficiency_middle_schools_large_district_size_only_df = \
    large_district_size(ela_proficiency_middle_schools_only_df)

ela_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

ela_proficiency_middle_schools_medium_district_size_only_df = \
    medium_district_size(ela_proficiency_middle_schools_only_df)

ela_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

ela_proficiency_middle_schools_small_district_size_only_df = \
    small_district_size(ela_proficiency_middle_schools_only_df)

ela_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_small_district_size_only.xlsx', index=False)
#preschools
ela_proficiency_preschools_large_district_size_only_df = \
    large_district_size(ela_proficiency_preschools_only_df)

ela_proficiency_preschools_large_district_size_only_df.\
    to_excel('ela_proficiency_preschools_large_district_size_only.xlsx', index=False)

ela_proficiency_preschools_medium_district_size_only_df = \
    medium_district_size(ela_proficiency_preschools_only_df)

ela_proficiency_preschools_medium_district_size_only_df.\
    to_excel('ela_proficiency_preschools_medium_district_size_only.xlsx', index=False)

ela_proficiency_preschools_small_district_size_only_df = \
    small_district_size(ela_proficiency_preschools_only_df)

ela_proficiency_preschools_small_district_size_only_df.\
    to_excel('ela_proficiency_preschools_small_district_size_only.xlsx', index=False)


# *FOR LOOP TO BE USED TO APPEND STATUS COLUMNS TO SHEETS* REF TO LINE 1153
#   charter schools + districts, elementary schools + districts,
#   high schools + districts, middle schools + districts
status = []

for student in ela_proficiency_charter_schools_large_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_charter_schools_large_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_charter_schools_medium_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_charter_schools_medium_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_charter_schools_small_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_charter_schools_small_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_charter_schools_small_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_elementary_schools_large_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_elementary_schools_large_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_elementary_schools_medium_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_elementary_schools_medium_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_elementary_schools_small_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_elementary_schools_small_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_high_schools_large_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_high_schools_large_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_high_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_large_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_high_schools_medium_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_high_schools_medium_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_high_schools_small_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_high_schools_small_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_high_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_high_schools_small_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_middle_schools_large_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_middle_schools_large_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_middle_schools_medium_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_middle_schools_medium_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in ela_proficiency_middle_schools_small_district_size_only_df['# ELA Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

ela_proficiency_middle_schools_small_district_size_only_df['# ELA Proficiency Status'] = status

ela_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('ela_proficiency_middle_schools_small_district_size_only.xlsx', index=False)

# add status column to ela_proficiency_preschools_only_df and set all values to = 'N/A'
ela_proficiency_preschools_only_df['# ELA Proficiency Status'] =\
    ['N/A'] * len(ela_proficiency_preschools_only_df)

ela_proficiency_preschools_only_df.\
    to_excel('ela_proficiency_preschools_only.xlsx', index=False)

# dataframe for math only
math_only_df = pd.DataFrame()
rcdts = ela_math_science_df.iloc[:,0]
math_only_df['RCDTS'] = rcdts.copy()
school_name = ela_math_science_df.iloc[:,2]
math_only_df['School Name'] = school_name.copy() # school name
city = ela_math_science_df.iloc[:,4]
math_only_df['City'] = city.copy()
county = ela_math_science_df.iloc[:,5]
math_only_df['County'] = county.copy()
district_size = ela_math_science_df.iloc[:,7]
math_only_df['District Size'] = district_size.copy()
school_type = ela_math_science_df.iloc[:,8]
math_only_df['School Type'] = school_type.copy()
math_proficiency_total_student = ela_math_science_df.iloc[:,46]
math_only_df['# Math Proficiency Total Student'] = \
    math_proficiency_total_student.copy()
math_proficiency_male = ela_math_science_df.iloc[:,47]
math_only_df['# Math Proficiency - Male'] = \
    math_proficiency_male.copy()
math_proficiency_female = ela_math_science_df.iloc[:,48]
math_only_df['# Math Proficiency - Female'] = \
    math_proficiency_female.copy()
math_proficiency_white = ela_math_science_df.iloc[:,49]
math_only_df['# Math Proficiency - White'] = \
    math_proficiency_white.copy()
math_proficiency_black_or_african_american = \
    ela_math_science_df.iloc[:,50]
math_only_df['# Math Proficiency - Black or African American'] = \
    math_proficiency_black_or_african_american.copy()
math_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,51]
math_only_df['# Math Proficiency - Hispanic or Latino'] = \
    math_proficiency_hispanic_or_latino.copy()
math_proficiency_asian = ela_math_science_df.iloc[:,52]
math_only_df['# Math Proficiency - Asian'] = \
    math_proficiency_asian.copy()
math_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,53]
math_only_df['# Math Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    math_proficiency_native_hawaiian_or_other_pacific_islander.copy()
math_proficiency_american_indian_or_alaska_native = ela_math_science_df.iloc[:,54]
math_only_df['# Math Proficiency - American Indian or Alaska Native'] = \
    math_proficiency_american_indian_or_alaska_native.copy()
math_proficiency_two_or_more_races = ela_math_science_df.iloc[:,55]
math_only_df['# Math Proficiency - Two or More Races'] = \
    math_proficiency_two_or_more_races.copy()
math_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,56]
math_only_df['# Math Proficiency - Children with Disabilities'] = \
    math_proficiency_children_with_disabilities.copy()

math_only_df.to_excel('math_only.xlsx', index=False)

math_only_df = delete_row(math_only_df)

math_only_df.to_excel('math_only.xlsx', index=False)
math_only_df.to_csv('math_only.csv', index=False)

# filter out all rows except high schools
math_proficiency_high_schools_only_df = high_schools(math_only_df)

# high schools only
math_proficiency_high_schools_only_df.to_excel(
    'math_proficiency_high_schools_only.xlsx',
    index=False
)

# filter out all rows except charter schools
math_proficiency_charter_schools_only_df = charter_schools(math_only_df)

# charter schools only
math_proficiency_charter_schools_only_df.to_excel(
    'math_proficiency_charter_schools_only.xlsx',
    index=False
)

# filter out all rows except elementary schools
math_proficiency_elementary_schools_only_df = elementary_schools(math_only_df)

# elementary schools only
math_proficiency_elementary_schools_only_df.to_excel(
    'math_proficiency_elementary_schools_only.xlsx',
    index=False
)

# filter out all rows except middle schools
math_proficiency_middle_schools_only_df = middle_schools(math_only_df)

# middle schools only
math_proficiency_middle_schools_only_df.to_excel(
    'math_proficiency_middle_schools_only.xlsx',
    index=False
)

# filter out all rows except preschools
math_proficiency_preschools_only_df = preschools(math_only_df)

# preschools only
math_proficiency_preschools_only_df.to_excel(
    'math_proficiency_preschools_only.xlsx',
    index=False
)

# populate missing values to = 0
math_proficiency_charter_schools_only_df = \
    math_proficiency_charter_schools_only_df.fillna(0)
math_proficiency_elementary_schools_only_df = \
    math_proficiency_elementary_schools_only_df.fillna(0)
math_proficiency_high_schools_only_df = \
    math_proficiency_high_schools_only_df.fillna(0)
math_proficiency_middle_schools_only_df = \
    math_proficiency_middle_schools_only_df.fillna(0)
math_proficiency_preschools_only_df = \
    math_proficiency_preschools_only_df.fillna('0')

# empty cells populated to = 0
math_proficiency_charter_schools_only_df.\
    to_excel('math_proficiency_charter_schools_only.xlsx', index=False)
math_proficiency_elementary_schools_only_df.\
    to_excel('math_proficiency_elementary_schools_only.xlsx', index=False)
math_proficiency_high_schools_only_df.\
    to_excel('math_proficiency_high_schools_only.xlsx', index=False)
math_proficiency_middle_schools_only_df.\
    to_excel('math_proficiency_middle_schools_only.xlsx', index=False)
math_proficiency_preschools_only_df.\
    to_excel('math_proficiency_preschools_only.xlsx', index=False) # all # math proficiency values expected to be 0

# *TO BE DEVELOPED* - IN PROGRESS
# 1. create sheets per district size -> small, medium, large (create functions for each district size)
# 2. for loop to create extra status column (exclude preschools) for each district doc (ELA/MATH/SCIENCE)
#charter schools
math_proficiency_charter_schools_large_district_size_only_df = \
    large_district_size(math_proficiency_charter_schools_only_df)

math_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

math_proficiency_charter_schools_medium_district_size_only_df = \
    medium_district_size(math_proficiency_charter_schools_only_df)

math_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

math_proficiency_charter_schools_small_district_size_only_df = \
    small_district_size(math_proficiency_charter_schools_only_df)

math_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_small_district_size_only.xlsx', index=False)
#elementary schools
math_proficiency_elementary_schools_large_district_size_only_df = \
    large_district_size(math_proficiency_elementary_schools_only_df)

math_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

math_proficiency_elementary_schools_medium_district_size_only_df = \
    medium_district_size(math_proficiency_elementary_schools_only_df)

math_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

math_proficiency_elementary_schools_small_district_size_only_df = \
    small_district_size(math_proficiency_elementary_schools_only_df)

math_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)
#high schools
math_proficiency_high_schools_large_district_size_only_df = \
    large_district_size(math_proficiency_high_schools_only_df)

math_proficiency_high_schools_large_district_size_only_df.\
    to_excel('math_proficiency_high_schools_large_district_size_only.xlsx', index=False)

math_proficiency_high_schools_medium_district_size_only_df = \
    medium_district_size(math_proficiency_high_schools_only_df)

math_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

math_proficiency_high_schools_small_district_size_only_df = \
    small_district_size(math_proficiency_high_schools_only_df)

math_proficiency_high_schools_small_district_size_only_df.\
    to_excel('math_proficiency_high_schools_small_district_size_only.xlsx', index=False)
#middle schools
math_proficiency_middle_schools_large_district_size_only_df = \
    large_district_size(math_proficiency_middle_schools_only_df)

math_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

math_proficiency_middle_schools_medium_district_size_only_df = \
    medium_district_size(math_proficiency_middle_schools_only_df)

math_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

math_proficiency_middle_schools_small_district_size_only_df = \
    small_district_size(math_proficiency_middle_schools_only_df)

math_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_small_district_size_only.xlsx', index=False)
#preschools
math_proficiency_preschools_large_district_size_only_df = \
    large_district_size(math_proficiency_preschools_only_df)

math_proficiency_preschools_large_district_size_only_df.\
    to_excel('math_proficiency_preschools_large_district_size_only.xlsx', index=False)

math_proficiency_preschools_medium_district_size_only_df = \
    medium_district_size(math_proficiency_preschools_only_df)

math_proficiency_preschools_medium_district_size_only_df.\
    to_excel('math_proficiency_preschools_medium_district_size_only.xlsx', index=False)

math_proficiency_preschools_small_district_size_only_df = \
    small_district_size(math_proficiency_preschools_only_df)

math_proficiency_preschools_small_district_size_only_df.\
    to_excel('math_proficiency_preschools_small_district_size_only.xlsx', index=False)


# *FOR LOOP TO BE USED TO APPEND STATUS COLUMNS TO SHEETS* REF TO LINE 1153
status = []

for student in math_proficiency_charter_schools_large_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_charter_schools_large_district_size_only_df['Status'] = status

math_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_charter_schools_medium_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_charter_schools_medium_district_size_only_df['Status'] = status

math_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_charter_schools_small_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_charter_schools_small_district_size_only_df['Status'] = status

math_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('math_proficiency_charter_schools_small_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_elementary_schools_large_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_elementary_schools_large_district_size_only_df['Status'] = status

math_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_elementary_schools_medium_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_elementary_schools_medium_district_size_only_df['Status'] = status

math_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_elementary_schools_small_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_elementary_schools_small_district_size_only_df['Status'] = status

math_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('math_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_high_schools_large_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_high_schools_large_district_size_only_df['Status'] = status

math_proficiency_high_schools_large_district_size_only_df.\
    to_excel('math_proficiency_high_schools_large_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_high_schools_medium_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_high_schools_medium_district_size_only_df['Status'] = status

math_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_high_schools_small_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_high_schools_small_district_size_only_df['Status'] = status

math_proficiency_high_schools_small_district_size_only_df.\
    to_excel('math_proficiency_high_schools_small_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_middle_schools_large_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_middle_schools_large_district_size_only_df['Status'] = status

math_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_middle_schools_medium_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_middle_schools_medium_district_size_only_df['Status'] = status

math_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in math_proficiency_middle_schools_small_district_size_only_df['# Math Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

math_proficiency_middle_schools_small_district_size_only_df['Status'] = status

math_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('math_proficiency_middle_schools_small_district_size_only.xlsx', index=False)


# add status column to math_proficiency_preschools_only_df and set all values to = 'N/A'
math_proficiency_preschools_only_df['Status'] =\
    ['N/A'] * len(math_proficiency_preschools_only_df)

math_proficiency_preschools_only_df.\
    to_excel('math_proficiency_preschools_only.xlsx', index=False)

# dataframe for science only
science_only_df = pd.DataFrame()
rcdts = ela_math_science_df.iloc[:,0]
science_only_df['RCDTS'] = rcdts.copy()
school_name = ela_math_science_df.iloc[:,2]
science_only_df['School Name'] = school_name.copy() # school name
city = ela_math_science_df.iloc[:,4]
science_only_df['City'] = city.copy()
county = ela_math_science_df.iloc[:,5]
science_only_df['County'] = county.copy()
district_size = ela_math_science_df.iloc[:,7]
science_only_df['District Size'] = district_size.copy()
school_type = ela_math_science_df.iloc[:,8]
science_only_df['School Type'] = school_type.copy()
science_proficiency_total_student = ela_math_science_df.iloc[:,208]
science_only_df['# Science Proficiency Total Student'] = \
    science_proficiency_total_student.copy()
science_proficiency_male = ela_math_science_df.iloc[:,209]
science_only_df['# Science Proficiency - Male'] = \
    science_proficiency_male.copy()
science_proficiency_female = ela_math_science_df.iloc[:,210]
science_only_df['# Science Proficiency - Female'] = \
    science_proficiency_female.copy()
science_proficiency_white = ela_math_science_df.iloc[:,211]
science_only_df['# Science Proficiency - White'] = \
    science_proficiency_white.copy()
science_proficiency_black_or_african_american = \
    ela_math_science_df.iloc[:,212]
science_only_df['# Science Proficiency - Black or African American'] = \
    science_proficiency_black_or_african_american.copy()
science_proficiency_hispanic_or_latino = ela_math_science_df.iloc[:,213]
science_only_df['# Science Proficiency - Hispanic or Latino'] = \
    science_proficiency_hispanic_or_latino.copy()
science_proficiency_asian = ela_math_science_df.iloc[:,214]
science_only_df['# Science Proficiency - Asian'] = \
    science_proficiency_asian.copy()
science_proficiency_native_hawaiian_or_other_pacific_islander = \
    ela_math_science_df.iloc[:,215]
science_only_df['# Science Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    science_proficiency_native_hawaiian_or_other_pacific_islander.copy()
science_proficiency_american_indian_or_alaska_native = \
    ela_math_science_df.iloc[:,216]
science_only_df['# Science Proficiency - American Indian or Alaska Native'] = \
    science_proficiency_american_indian_or_alaska_native.copy()
science_proficiency_two_or_more_races = ela_math_science_df.iloc[:,217]
science_only_df['# Science Proficiency - Two or More Races'] = \
    science_proficiency_two_or_more_races.copy()
science_proficiency_children_with_disabilities = ela_math_science_df.iloc[:,218]
science_only_df['# Science Proficiency - Children with Disabilities'] = \
    science_proficiency_children_with_disabilities.copy()

science_only_df.to_excel('science_only.xlsx', index=False)

science_only_df = delete_row(science_only_df)

science_only_df.to_excel('science_only.xlsx', index=False)
science_only_df.to_csv('science_only.csv', index=False)

# filter out all rows except high schools
science_proficiency_high_schools_only_df = high_schools(science_only_df)

# high schools only
science_proficiency_high_schools_only_df.to_excel(
    'science_proficiency_high_schools_only.xlsx',
    index=False
)

# filter out all rows except charter schools
science_proficiency_charter_schools_only_df = charter_schools(science_only_df)

# charter schools only
science_proficiency_charter_schools_only_df.to_excel(
    'science_proficiency_charter_schools_only.xlsx',
    index=False
)

# filter out all rows except elementary schools
science_proficiency_elementary_schools_only_df = elementary_schools(science_only_df)

# elementary schools only
science_proficiency_elementary_schools_only_df.to_excel(
    'science_proficiency_elementary_schools_only.xlsx',
    index=False
)

# filter out all rows except middle schools
science_proficiency_middle_schools_only_df = middle_schools(science_only_df)

# middle schools only
science_proficiency_middle_schools_only_df.to_excel(
    'science_proficiency_middle_schools_only.xlsx',
    index=False
)

# filter out all rows except preschools
science_proficiency_preschools_only_df = preschools(science_only_df)

# preschools only
science_proficiency_preschools_only_df.to_excel(
    'science_proficiency_preschools_only.xlsx',
    index=False
)

# populate missing values to = 0
science_proficiency_charter_schools_only_df = \
    science_proficiency_charter_schools_only_df.fillna(0)
science_proficiency_elementary_schools_only_df = \
    science_proficiency_elementary_schools_only_df.fillna(0)
science_proficiency_high_schools_only_df = \
    science_proficiency_high_schools_only_df.fillna(0)
science_proficiency_middle_schools_only_df = \
    science_proficiency_middle_schools_only_df.fillna(0)
science_proficiency_preschools_only_df = \
    science_proficiency_preschools_only_df.fillna('0')

# empty cells populated to = 0
science_proficiency_charter_schools_only_df.\
    to_excel('science_proficiency_charter_schools_only.xlsx', index=False)
science_proficiency_elementary_schools_only_df.\
    to_excel('science_proficiency_elementary_schools_only.xlsx', index=False)
science_proficiency_high_schools_only_df.\
    to_excel('science_proficiency_high_schools_only.xlsx', index=False)
science_proficiency_middle_schools_only_df.\
    to_excel('science_proficiency_middle_schools_only.xlsx', index=False)
science_proficiency_preschools_only_df.\
    to_excel('science_proficiency_preschools_only.xlsx', index=False) # all # sci proficiency values expected to = 0

# *TO BE DEVELOPED* - IN PROGRESS
# 1. create sheets per district size -> small, medium, large (create functions for each district size)
# 2. for loop to create extra status column (exclude preschools) for each district doc (ELA/MATH/SCIENCE)

#charter schools
science_proficiency_charter_schools_large_district_size_only_df = \
    large_district_size(science_proficiency_charter_schools_only_df)

science_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

science_proficiency_charter_schools_medium_district_size_only_df = \
    medium_district_size(science_proficiency_charter_schools_only_df)

science_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

science_proficiency_charter_schools_small_district_size_only_df = \
    small_district_size(science_proficiency_charter_schools_only_df)

science_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_small_district_size_only.xlsx', index=False)
#elementary schools
science_proficiency_elementary_schools_large_district_size_only_df = \
    large_district_size(science_proficiency_elementary_schools_only_df)

science_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

science_proficiency_elementary_schools_medium_district_size_only_df = \
    medium_district_size(science_proficiency_elementary_schools_only_df)

science_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

science_proficiency_elementary_schools_small_district_size_only_df = \
    small_district_size(science_proficiency_elementary_schools_only_df)

science_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)
#high schools
science_proficiency_high_schools_large_district_size_only_df = \
    large_district_size(science_proficiency_high_schools_only_df)

science_proficiency_high_schools_large_district_size_only_df.\
    to_excel('science_proficiency_high_schools_large_district_size_only.xlsx', index=False)

science_proficiency_high_schools_medium_district_size_only_df = \
    medium_district_size(science_proficiency_high_schools_only_df)

science_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

science_proficiency_high_schools_small_district_size_only_df = \
    small_district_size(science_proficiency_high_schools_only_df)

science_proficiency_high_schools_small_district_size_only_df.\
    to_excel('science_proficiency_high_schools_small_district_size_only.xlsx', index=False)
#middle schools
science_proficiency_middle_schools_large_district_size_only_df = \
    large_district_size(science_proficiency_middle_schools_only_df)

science_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

science_proficiency_middle_schools_medium_district_size_only_df = \
    medium_district_size(science_proficiency_middle_schools_only_df)

science_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

science_proficiency_middle_schools_small_district_size_only_df = \
    small_district_size(science_proficiency_middle_schools_only_df)

science_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_small_district_size_only.xlsx', index=False)
#preschools
science_proficiency_preschools_large_district_size_only_df = \
    large_district_size(science_proficiency_preschools_only_df)

science_proficiency_preschools_large_district_size_only_df.\
    to_excel('science_proficiency_preschools_large_district_size_only.xlsx', index=False)

science_proficiency_preschools_medium_district_size_only_df = \
    medium_district_size(science_proficiency_preschools_only_df)

science_proficiency_preschools_medium_district_size_only_df.\
    to_excel('science_proficiency_preschools_medium_district_size_only.xlsx', index=False)

science_proficiency_preschools_small_district_size_only_df = \
    small_district_size(science_proficiency_preschools_only_df)

science_proficiency_preschools_small_district_size_only_df.\
    to_excel('science_proficiency_preschools_small_district_size_only.xlsx', index=False)


# *FOR LOOP TO BE USED TO APPEND STATUS COLUMNS TO SHEETS* REF TO LINE 1153
status = []

for student in science_proficiency_charter_schools_large_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_charter_schools_large_district_size_only_df['Status'] = status

science_proficiency_charter_schools_large_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_large_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_charter_schools_medium_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_charter_schools_medium_district_size_only_df['Status'] = status

science_proficiency_charter_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_charter_schools_small_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_charter_schools_small_district_size_only_df['Status'] = status

science_proficiency_charter_schools_small_district_size_only_df.\
    to_excel('science_proficiency_charter_schools_small_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_elementary_schools_large_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_elementary_schools_large_district_size_only_df['Status'] = status

science_proficiency_elementary_schools_large_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_large_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_elementary_schools_medium_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_elementary_schools_medium_district_size_only_df['Status'] = status

science_proficiency_elementary_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_elementary_schools_small_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_elementary_schools_small_district_size_only_df['Status'] = status

science_proficiency_elementary_schools_small_district_size_only_df.\
    to_excel('science_proficiency_elementary_schools_small_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_high_schools_large_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_high_schools_large_district_size_only_df['Status'] = status

science_proficiency_high_schools_large_district_size_only_df.\
    to_excel('science_proficiency_high_schools_large_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_high_schools_medium_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_high_schools_medium_district_size_only_df['Status'] = status

science_proficiency_high_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_high_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_high_schools_small_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_high_schools_small_district_size_only_df['Status'] = status

science_proficiency_high_schools_small_district_size_only_df.\
    to_excel('science_proficiency_high_schools_small_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_middle_schools_large_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 20:
            status.append('Up to Standard')
        elif student >= 10 and student <= 19:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_middle_schools_large_district_size_only_df['Status'] = status

science_proficiency_middle_schools_large_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_large_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_middle_schools_medium_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 15:
            status.append('Up to Standard')
        elif student >= 10 and student <= 14:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_middle_schools_medium_district_size_only_df['Status'] = status

science_proficiency_middle_schools_medium_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_medium_district_size_only.xlsx', index=False)

status = []

for student in science_proficiency_middle_schools_small_district_size_only_df['# Science Proficiency Total Student']:
    try:
        if student >= 10:
            status.append('Up to Standard')
        elif student >= 5 and student <= 9:
            status.append('Moderate')
        else:
            status.append('Alarming')
    except:
        status.append('Not an appropriate value')

science_proficiency_middle_schools_small_district_size_only_df['Status'] = status

science_proficiency_middle_schools_small_district_size_only_df.\
    to_excel('science_proficiency_middle_schools_small_district_size_only.xlsx', index=False)

# add status column to math_proficiency_preschools_only_df and set all values to = 'N/A'
science_proficiency_preschools_only_df['Status'] =\
    ['N/A'] * len(science_proficiency_preschools_only_df)

science_proficiency_preschools_only_df.\
    to_excel('science_proficiency_preschools_only.xlsx', index=False)

# ela only total student per school type pivot table
ela_only_total_student_per_school_type_pivot_table_df = pd.pivot_table(
    ela_only_df,
    index='School Name',
    columns='School Type',
    values='# ELA Proficiency Total Student',
    aggfunc='sum'
)

ela_only_total_student_per_school_type_pivot_table_df.to_excel\
    ('ela_proficiency_total_student_pivot_table.xlsx') # 0 value populated for preschools

# ela only average per school type pivot table
ela_only_student_quantity_average_pivot_table_df = pd.pivot_table(
    ela_only_df,
    index='School Name',
    columns='School Type',
    values='# ELA Proficiency Total Student',
    aggfunc='mean'
)

ela_only_student_quantity_average_pivot_table_df.to_excel\
    ('ela_proficiency_student_quantity_average_pivot_table.xlsx') # preschools excluded

# ela only sum per district size pivot table
# index = school name, columns = district size, values = # ELA Proficiency - Black or African American
ela_only_black_or_african_american_student_total_pivot_table_df = pd.pivot_table(
    ela_only_df,
    index='School Name',
    columns='District Size',
    values='# ELA Proficiency - Black or African American',
    aggfunc='sum'
)

ela_only_black_or_african_american_student_total_pivot_table_df.to_excel\
    ('ela_only_black_or_african_american_student_total_pivot_table.xlsx')

# math only sum per district size pivot table
# index = school name, columns = district size, values = # Math Proficiency - Black or African American
math_only_black_or_african_american_student_total_pivot_table_df = pd.pivot_table(
    math_only_df,
    index='School Name',
    columns='District Size',
    values='# Math Proficiency - Black or African American',
    aggfunc='sum'
)

math_only_black_or_african_american_student_total_pivot_table_df.to_excel\
    ('math_only_black_or_african_american_student_total_pivot_table.xlsx')

# science only sum per district size pivot table
# index = school name, columns = district size,
# values = # Science Proficiency - Black or African American
science_only_black_or_african_american_student_total_pivot_table_df = pd.pivot_table(
    science_only_df,
    index='School Name',
    columns='District Size',
    values='# Science Proficiency - Black or African American',
    aggfunc='sum'
)

science_only_black_or_african_american_student_total_pivot_table_df.to_excel\
    ('science_only_black_or_african_american_student_total_pivot_table.xlsx')

# join columns on merge, left ->
# ex: math_only_black_or_african_american_student_total_pivot_table_df,
#     science_only_black_or_african_american_student_total_pivot_table_df
# on = 'District Size'
math_and_science_only_black_or_african_american_student_table = pd.merge(
    math_only_black_or_african_american_student_total_pivot_table_df,
    science_only_black_or_african_american_student_total_pivot_table_df,
    on='School Name'
)

math_and_science_only_black_or_african_american_student_table.to_excel(
    'math_and_science_only_black_or_african_american_student_table.xlsx'
)