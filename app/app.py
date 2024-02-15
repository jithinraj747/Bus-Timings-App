import pandas as pd
import json

import streamlit as st

# add absolute file paths or else streamlit will not recognise it

with open('places.json') as data:
    places = json.load(data)

with open('time_tables.json') as data:
    time_tables = json.load(data)

# a - boarding point, b - destination
def get_time_table(a,b):
    # filtering the list to contain only those dicts containing the inputs a,b as keys
    time_tables_new = [dict_element for dict_element in time_tables if {a, b}.issubset(list(dict_element.keys()))]

    # converting each dict in list to a tuple keyed dict so as to convert them to a multiindexed columned dataframe
    # then converting each dict to a dataframe and appending it to a list
    lst_new = []
    for dict_element in time_tables_new:
        dict_new = {}
        dict_new['Day', ''] = dict_element['Day']
        dict_new[(a, 'A')] = dict_element[a]['A']
        dict_new[(a, 'D')] = dict_element[a]['D']
        dict_new[(a, 'Via')] = dict_element[a]['Via']
        dict_new[(b, 'A')] = dict_element[b]['A']
        dict_new[(b, 'D')] = dict_element[b]['D']
        dict_new[(b, 'Via')] = dict_element[b]['Via']
        lst_new.append(pd.DataFrame(dict_new))

    # concatenating all the dataframes in the list
    df_new = pd.concat(lst_new, ignore_index=True)

    # filtering so that at least one of the A,D values must be non-null for each place
    df_new = df_new[(df_new[a].A.notnull() | df_new[a].D.notnull()) & (df_new[b].A.notnull() | df_new[b].D.notnull())]

    # we actually only need 'D','Via' columns of boarding point and 'A' column of destination for the final output
    # columnwise fillna between A,D columns of each place so that 'D' column of boarding point and 'A' column of destination is filled
    df_new.iloc[:,[2,1]] = df_new.iloc[:,[2,1]].bfill(axis=1)
    df_new.iloc[:,[-3,-2]] = df_new.iloc[:,[-3,-2]].bfill(axis=1)

    # clipping the first single column and last two columns since they are not needed in the output
    df_new = df_new.iloc[:, 2:-2]

    # changing the dtypes of 'D','A' to time formats so as to compare and remove those rows having reversed order of time
    df_new.iloc[:, 0] = pd.to_datetime(df_new.iloc[:, 0], format='%I:%M %p')
    df_new.iloc[:, -1] = pd.to_datetime(df_new.iloc[:, -1], format='%I:%M %p')

    # removing all rows with reversed time order
    df_new = df_new[df_new.iloc[:, 0] < df_new.iloc[:, -1]]

    # sorting the data based on the 'D' (departure) timings of [a] (boarding point)
    df_new.sort_values(by=(a, 'D'), inplace=True, ignore_index=True)

    # correcting the index so as to start from 1
    df_new.index += 1

    # time format changing (using .df.strftime) can only be done to produce new columns in the same dataframe based on existing columns
    # creating and adding two new dummy columns: 'test1' and 'test2'
    df_new['test1'] = pd.to_datetime(df_new.iloc[:, 0])
    df_new['test2'] = pd.to_datetime(df_new.iloc[:, 2])
    df_new['test1'] = df_new['test1'].dt.strftime('%I:%M %p')
    df_new['test2'] = df_new['test2'].dt.strftime('%I:%M %p')

    # creating a new dataframe based on the time formatted two new columns and 'Via' column of [a]
    # changing the 'A' and 'D' to 'Arrival' and 'Departure'
    df_final = pd.DataFrame(columns=pd.MultiIndex.from_tuples([(a,'Departure'),(a,'Via'),(b,'Arrival')]))
    df_final[(a, 'Departure')] = df_new['test1']
    df_final[(a, 'Via')] = df_new[(a, 'Via')]
    df_final[(b, 'Arrival')] = df_new['test2']
    
    # removing null value columns if any ('Via' column might be all null in most cases)
    df_final = df_final.dropna(axis=1, how='all')

    return df_final

def main():

    st.title('Bus Timings')

    a = st.selectbox('Boarding point: ',places)
    b = st.selectbox('Destination: ',places)

    if st.button('Search'):
        try:
            st.success(st.dataframe(get_time_table(a, b)))
        except:
            st.error('There are no bus routes.')


if __name__ == '__main__':
    main()
