import streamlit as st
PAGES=["Overview","Analyze message","Batch analysis","History & exports","How it works"]
def render_header():
    st.markdown("""<style>.block-container{padding-top:1.5rem;max-width:1400px}.ss-hero{padding:1.35rem 1.5rem;border-radius:18px;background:linear-gradient(120deg,#10243a,#17606a);color:#f5fbff;margin-bottom:1.2rem}.ss-hero h1{margin:0;font-size:2.2rem}.ss-hero p{margin:.4rem 0 0;opacity:.9}div[data-testid=stMetric]{border:1px solid rgba(128,128,128,.25);padding:.8rem;border-radius:12px}</style><div class="ss-hero"><h1>🛡️ ScamShield Pro</h1><p>Banking SMS & email scam triage · Explainable local analysis · Student project</p></div>""",unsafe_allow_html=True)
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🛡️ ScamShield Pro"); st.caption("Offline-first demonstration")
        page=st.radio("Navigation",PAGES,index=0); st.divider(); st.caption("Educational prototype — not a production fraud service.")
    return page
