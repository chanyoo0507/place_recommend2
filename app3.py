import streamlit as st
import pandas as pd

def load_file():
    uploaded_file = st.file_uploader("장소 데이터 엑셀 파일을 업로드하세요",type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        st.info("엑셀 파일을 업로드하면 데이터가 표시됩니다")

def print_table(table, table_name):
    st.subheader(table_name)
    if len(table)>0:
        st.dataframe(table)
    else:
        st.warning("출력할 장소가 없습니다")

def menu_select():
    selected_menu = st.sidebar.radio("사용 기능 선택하기",["전체 보기","검색하기","통계 보기"])
    return selected_menu
    
def how_to_search():
    selected_keys = []
    st.subheader("검색 기준 선택하기")
    for i in df.columns:
        if i == "place_id" or "이름":
            continue
        selected = st.checkbox(i)
        if selected == True:
            selected_keys.append[i]
    return selected_keys

def search_by_key(key):
    if pd.api.types.is_numeric_dtype(df[key]):
        selected_key = st.number_input
    else:
        selected_key = st.selectbox(key+"을 선택하세요",df[key].unique())
        return df[(df[key] == selected_key)]
        
    

def search_place():
    selected_region = st.selectbox("지역을 선택하세요",df["지역"].unique())
    selected_budget = st.number_input("사용 가능한 예산을 입력하세요", min_value=0,value=10000,step=1000)
    selected_indoor = st.radio("실내 여부를 선택하세요", df["실내여부"].unique())
    result=df[(df["지역"] == selected_region) & (df["예산"] <= selected_budget) & (df["실내여부"] == selected_indoor)]
    return result

def count_chart(key):
    key_count = df[key].value_counts()
    st.subheader(key+"별 장소 개수")
    st.bar_chart(key_count)

def average_chart(group, num):
    avg_score = df.groupby(group)[num].mean()
    st.subheader(group+"별 평균"+num)
    st.bar_chart(avg_score)

st.title("강생도 2.0")
st.write("엑셀 파일을 업로드하면 장소 데이터를 확인할 수 있습니다.")

df = load_file()
if df is not None:
    menu = menu_select()
    if menu == "전체 보기":
        print_table(df,"업로드한 장소 데이더")
    if menu == "검색하기":
        search_result = search_place()
        print_table(search_result,"추천 결과")
    if menu == "통계 보기":
        count_chart("지역")
        count_chart("유형")
        average_chart("지역","평점")
