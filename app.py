import streamlit as st
import requests
import pandas as pd

API_KEY = "dda13d8b986a418caac237bb175b4c02"  # ⚠️ 여기에 발급받은 API KEY 넣기

def get_school_code(school_name):
    url = f"https://open.neis.go.kr/hub/schoolInfo"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "SCHUL_NM": school_name
    }
    res = requests.get(url, params=params).json()
    
    try:
        info = res['schoolInfo'][1]['row'][0]
        return info['ATPT_OFCDC_SC_CODE'], info['SD_SCHUL_CODE'], info['SCHUL_NM']
    except:
        return None, None, None

def get_meal_info(edu_code, school_code, date):
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": edu_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": date
    }
    res = requests.get(url, params=params).json()
    
    try:
        meals = res['mealServiceDietInfo'][1]['row']
        meal_list = []
        for meal in meals:
            meal_list.append({
                "급식종류": meal["MMEAL_SC_NM"],
                "식단": meal["DDISH_NM"].replace("<br/>", "\n"),
                "칼로리": meal.get("CAL_INFO", "정보 없음")
            })
        return meal_list
    except:
        return []

# Streamlit UI
st.title("📚 급식 조회기")

school_name = st.text_input("학교 이름을 입력하세요", "서울고등학교")
date = st.date_input("날짜 선택")

if st.button("급식 정보 조회"):
    edu_code, school_code, found_name = get_school_code(school_name)
    if not edu_code:
        st.error("학교를 찾을 수 없습니다.")
    else:
        st.success(f"학교명: {found_name} | 코드: {edu_code}-{school_code}")
        meals = get_meal_info(edu_code, school_code, date.strftime("%Y%m%d"))
        if meals:
            for meal in meals:
                st.markdown(f"### 🍱 {meal['급식종류']}")
                st.text(meal['식단'])
                st.caption(f"칼로리: {meal['칼로리']}")
        else:
            st.warning("해당 날짜의 급식 정보가 없습니다.")
