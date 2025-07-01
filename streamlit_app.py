import pandas as pd
import streamlit as st
import altair as alt

# 페이지 기본 설정
st.set_page_config(page_title="연령대별 장르 분석", layout="wide")

# CSV 경로
csv_path = "연령대별_장르_선호_및_평점.csv"

# 데이터 불러오기
df = pd.read_csv(csv_path)

# 제목
st.title("📊 연령대별 장르 선호 및 평점 분석")

# 연령대 선택
age_group = st.selectbox("👶 연령대를 선택하세요:", sorted(df["age_group"].unique()))

# 해당 연령대 필터링
filtered = df[df["age_group"] == age_group]

# 시청 수 기준 Top 5
top_watch = filtered.sort_values(by="watch_count", ascending=False).head(5)

# 평균 평점 기준 Top 5
top_rating = filtered.sort_values(by="avg_rating", ascending=False).head(5)

# 📺 시청 수 시각화
st.subheader(f"📺 {age_group} 연령대가 자주 본 장르 Top 5")
chart_watch = alt.Chart(filtered).mark_bar().encode(
    x=alt.X("genres:N", title="장르", sort="-y"),
    y=alt.Y("watch_count:Q", title="시청 수"),
    color=alt.condition(
        alt.FieldOneOfPredicate(field="genres", oneOf=top_watch["genres"].tolist()),
        alt.value("orange"),
        alt.value("lightgray")
    ),
    tooltip=["genres", "watch_count"]
).properties(width=700, height=400)

st.altair_chart(chart_watch)

# ⭐ 평균 평점 시각화
st.subheader(f"⭐ {age_group} 연령대가 높게 평가한 장르 Top 5")
chart_rating = alt.Chart(filtered).mark_bar().encode(
    x=alt.X("genres:N", title="장르", sort="-y"),
    y=alt.Y("avg_rating:Q", title="평균 평점"),
    color=alt.condition(
        alt.FieldOneOfPredicate(field="genres", oneOf=top_rating["genres"].tolist()),
        alt.value("blue"),
        alt.value("lightgray")
    ),
    tooltip=["genres", "avg_rating"]
).properties(width=700, height=400)

st.altair_chart(chart_rating)
