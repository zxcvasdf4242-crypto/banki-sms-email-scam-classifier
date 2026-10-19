from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scamshield.engine import analyze_message, analyze_many, SAMPLE_MESSAGES
from scamshield.storage import load_history, save_history, clear_history
from scamshield.ui import render_header, render_sidebar
st.set_page_config(page_title="ScamShield Pro",page_icon="🛡️",layout="wide")
render_header(); page=render_sidebar(); history_path=ROOT/"data"/"history.csv"; history=load_history(history_path)
if page=="Overview":
    st.subheader("Security overview")
    a,b,c,d=st.columns(4); a.metric("Messages analyzed",len(history)); b.metric("Scam-like flags",int((history.label=="Scam-like").sum()) if not history.empty else 0); c.metric("Likely safe",int((history.label=="Likely safe").sum()) if not history.empty else 0); d.metric("Processing","Local / offline")
    st.markdown("### Start an investigation")
    x,y=st.columns(2)
    x.info("**Analyze a message**\n\nPaste a suspicious SMS, email, banking alert, or loan offer.")
    y.info("**Batch CSV analysis**\n\nAnalyze multiple messages and export a results file.")
    st.markdown("### Recent activity")
    if history.empty: st.caption("No analyses saved yet. Open Analyze message to get started.")
    else: st.dataframe(history.tail(10).iloc[::-1],use_container_width=True,hide_index=True)
    st.caption("Educational prototype. Results are heuristic signals, not proof of fraud.")
elif page=="Analyze message":
    st.subheader("Message investigation")
    st.warning("Do not paste real OTPs, passwords, account numbers, or private customer data.")
    sample=st.selectbox("Try a sample",["Choose a sample…",*SAMPLE_MESSAGES.keys()]); text=SAMPLE_MESSAGES.get(sample,"") if sample!="Choose a sample…" else ""
    message=st.text_area("Message text",value=text,height=160,placeholder="Paste SMS or email text here…")
    if st.button("Analyze message",type="primary",use_container_width=True):
        if not message.strip(): st.warning("Enter a message first.")
        else:
            result=analyze_message(message); save_history(history_path,[{"message":message,**result}]); st.session_state["last_result"]=result
    result=st.session_state.get("last_result")
    if result:
        st.divider(); a,b,c=st.columns(3); a.metric("Assessment",result["label"]); b.metric("Risk score",f'{result["risk_score"]}/100'); c.metric("Signals found",len(result["signals"]))
        if result["label"]=="Scam-like": st.error("Potential scam indicators detected. Verify independently through the institution’s official app or number.")
        else: st.success("Few known scam indicators were found. This does not guarantee the message is legitimate.")
        st.markdown("#### Why it was flagged")
        if result["signals"]:
            for signal in result["signals"]: st.write("• "+signal)
        else: st.write("No high-risk rule matched. Unexpected messages should still be independently verified.")
        with st.expander("Technical details"): st.json({k:v for k,v in result.items() if k!="signals"})
elif page=="Batch analysis":
    st.subheader("Batch CSV analysis")
    st.write("Upload a CSV with a column containing message text. Common column names are detected automatically.")
    uploaded=st.file_uploader("Choose a CSV file",type=["csv"])
    if uploaded:
        try:
            df=pd.read_csv(uploaded)
            if df.empty or len(df.columns)==0: st.error("This CSV has no usable rows or columns.")
            else:
                st.dataframe(df.head(8),use_container_width=True,hide_index=True)
                preferred=next((c for c in df.columns if str(c).strip().lower() in {"message","text","sms","email","content","body","message_text"}),df.columns[0])
                col=st.selectbox("Select the message column",list(df.columns),index=list(df.columns).index(preferred))
                if st.button("Analyze CSV",type="primary",use_container_width=True):
                    texts=df[col].fillna("").astype(str).tolist(); results=analyze_many(texts); out=pd.concat([df.reset_index(drop=True),pd.DataFrame(results)],axis=1); st.session_state["batch_out"]=out
                    save_history(history_path,[{"message":t,**r} for t,r in zip(texts,results) if t.strip()])
                out=st.session_state.get("batch_out")
                if out is not None:
                    st.markdown("### Results"); st.dataframe(out,use_container_width=True,hide_index=True)
                    a,b,c=st.columns(3); a.metric("Rows",len(out)); b.metric("Scam-like",int((out.label=="Scam-like").sum())); c.metric("Likely safe",int((out.label=="Likely safe").sum()))
                    st.download_button("Download analyzed CSV",out.to_csv(index=False).encode("utf-8-sig"),file_name="scamshield_results.csv",mime="text/csv",use_container_width=True)
        except Exception as exc: st.error(f"Could not process this CSV: {exc}"); st.info("Save it as a standard UTF-8 CSV and try again.")
elif page=="History & exports":
    st.subheader("Analysis history")
    if history.empty: st.info("No history yet.")
    else:
        choices=st.multiselect("Filter by assessment",["Scam-like","Likely safe"],default=["Scam-like","Likely safe"]); shown=history[history.label.isin(choices)]
        st.dataframe(shown.iloc[::-1],use_container_width=True,hide_index=True)
        st.download_button("Export history CSV",shown.to_csv(index=False).encode("utf-8-sig"),file_name="scamshield_history.csv",mime="text/csv")
    if st.button("Clear local history"):
        clear_history(history_path); st.success("History cleared."); st.rerun()
elif page=="How it works":
    st.subheader("How ScamShield Pro works")
    st.markdown("""**Pipeline**\n1. Normalize message text.\n2. Check for urgency, credential/KYC requests, upfront fees, suspicious links, prize bait, and guaranteed-loan language.\n3. Combine matched signals into an explainable heuristic score.\n4. Show a label and the exact indicators that matched.\n\n**Limitations**\n- This is a transparent rule-based academic prototype, not a trained or bank-grade classifier.\n- The score is not a probability of fraud.\n- Messages can be misclassified; verify through official channels.\n- Do not enter secrets or personal customer data.""")
    st.dataframe(pd.DataFrame([{"sample":k,"message":v} for k,v in SAMPLE_MESSAGES.items()]),use_container_width=True,hide_index=True)
