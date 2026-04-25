import streamlit as st

if "places" not in st.session_state:
    st.session_state.places = [
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
        if mode == "전부" or (mode == "기준 이상" and place[key] >= value) or (mode == "기준 이하" and place[key] <= value):
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

def place_search_by_number_total(result_input,key,min,step_value):
    mode = st.radio(key + " 검색 기준을 선택하세요", ["전부", "기준 이상", "기준 이하"])
    if mode != "전부":
        value = st.number_input(key + "을(를) 입력하세요",min_value=min, step=step_value)
        result = place_search_by_number(result_input,key,value,mode)
        return result
    else:
        return result_input

st.title("강원생활도우미앱")

menu = st.selectbox("기능을 선택하세요", ["전체 보기", "추천 받기", "장소 추가"])

if menu == "전체 보기":
    st.subheader("전체 결과")
    place_output(st.session_state.places)
elif menu == "추천 받기":
    indoor = st.selectbox("실내여부를 선택하세요", ["전부", "실내", "실외"])
    result = place_search_by_category(st.session_state.places,"실내여부",indoor)
    result = place_search_by_number_total(result,"비용",0,1000)
    result = place_search_by_number_total(result,"평점",0.0,0.1)
    time_mode = st.radio("방문 시간 검색 방식을 선택하세요", ["전부", "선택"])
    if time_mode != "전부":
        time = st.number_input("방문 시각을 입력하세요",min_value=0, step=1,max_value=24)
        result = place_search_by_number(result,"개장시간",time,"기준 이하")
        result = place_search_by_number(result,"폐장시간",time,"기준 이상")
    result = place_search_by_number_total(result,"평균인파",0,1000)
    st.subheader("추천 결과")
    place_output(result)
elif menu == "장소 추가":
    name = st.text_input("장소 이름을 입력하세요")
    indoor = st.selectbox("실내/실외를 선택하세요", ["실내", "실외"])
    cost = st.number_input("새 장소의 예산을 입력하세요", min_value=0, step=1000)
    rate = st.number_input("새 장소의 평점을 입력하세요", min_value=0.0, step=0.1, max_value=5.0)
    open = st.number_input("새 장소의 개장시간을 입력하세요", min_value=0, step=1, max_value=24)
    close = st.number_input("새 장소의 폐장시간을 입력하세요", min_value=0, step=1, max_value=24)
    population = st.number_input("새 장소의 평균인파를 입력하세요", min_value=0, step=1000)

    if st.button("장소 추가"):
        place_add(st.session_state.places,name,indoor,cost,rate,open,close,population)
        st.success("새 장소가 추가되었습니다")
