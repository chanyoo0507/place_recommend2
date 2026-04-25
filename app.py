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

def place_search_by_category(place_list,key,value):
    result = []
    for place in place_list:
        if (place[key] == value or value == "전부"):
            result.append(place)
    return result

def place_search_by_number(place_list,key,value,mode):
    result = []
    for place in place_list:
        if mode == "전부" or (mode == "기준 이상", place[key] >= value) or (mode == "기준 이하", place[key] <= value):
            result.append(place)
    return result

def place_add(place_list,name,indoor,cost,rate,open,close,population):
    new_place = {
        "이름": name,
        "실내여부": indoor,
        "예산": cost,
        "평점": rate,
        "개장시간": open,
        "폐장시간": close,
        "평균인파": population
    }
    place_list.append(new_place)

