import streamlit as st
from generate import answer_question
from verify import verify_answer

st.set_page_config(page_title="Taskly Support Copilot")
st.title("Taskly Support Copilot")
st.caption("Ask a question about Taskly. Answers are grounded in real docs and fact-checked before being shown.")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("ask_form", clear_on_submit=True):
    question = st.text_input("Your question")
    submitted = st.form_submit_button("Ask")

if submitted and question:
    with st.spinner("Searching docs and generating an answer..."):
        result = verify_answer(question)
    st.session_state.history.append({"question": question, "result": result})

for item in reversed(st.session_state.history):
    st.divider()
    st.markdown(f"**Q: {item['question']}**")

    st.write(item["result"]["answer"])

    verdict_line = item["result"]["verification"].splitlines()[0]
    if "UNSUPPORTED" in verdict_line:
        st.error(verdict_line)
    elif "PARTIALLY" in verdict_line:
        st.warning(verdict_line)
    else:
        st.success(verdict_line)

    with st.expander("Full verification details"):
        st.text(item["result"]["verification"])

    st.caption("Sources: " + ", ".join(item["result"]["sources_used"]))
