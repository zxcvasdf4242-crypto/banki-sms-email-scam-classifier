from pathlib import Path
from datetime import datetime,timezone
import pandas as pd
COLUMNS=["timestamp_utc","message_preview","label","risk_score","signal_count","signals"]
def load_history(path):
    p=Path(path)
    if not p.exists(): return pd.DataFrame(columns=COLUMNS)
    try:
        df=pd.read_csv(p)
        for col in COLUMNS:
            if col not in df.columns: df[col]=""
        return df[COLUMNS]
    except (OSError,ValueError,pd.errors.ParserError): return pd.DataFrame(columns=COLUMNS)
def save_history(path,records):
    if not records:return
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); old=load_history(p); rows=[]
    for r in records:
        rows.append({"timestamp_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),"message_preview":str(r.get("message",""))[:180],"label":r.get("label",""),"risk_score":r.get("risk_score",0),"signal_count":r.get("signal_count",len(r.get("signals",[]))),"signals":"; ".join(r.get("signals",[]))})
    pd.concat([old,pd.DataFrame(rows)],ignore_index=True).to_csv(p,index=False,encoding="utf-8-sig")
def clear_history(path):
    p=Path(path)
    if p.exists():p.unlink()
