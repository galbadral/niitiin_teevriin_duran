import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import altair as alt
import pydeck as pdk
import streamlit as st
from PIL import Image
import datetime 
from datetime import datetime
    
st.header('\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\n\n## Улаанбаатарын нийтийн тээврийг дурандах нь!\n Д.Галбадрал, Дата Дуран Дататон\n\n## \U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C')
@st.cache_resource
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

tab1, tab2 = st.tabs(["Далай", "Сүхээ"])

#with col2:
with tab1:
    col1,col2 = st.columns(2)
    day = col1.selectbox(
        'Долоо хоногийн ямар гараг вэ?',
        ('Даваа', 'Мягмар', 'Лхагва','Пүрэв','Баасан','Бямба','Ням'))

    if day == 'Даваа':
        day = 1
    elif day == 'Мягмар':
        day = 2
    elif day == 'Лхагва':
        day= 3
    elif day == 'Пүрэв':
        day = 4
    elif day == 'Баасан':
        day= 5
    elif day == 'Бямба':
        day = 6
    elif day == 'Ням':
        day= 7

    df= load_data("merged_df"+str(day)+".csv.gz")

    hour = col2.selectbox(
        'Та хэдэн цагаас автобусанд суух вэ?',
        (np.arange(6,23)),index=12)

    bus_stops=df['bus_stop'].unique()

    bus_stop = col1.selectbox(
        'Та ямар буудлаас суух вэ?',
        (bus_stops),index=40)

    #To find buses that will come at that stop and time
    bus_stop_at_hour= df.loc[(df['bus_stop']==bus_stop) & (df['hour']==hour)]
    bus_stop_at_hour = bus_stop_at_hour.drop_duplicates(subset='id')
    routes_option = bus_stop_at_hour['bus_number'].drop_duplicates()
    #routes_option = routes_option.values()

    picked_route = col2.selectbox(
        'Та ямар чиглэлийн автобусанд суух вэ?',
        (routes_option))#index=6)

    bus_route_at_hour=bus_stop_at_hour.loc[bus_stop_at_hour['bus_number']==picked_route]
    direction_picker=bus_route_at_hour['direction'].drop_duplicates()

    bus_stop = col1.selectbox(
        'Та аль зүгрүү яах вэ?',
        (direction_picker))
    buses_at_hour=bus_route_at_hour.loc[bus_route_at_hour['direction'].isin(direction_picker)]


    bus_picker= buses_at_hour['time'].values

    bus_picked = col2.selectbox(
        'Та аль автобусанд нь суух вэ?',
        (bus_picker))

    bus=buses_at_hour.loc[buses_at_hour['time'].astype(str)==bus_picked].reset_index(drop=True)

    bus_id=bus.loc[0,'id']

    unique_bus=df.loc[df['id']==bus_id].reset_index(drop=True)

    on_board_index=unique_bus.loc[(unique_bus['time'].astype(str)==bus_picked)].index[0]

    unique_bus = unique_bus[on_board_index:]

    last_stop_index=unique_bus.drop_duplicates(subset='direction')

    #last_stop_index_new=last_stop_index.reset_index()

    last_stop_index=last_stop_index.index[1]

    unique_bus=unique_bus[:last_stop_index]

    bus_stop_indexes=unique_bus.drop_duplicates(subset='bus_stop').index

    bus_stop_names=unique_bus.drop_duplicates(subset='bus_stop')['bus_stop'].values


    #BREAKK
    #if st.button('Автобусандаа суух'):


        #progress_text = "Та автобусандаа амжилттай суулаа!\U0001F609 \nАвтобус хөдөлтөл түр хүлээнэ үү!\U0001F97A"
        #my_bar = st.progress(0, text=progress_text)


        #for percent_complete in range(100):
            #time.sleep(0.03)
            #my_bar.progress(percent_complete + 1, text=progress_text)



    off_bus_name=''
    off_bus_index=0
    how_many_stops_to_go=0

    #if st.button('Болсон!'):



    #progress_text = "Та автобусандаа амжилттай суулаа!\U0001F609 \nАвтобус хөдөлтөл түр хүлээнэ үү!\U0001F97A"
    #my_bar = st.progress(0, text=progress_text)



    #for percent_complete in range(100):
    #    time.sleep(0.03)
     #   my_bar.progress(percent_complete + 1, text=progress_text) 

    image = Image.open('line2.png')

    st.image(image)

    col_1,col_2 = st.columns(2)
    genre = col_1.radio(
    "Та буух буудлаа буудлын нэрээрээ сонгох уу? \nЭсвэл буудлаараа сонгох уу?",
    ('Буудал сонгох', 'Хэдэн буудал явахаа сонгох'),index=1)
    if genre == 'Буудал сонгох':
        to_show_stops=bus_stop_names[1:]

        off_bus_name = col_2.selectbox(
            'Та аль буудал дээр буух вэ?',
            (to_show_stops),index=5)

        #how_many_stops_to_go = np.where(bus_stop_names == off_bus_name)[0].item()
        bus_stop_dict = {stop_name: index for index, stop_name in enumerate(bus_stop_names)}
        how_many_stops_to_go = bus_stop_dict[off_bus_name]
        #how_many_stops_to_go = bus_stop_names.tolist().index(off_bus_name)
        off_bus_index=bus_stop_indexes[how_many_stops_to_go]

    else:
        bus_stops_left=len(bus_stop_indexes)-1
        to_show_how_many =np.arange(1,14)

        how_many_stops_to_go = col_2.selectbox(
            'Та хэдэн буудал явах вэ?',
            (to_show_how_many),index=5)

        off_bus_name = bus_stop_names[how_many_stops_to_go]
        off_bus_index = bus_stop_indexes[how_many_stops_to_go]

    st.image(image)
    #BREAKKK
    coll1,coll2,coll3 = st.columns((1,4,1))
    if coll2.button('\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C Намайг дар!\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C'):
        progress_text = "Автобус замдаа явж байна!\U0001F609 \nТа "+str(how_many_stops_to_go)+" буудлын дараа "+str(off_bus_name)+" буудал дээр бууна. Та түр хүлээнэ үү!\U0001F97A"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.025)
            my_bar.progress(percent_complete + 1, text=progress_text)
        bus_stop_names_unique=bus_stop_names[:(how_many_stops_to_go+1)]
        bus_stop_indexes_unique=bus_stop_indexes[:(how_many_stops_to_go+1)]

        unique_bus=unique_bus[:(off_bus_index+1)]



        total_sec=0
        total_person_added=0


        cap= str(unique_bus['capacity'].iloc[0])
        seats=str(unique_bus['seats'].iloc[0])
        type1=str(unique_bus['bus_type'].iloc[0])
        st.write("\U0001F68C Төрөл:------ "+type1)
        st.write("\U0001F925 Багтаамж:--- "+cap)
        st.write("\U0001F644 Суудлын тоо: "+seats)
        st.write(" ")


        for i in range(0,len(bus_stop_indexes_unique)-1):
            st.write("\n###### ",str(i)+")\U0001F6D1",bus_stop_names_unique[i]+"-----------\U0001F55B Цаг:",unique_bus['time'][bus_stop_indexes_unique[i].item()])
            st.write(" ")

            #SHOWING THE PEOPLE ENTERED
            a=bus_stop_indexes_unique[i+1].item()
            b=bus_stop_indexes_unique[i].item()

            people_entered = a-b
            #people_entered = bus_stop_indexes_unique[i+1]-bus_stop_indexes_unique[i]
            total_person_added=total_person_added+people_entered

            st.write("-------------------\U0001F6B6 ","Суусан хүмүүс:",people_entered," Нийт:",total_person_added)    

            #SHOWING TIME SPENT
            unique_bus['date/time']=pd.to_datetime(unique_bus['date/time'])
            time_spent = unique_bus['date/time'][bus_stop_indexes_unique[i+1].item()] - unique_bus['date/time'][bus_stop_indexes_unique[i].item()]

            # Convert the timestamps to datetime objects
            #timestamp1 = dt.strptime(unique_bus['date/time'][bus_stop_indexes_unique[i].item()], '%Y-%m-%d %H:%M:%S')
            #timestamp2 = dt.strptime(unique_bus['date/time'][bus_stop_indexes_unique[i+1].item()], '%Y-%m-%d %H:%M:%S')

            # Calculate the time difference in seconds
            #time_spent_sec = (timestamp2 - timestamp1).total_seconds()

            # convert the duration to seconds
            time_spent_sec = abs(time_spent.total_seconds())
            total_sec=total_sec+time_spent_sec

            m, s = divmod(time_spent_sec, 60)
            st.write("-------------------\U0001F647","Хоорондын хугацаа:", "{:2d} минут,{:2d} секунд".format(int(m), int(s)))

            st.write(" ")

            if i== len(bus_stop_indexes_unique)-2:
                st.write("\n##### ",str(i)+")\U0001F68D",bus_stop_names_unique[i+1],)
                st.write("-------------------\U0001F55B Цаг:",unique_bus['time'][bus_stop_indexes_unique[i+1].item()])

        m, s = divmod(total_sec, 60)
        h, m = divmod(m, 60)
        st.write("\n### Нийт зарцуулсан хугацаа:", "{:2d} цаг,{:02d} минут,{:02d} секунд".format(int(h), int(m), int(s)))
        st.write("### Нийт суусан хүмүүс:", total_person_added)
      
    else:
        st.caption('Жолоочоо алив ээ!')
        
        
        
    
    
        
