import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)

def how_to_search(df):
    keys=[]
    st.sidebar.subheader("검색 기준 선택")
    for key in df.columns:
        if key != "추천ID" and key != "place_id":
            is_key_selected = st.sidebar.checkbox(key)
            if is_key_selected:
                keys.append(key)
    return keys

def search_recommendations(df,keys):
    st.subheader("추천 장소 검색")

    selected_key={}
    for key in keys:
        if pd.api.types.is_numeric_dtype(df[key]):
            if key == "예산":
                selected_key[key] = st.number_input(
                    "최대 예산",
                    min_value=0,
                    value=10000,
                    step=1000
                )
            elif key == "평점":
                selected_key[key] = st.number_input(
                    "최소 평점",
                    min_Value=0.0,
                    value=4.0,
                    step=0.1
                )
        else:
            selected_key.append[key] = st.selectbox(key+"선택",df[key].unique())
    #selected_region = st.selectbox("지역 선택", df["지역"].unique())
    #selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    #selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    #selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())

    result = df
    for key, selection in selected_key:
        if pd.api.types.is_numeric_dtype(df[key]):
            if key == "예산":
                result = result[(result[key] <= selection)]
            if key == "평점":
                result = result[(result[key] >= selection)]
        else:
            result = result[(result[key] == selection)]
    #result = df[
    #    (df["지역"] == selected_region) &
    #    (df["추천목적"] == selected_purpose) &
    #    (df["추천상황"] == selected_situation) &
    #    (df["추천대상"] == selected_target) &
    #    (df["예산"] <= selected_budget)
    #]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_keys = how_to_search(merged_df)
        search_recommendations(merged_df,search_keys)

    elif menu == "데이터 시각화":
        show_chart(merged_df)
