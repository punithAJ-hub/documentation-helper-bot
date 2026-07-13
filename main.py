import streamlit as st
from typing import Any, Dict, List

from backend.core import run_llm



def _format_sources(context_docs: List[Any]) -> List[Any]:
  return [
      str((meta.get("source") or "Unknown"))
      for doc in (context_docs or [])
      if(meta :=(getattr(doc, "metadata", None) or {})) is not None
  ]


st.set_page_config(page_title="Langchain Documentation Helper", layout="centered")
st.title("Langchain Documentation Helper")

with st.sidebar:
    st.subheader("Session")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me anything about Langchain docs. I'll retrieve relavant context and sources",
            "sources":[]
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- {s}")


prompt = st.chat_input("Ask a question about Langchain docs")

if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt, "sources":[]})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        try:
            with st.spinner("Retrieving docs and generating answers..."):
                result: Dict[str, Any] = run_llm(prompt)
                ans = str(result.get("answer", "")).strip() or "(No answer returned.)"
                sources = _format_sources(result.get("context",[]))
            st.markdown(ans)

            if sources:
                with st.expander("Sources"):
                    for s in sources:
                        st.markdown(f"- {s}")
            st.session_state.messages.append({"role":"assistant", "content":ans, "sources":sources})

        except Exception as e:
            st.error("Failed to generate a response")