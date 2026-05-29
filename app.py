import streamlit as st
st.titleimport streamlit as st

st.set_page_config(
    page_title="최립우 정보",
    page_icon="📘"
)

st.title("최립우 나무위키")

st.write("아래 버튼을 누르면 나무위키 페이지로 이동합니다.")

st.link_button(
    "최립우 나무위키 바로가기",
    "https://namu.wiki/w/%EC%B5%9C%EB%A6%BD%EC%9A%B0"
)
st.write(