with tab2:
    colll1,colll2 = st.columns(2)
    day = colll1.selectbox(
        'Долоо хоногийн ямар гараг вэ?',
        ('Даваа', 'Мягмар', 'Лхагва','Пүрэв','Баасан','Бямба','Ням'),key='Сүх')

    if day == 'Даваа':
        day = 1
    elif day == 'Мягмар':
        day = 2
    elif day == 'Лхагва':
        day= 3
    elif day == 'Пүрэв':
        day = 4
    elif day == 'Баасан':
        day= 5
    elif day == 'Бямба':
        day = 6
    elif day == 'Ням':
        day= 7

    df= load_data("merged_df"+str(day)+".csv.gz")

    hour = colll2.selectbox(
        'Та хэдэн цагаас автобусанд суух вэ?',
        (np.arange(6,23)),index=12,key='Сүх1')

    bus_stops=df['bus_stop'].unique()

    bus_stop = colll1.selectbox(
        'Та ямар буудлаас суух вэ?',
        (bus_stops),index=40,key='Сүх2')

    #To find buses that will come at that stop and time
    bus_stop_at_hour= df.loc[(df['bus_stop']==bus_stop) & (df['hour']==hour)]
    bus_stop_at_hour = bus_stop_at_hour.drop_duplicates(subset='id')
    routes_option = bus_stop_at_hour['bus_number'].drop_duplicates()
    #routes_option = routes_option.values()

    picked_route = colll2.selectbox(
        'Та ямар чиглэлийн автобусанд суух вэ?',
        (routes_option),key='Сүх3')

    bus_route_at_hour=bus_stop_at_hour.loc[bus_stop_at_hour['bus_number']==picked_route]
    direction_picker=bus_route_at_hour['direction'].drop_duplicates()

    bus_stop = colll1.selectbox(
        'Та аль зүгрүү яах вэ?',
        (direction_picker),key='Сүх4')
    buses_at_hour=bus_route_at_hour.loc[bus_route_at_hour['direction'].isin(direction_picker)]


    bus_picker= buses_at_hour['time'].values

    bus_picked = colll2.selectbox(
        'Та аль автобусанд нь суух вэ?',
        (bus_picker),key='Сүх5')

    bus=buses_at_hour.loc[buses_at_hour['time'].astype(str)==bus_picked].reset_index(drop=True)

    bus_id=bus.loc[0,'id']

    unique_bus=df.loc[df['id']==bus_id].reset_index(drop=True)

    on_board_index=unique_bus.loc[(unique_bus['time'].astype(str)==bus_picked)].index[0]

    unique_bus = unique_bus[on_board_index:]

    last_stop_index=unique_bus.drop_duplicates(subset='direction')

    #last_stop_index_new=last_stop_index.reset_index()

    last_stop_index=last_stop_index.index[1]

    unique_bus=unique_bus[:last_stop_index]

    bus_stop_indexes=unique_bus.drop_duplicates(subset='bus_stop').index

    bus_stop_names=unique_bus.drop_duplicates(subset='bus_stop')['bus_stop'].values


    #BREAKK
    #if st.button('Автобусандаа суух'):


        #progress_text = "Та автобусандаа амжилттай суулаа!\U0001F609 \nАвтобус хөдөлтөл түр хүлээнэ үү!\U0001F97A"
        #my_bar = st.progress(0, text=progress_text)


        #for percent_complete in range(100):
            #time.sleep(0.03)
            #my_bar.progress(percent_complete + 1, text=progress_text)



    off_bus_name=''
    off_bus_index=0
    how_many_stops_to_go=0

    #if st.button('Болсон!'):



    #progress_text = "Та автобусандаа амжилттай суулаа!\U0001F609 \nАвтобус хөдөлтөл түр хүлээнэ үү!\U0001F97A"
    #my_bar = st.progress(0, text=progress_text)



    #for percent_complete in range(100):
    #    time.sleep(0.03)
     #   my_bar.progress(percent_complete + 1, text=progress_text) 

    image = Image.open('line2.png')

    st.image(image)

    col__1,col__2 = st.columns(2)
    genre = col__1.radio(
    "Та буух буудлаа буудлын нэрээрээ сонгох уу? \nЭсвэл буудлаараа сонгох уу?",
    ('Буудал сонгох', 'Хэдэн буудал явахаа сонгох'),index=1,key='Сүх6')
    if genre == 'Буудал сонгох':
        to_show_stops=bus_stop_names[1:]

        off_bus_name = col__2.selectbox(
            'Та аль буудал дээр буух вэ?',
            (to_show_stops),index=5,key='Сүх7')

        #how_many_stops_to_go = np.where(bus_stop_names == off_bus_name)[0].item()
        bus_stop_dict = {stop_name: index for index, stop_name in enumerate(bus_stop_names)}
        how_many_stops_to_go = bus_stop_dict[off_bus_name]
        #how_many_stops_to_go = bus_stop_names.tolist().index(off_bus_name)
        off_bus_index=bus_stop_indexes[how_many_stops_to_go]

    else:
        bus_stops_left=len(bus_stop_indexes)-1
        to_show_how_many =np.arange(1,14)

        how_many_stops_to_go = col__2.selectbox(
            'Та хэдэн буудал явах вэ?',
            (to_show_how_many),index=5,key='Сүх8')

        off_bus_name = bus_stop_names[how_many_stops_to_go]
        off_bus_index = bus_stop_indexes[how_many_stops_to_go]

    st.image(image)
    #BREAKKK
    collll1,collll2,collll3 = st.columns((1,2,1))
    #if collll2.button('\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\n\nУлаанбаатарын автобусанд сууж үзэцгээе!\n\n Та бэлэн үү!\n\n\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E\U0001F68C\U0001F68C\U0001F68E',key='Сүх9'):
    progress_text = "Автобус замдаа явж байна!\U0001F609 \nТа "+str(how_many_stops_to_go)+" буудлын дараа "+str(off_bus_name)+" буудал дээр бууна. Та түр хүлээнэ үү!\U0001F97A"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1, text=progress_text)
    bus_stop_names_unique=bus_stop_names[:(how_many_stops_to_go+1)]
    bus_stop_indexes_unique=bus_stop_indexes[:(how_many_stops_to_go+1)]

    unique_bus=unique_bus[:(off_bus_index+1)]



    total_sec=0
    total_person_added=0


    cap= str(unique_bus['capacity'].iloc[0])
    seats=str(unique_bus['seats'].iloc[0])
    type1=str(unique_bus['bus_type'].iloc[0])
    st.write("\U0001F68C Төрөл:------ "+type1)
    st.write("\U0001F925 Багтаамж:--- "+cap)
    st.write("\U0001F644 Суудлын тоо: "+seats)
    st.write(" ")


    for i in range(0,len(bus_stop_indexes_unique)-1):
        st.write("\n###### ",str(i)+")\U0001F6D1",bus_stop_names_unique[i]+"-----------\U0001F55B Цаг:",unique_bus['time'][bus_stop_indexes_unique[i].item()])
        st.write(" ")

        #SHOWING THE PEOPLE ENTERED
        a=bus_stop_indexes_unique[i+1].item()
        b=bus_stop_indexes_unique[i].item()

        people_entered = a-b
        #people_entered = bus_stop_indexes_unique[i+1]-bus_stop_indexes_unique[i]
        total_person_added=total_person_added+people_entered

        st.write("-------------------\U0001F6B6 ","Суусан хүмүүс:",people_entered," Нийт:",total_person_added)    

        #SHOWING TIME SPENT
        unique_bus['date/time']=pd.to_datetime(unique_bus['date/time'])
        time_spent = unique_bus['date/time'][bus_stop_indexes_unique[i+1].item()] - unique_bus['date/time'][bus_stop_indexes_unique[i].item()]

        # Convert the timestamps to datetime objects
        #timestamp1 = dt.strptime(unique_bus['date/time'][bus_stop_indexes_unique[i].item()], '%Y-%m-%d %H:%M:%S')
        #timestamp2 = dt.strptime(unique_bus['date/time'][bus_stop_indexes_unique[i+1].item()], '%Y-%m-%d %H:%M:%S')

        # Calculate the time difference in seconds
        #time_spent_sec = (timestamp2 - timestamp1).total_seconds()

        # convert the duration to seconds
        time_spent_sec = abs(time_spent.total_seconds())
        total_sec=total_sec+time_spent_sec

        m, s = divmod(time_spent_sec, 60)
        st.write("-------------------\U0001F647","Хоорондын хугацаа:", "{:2d} минут,{:2d} секунд".format(int(m), int(s)))

        st.write(" ")

        if i== len(bus_stop_indexes_unique)-2:
            st.write("\n##### ",str(i)+")\U0001F68D",bus_stop_names_unique[i+1],)
            st.write("-------------------\U0001F55B Цаг:",unique_bus['time'][bus_stop_indexes_unique[i+1].item()])

    m, s = divmod(total_sec, 60)
    h, m = divmod(m, 60)
    st.write("\n### Нийт зарцуулсан хугацаа:", "{:2d} цаг,{:02d} минут,{:02d} секунд".format(int(h), int(m), int(s)))
    st.write("### Нийт суусан хүмүүс:", total_person_added)
    for_graph1=unique_bus[['date/time','X','Y']]
#else:
    #st.caption('Жолоочоо алив ээ!')