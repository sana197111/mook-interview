import random
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
load_dotenv()

# 페이지 설정
st.set_page_config(page_title='묵묵한 페이지', page_icon=None, layout='centered', initial_sidebar_state='auto')

# 홈페이지 구현
st.title("묵묵한 페이지: 당신의 이야기로 채우다")
st.subheader("당신의 이야기가 감동의 문장이 되다.")
st.markdown("묵묵한 페이지는 당신의 이야기를 중심으로, 당신만의 고유한 문장을 만들어냅니다.<br/>여러분의 소중한 경험과 생각이 담긴 문장을 만들어보세요.", unsafe_allow_html=True)

# 질문 리스트
questions = [
    "작가님의 필명은 무엇인가요?",
    "가장 중요하게 생각하는 삶의 목표 하나는 무엇인가요?",
    "최근 당신이 다른 사람에게 감사함을 느낀 순간은 언제인가요?",
    "가족 중 누군가를 설명한다면, 그 사람을 한 단어로 표현한다면 그 단어는 무엇인가요?",
    "일상에서 당신을 가장 행복하게 만드는 활동은 무엇인가요?",
    "현재 가장 큰 고민은 무엇인가요?",
    "힘든 시기를 극복하는 데 도움이 되는 것은 무엇인가요?",
    "당신이 선택한 전공 또는 진로에 대한 꿈은 무엇인가요?"
]

# 세션 상태 설정
if 'page' not in st.session_state:
    st.session_state.page = 0  # 초기 페이지 상태 설정
    st.session_state.answers = {}  # 답변 저장용 딕셔너리

# 시작 버튼을 누르면 다음 페이지로 이동
if st.session_state.page == 0 and st.button("당신의 이야기 시작하기"):
    st.session_state.page = 1

# 답변 입력 페이지
if 1 <= st.session_state.page <= len(questions):
    # 현재 페이지의 질문에 대한 답변 입력 받기
    answer = st.text_input(questions[st.session_state.page - 1])
    
    # 답변이 입력되면
    if answer:
        # 답변 저장하고 다음 페이지로 이동
        st.session_state.answers[questions[st.session_state.page - 1]] = answer
        st.session_state.page += 1
        
        # 답변이 입력된 후 바로 다음 질문 렌더링
        if st.session_state.page <= len(questions):  # 여기서 체크를 추가합니다.
            st.text_input(questions[st.session_state.page - 1])

chat_model = ChatOpenAI()

# 모든 질문에 답변하면 문장 생성 페이지로 이동
if st.session_state.page == len(questions) + 1:
    # 문장 생성 버튼을 누르면
    if st.button("문장 생성하기"):
        # 2개의 랜덤 인덱스 선택
        random_indexes = random.sample(range(len(questions)), 2)
        
        # 랜덤으로 선택된 2개의 항목으로 프롬프트 작성
        selected_items = [
            (questions[idx], st.session_state.answers[questions[idx]])
            for idx in random_indexes
        ]

        # 키워드 추출 및 프롬프트 생성
        keywords = ["이름", "삶의 목표", "감사한 순간", "가족", "행복", "현재 고민", "어려움 극복", "진로/꿈"]
        selected_keywords = [keywords[idx] for idx in random_indexes]
        
        # 프롬프트 생성
        prompt_items_text = "\n".join([f"{keyword}: {item[1]}" for keyword, item in zip(selected_keywords, selected_items)])
        prompt = f"""
        {prompt_items_text}
        이 요소를 비유적으로 표현하면서 감동적이고 일관된 에세이를 생성해줘.
        제목, (한줄 띄고) 작가명, (한줄 띄고) 에세이 내용으로 출력해줘.
        """
        # 로딩 애니메이션 또는 메시지 표시 시작
        with st.spinner('에세이를 생성하는 중입니다...'):
            result = chat_model.predict(prompt)
        
        # 로딩 애니메이션/메시지 종료 및 결과 표시
        st.write(result)
    else:
        st.write("답변을 기반으로 문장을 생성하려면 위의 '문장 생성하기' 버튼을 눌러주세요.")