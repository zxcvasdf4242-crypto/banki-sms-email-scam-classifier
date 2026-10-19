import re
SAMPLE_MESSAGES={
"Test C — upfront loan fee":"Guaranteed loan approval! Pay a processing fee now to receive ₹2,00,000 instantly. No documents required.",
"Urgent KYC link":"URGENT! Your bank account will be blocked today. Verify your KYC immediately at http://fake-bank-example.test and claim your reward.",
"Ordinary statement notice":"Your monthly account statement is available. Sign in through your bank's official application to view it.",
"Installment reminder":"Your loan installment is due on the 10th. Review your repayment schedule in the official banking app.",
"Prize / reward message":"Congratulations! You won a cash prize. Pay a small release fee now to claim your reward."}
RULES=[
("Urgency or threat",r"\b(urgent|immediately|blocked today|suspended|expire today|final warning)\b",18),
("Credential or KYC request",r"\b(otp|pin|password|cvv|kyc|credentials)\b",25),
("Upfront payment / fee",r"\b(processing fee|upfront fee|release fee|activation fee|pay a fee|pay first|advance payment)\b",28),
("Guaranteed loan or approval",r"\b(guaranteed loan|guaranteed approval|no documents required|instant guaranteed credit|loan approved instantly)\b",18),
("Prize or reward bait",r"\b(claim your reward|you won|cash prize|lottery|claim prize|free gift)\b",15),
("Pressure to click a link",r"\b(click|tap|open|visit)\b.{0,35}\b(link|url|below|here|verify|update)\b",12),
("Too-good-to-be-true returns",r"\b(no risk|double your money|guaranteed returns|risk.free profit)\b",20)]
def analyze_message(message):
    text="" if message is None else str(message); clean=re.sub(r"\s+"," ",text).strip(); signals=[]; score=0
    for name,pattern,weight in RULES:
        if re.search(pattern,clean,re.I): signals.append(name); score+=weight
    urls=re.findall(r"https?://[^\s<>\"']+",clean,re.I)
    if urls: signals.append("Contains a URL; verify the domain independently"); score+=10
    score=min(score,100); label="Scam-like" if score>=25 else "Likely safe"
    return {"label":label,"risk_score":int(score),"signals":signals,"signal_count":len(signals),"message_length":len(clean),"has_url":bool(urls)}
def analyze_many(messages): return [analyze_message(m) for m in messages]
