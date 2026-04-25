import streamlit as st

places = [
    {"이름":"속초 해수욕장","실내여부":"실외","비용":0,"평점":4.3,"개장시간":9,"폐장시간":18,"평균인파":15000},
    {"이름":"엑스포공원","실내여부":"실외","비용":0,"평점":4.5,"개장시간":0,"폐장시간":24,"평균인파":3000},
    {"이름":"속초 중앙시장","실내여부":"실내","비용":10000,"평점":4,"개장시간":8,"폐장시간":24,"평균인파":18000},
    {"이름":"설악산","실내여부":"실외","비용":0,"평점":4.7,"개장시간":3,"폐장시간":15,"평균인파":6000}
]

def place_output(result):
    if result == []:
        st.write("조건에 맞는 장소가 없습니다")
    else:
        for place in result:
            for key in place:
                st.write(key, " : ", place[key])
            st.write("---")

def place_search(place_list,indoor,cost,rate,visit_time,population):
    result = []
    for place in place_list:
        if (place["실내여부"] == indoor or indoor == "전부") and place["비용"] <= cost:
            result.append(place)
