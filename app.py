import streamlit as st
import json
import pandas as pd
import re
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="WE Plan Calculator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WE_PURPLE = "#5C2D91"
WE_PURPLE_2 = "#6F35B5"
WE_PURPLE_LIGHT = "#8B5FD3"
WE_BG = "#F7F5FB"
WE_GREEN = "#16A36A"
WE_ORANGE = "#F59E0B"

# ============================================================
# LOAD PLANS
# ============================================================

PLANS_PATH = Path(__file__).parent / "plans.json"


def load_plans():
    if not PLANS_PATH.exists():
        return []

    with open(PLANS_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict):
        plans = raw.get("plans", [])
    elif isinstance(raw, list):
        plans = raw
    else:
        plans = []

    for p in plans:
        p.setdefault("name_en", "WE Plan")
        p.setdefault("price", 0)
        p.setdefault("data_gb", 0)
        p.setdefault("minutes", 0)
        p.setdefault("sms", 0)
        p.setdefault("best_for_en", "")

    return sorted(plans, key=lambda x: x.get("price", 0))


plans = load_plans()

# ============================================================
# HELPERS
# ============================================================

def find_best_plan(gb, mins, sms=0):
    fits = [
        p for p in plans
        if p.get("data_gb", 0) >= gb
        and p.get("minutes", 0) >= mins
        and p.get("sms", 0) >= sms
    ]

    if not fits:
        return None

    return min(fits, key=lambda x: x.get("price", 0))


def calculate_match(plan, gb, mins, sms=0):
    if not plan:
        return 0

    data_score = min(gb / max(plan.get("data_gb", 1), 1), 1)
    min_score = min(mins / max(plan.get("minutes", 1), 1), 1)

    if sms > 0:
        sms_score = min(sms / max(plan.get("sms", 1), 1), 1)
    else:
        sms_score = 1

    score = (
        data_score * 0.45
        + min_score * 0.40
        + sms_score * 0.15
    ) * 100

    if (
        plan.get("data_gb", 0) >= gb
        and plan.get("minutes", 0) >= mins
        and plan.get("sms", 0) >= sms
    ):
        score += 10

    return min(round(score), 100)

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(circle at top right,
        rgba(139,95,211,0.16),
        rgba(255,255,255,0) 30%),
        {WE_BG};
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    background: transparent !important;
}}

.we-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,0.92);
    padding: 18px 24px;
    border-radius: 22px;
    border: 1px solid rgba(92,45,145,0.10);
    box-shadow: 0 10px 35px rgba(75,38,110,0.08);
    margin-bottom: 24px;
}}

.brand-wrap {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.we-logo {{
    width: 50px;
    height: 50px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    font-weight: 800;
    background: linear-gradient(145deg,{WE_PURPLE},{WE_PURPLE_LIGHT});
}}

.we-title {{
    font-size: 29px;
    color: {WE_PURPLE};
    font-weight: 800;
}}

.we-subtitle {{
    color: #777087;
    font-size: 13px;
}}

.we-card {{
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(92,45,145,0.08);
    box-shadow: 0 10px 30px rgba(80,50,110,0.06);
    margin-bottom: 18px;
}}

.card-title {{
    color: #171323;
    font-weight: 800;
    font-size: 22px;
}}

.card-subtitle {{
    color: #817A8D;
    font-size: 14px;
    margin-top: 3px;
}}

.best-card {{
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #FBF7FF 55%,
        #EFE3FF 100%
    );
    border-radius: 24px;
    padding: 28px;
    border: 1px solid rgba(92,45,145,0.15);
    box-shadow: 0 20px 45px rgba(92,45,145,0.10);
    min-height: 350px;
}}

.best-badge {{
    display: inline-block;
    background: {WE_PURPLE};
    color: white;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 18px;
}}

.plan-name {{
    color: {WE_PURPLE};
    font-size: 30px;
    font-weight: 850;
}}

.plan-caption {{
    color: #837B8D;
    font-size: 14px;
}}

.price-label {{
    margin-top: 20px;
    font-size: 12px;
    color: #777;
}}

.plan-price {{
    color: {WE_PURPLE};
    font-size: 46px;
    font-weight: 800;
}}

.plan-price span {{
    font-size: 18px;
    color: #71677C;
    font-weight: 500;
}}

.features {{
    display: flex;
    gap: 10px;
    margin-top: 22px;
}}

.feature {{
    flex: 1;
    background: white;
    border: 1px solid #EEE8F3;
    border-radius: 15px;
    padding: 13px 8px;
    text-align: center;
}}

.feature-value {{
    color: #20192B;
    font-weight: 750;
    font-size: 15px;
}}

.feature-label {{
    color: #9A91A4;
    font-size: 11px;
}}

.why-box {{
    background: rgba(92,45,145,0.06);
    border-radius: 15px;
    padding: 15px;
    color: #5D5268;
    font-size: 13px;
    margin-top: 18px;
}}

.why-title {{
    font-weight: 750;
    color: {WE_PURPLE};
    margin-bottom: 5px;
}}

.usage-box {{
    background: white;
    border-radius: 18px;
    border: 1px solid #EFE9F4;
    padding: 17px;
    text-align: center;
}}

.usage-number {{
    font-size: 24px;
    font-weight: 800;
    color: {WE_PURPLE};
}}

.usage-number.green {{
    color: {WE_GREEN};
}}

.usage-number.orange {{
    color: {WE_ORANGE};
}}

.usage-label {{
    color: #968D9F;
    font-size: 12px;
}}

.stButton > button {{
    border-radius: 13px;
    background: linear-gradient(100deg,{WE_PURPLE},{WE_PURPLE_2});
    color: white;
    border: none;
    font-weight: 700;
    min-height: 44px;
}}

.stButton > button:hover {{
    background: linear-gradient(100deg,{WE_PURPLE_2},{WE_PURPLE_LIGHT});
    color: white;
}}

.stTabs [data-baseweb="tab-list"] {{
    display: flex !important;
    gap: 14px !important;
    flex-wrap: nowrap !important;
    overflow: visible !important;
    margin-bottom: 20px;
}}

.stTabs [data-baseweb="tab"] {{
    min-width: 190px !important;
    height: 50px !important;
    background: #EEE8F5 !important;
    border-radius: 14px !important;
    border: 1px solid #D6C4EA !important;
    justify-content: center !important;
}}

.stTabs [data-baseweb="tab"] p {{
    color: #5C2D91 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    opacity: 1 !important;
}}

.stTabs [aria-selected="true"] {{
    background: #5C2D91 !important;
}}

.stTabs [aria-selected="true"] p {{
    color: white !important;
}}

[data-testid="stChatMessage"] {{
    background: white;
    border-radius: 16px;
    border: 1px solid #EFE9F3;
    padding: 8px;
    margin-bottom: 10px;
}}

/* =========================================
   WE BRAND TEXT FIX
========================================= */

/* Default text */
.stApp,
.stApp p,
.stApp span,
.stApp div,
.stApp label,
.stApp li {{
    color: #222222 !important;
    opacity: 1 !important;
}}

/* Main headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {{
    color: #5C2D91 !important;
    opacity: 1 !important;
}}

/* Custom headings */
.we-title,
.card-title,
.plan-name,
.why-title {{
    color: #5C2D91 !important;
}}

/* Secondary text */
.we-subtitle,
.card-subtitle,
.plan-caption,
.usage-label,
.feature-label {{
    color: #5A5363 !important;
    opacity: 1 !important;
}}

/* Orange highlights */
.price-label {{
    color: #F59E0B !important;
}}

.usage-number.orange {{
    color: #F59E0B !important;
}}

/* Inputs */
input,
textarea,
[data-testid="stNumberInput"] input,
[data-testid="stChatInput"] textarea {{
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}}

/* Placeholder */
input::placeholder,
textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {{
    color: #6A6173 !important;
    -webkit-text-fill-color: #6A6173 !important;
    opacity: 1 !important;
}}

/* Tabs not selected */
.stTabs [data-baseweb="tab"] p {{
    color: #5C2D91 !important;
    -webkit-text-fill-color: #5C2D91 !important;
    font-weight: 800 !important;
}}

/* Selected tab */
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] * {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

/* Purple buttons */
.stButton > button {{
    background: #5C2D91 !important;
}}

.stButton > button,
.stButton > button p,
.stButton > button span {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}}

/* Best match badge */
.best-badge {{
    background: #5C2D91 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

/* Logo text */
.we-logo {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

/* Chat messages */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] *,
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] * {{
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    opacity: 1 !important;
}}

/* Metrics */
[data-testid="stMetricLabel"] p {{
    color: #5C2D91 !important;
    font-weight: 800 !important;
}}

[data-testid="stMetricValue"] {{
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    font-weight: 900 !important;
}}

/* Alerts */
[data-testid="stAlert"],
[data-testid="stAlert"] *,
[data-testid="stAlert"] p {{
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    opacity: 1 !important;
}}

/* =========================
   INPUT TEXT WHITE
========================= */

/* Number inputs */
[data-testid="stNumberInput"] input {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}}

/* Chat input */
[data-testid="stChatInput"] textarea {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* Chat placeholder */
[data-testid="stChatInput"] textarea::placeholder {{
    color: #D9D9D9 !important;
    -webkit-text-fill-color: #D9D9D9 !important;
    opacity: 1 !important;
}}

/* Any regular text input */
input {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}t

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

header_html = """
<div class="we-header">
<div class="brand-wrap">
<div class="we-logo">WE</div>
<div>
<div class="we-title">WE Plan Calculator</div>
<div class="we-subtitle">Smart plan recommendation & cost optimization</div>
</div>
</div>
<div style="color:#756D80;font-size:13px;font-weight:600;">
Powered by Smart Recommendation Engine
</div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Plan Calculator",
    "📄 Bill Analysis",
    "🤖 Smart Assistant"
])

# ============================================================
# TAB 1
# ============================================================

with tab1:

    left, right = st.columns([1.55, 1], gap="large")

    with left:

        st.markdown(
            """
<div class="we-card">
<div class="card-title">Tell us your usage</div>
<div class="card-subtitle">
Adjust your typical monthly usage and we'll recommend the best value plan.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        gb = st.slider("🌐 Internet usage (GB)", 0, 200, 45, 1)
        mins = st.slider("📞 Call minutes", 0, 6000, 600, 50)
        sms = st.slider("💬 SMS messages", 0, 2000, 100, 25)

        a, b, c = st.columns(3)

        with a:
            st.markdown(
                f"""
<div class="usage-box">
<div class="usage-number">{gb} GB</div>
<div class="usage-label">Internet</div>
</div>
""",
                unsafe_allow_html=True
            )

        with b:
            st.markdown(
                f"""
<div class="usage-box">
<div class="usage-number green">{mins}</div>
<div class="usage-label">Minutes</div>
</div>
""",
                unsafe_allow_html=True
            )

        with c:
            st.markdown(
                f"""
<div class="usage-box">
<div class="usage-number orange">{sms}</div>
<div class="usage-label">SMS</div>
</div>
""",
                unsafe_allow_html=True
            )

    with right:

        best = find_best_plan(gb, mins, sms)

        if best:

            best_for = (
                best.get("best_for_en")
                or "A balanced plan that covers your expected monthly usage."
            )

            st.markdown(
                f"""
<div class="best-card">

<div class="best-badge">✦ BEST MATCH</div>

<div class="plan-name">
{best.get("name_en", "WE Plan")}
</div>

<div class="plan-caption">
Our top recommendation for your usage
</div>

<div class="price-label">
MONTHLY PRICE
</div>

<div class="plan-price">
{best.get("price", 0)}
<span>EGP</span>
</div>

<div class="features">

<div class="feature">
<div class="feature-value">🌐 {best.get("data_gb", 0)} GB</div>
<div class="feature-label">Internet</div>
</div>

<div class="feature">
<div class="feature-value">📞 {best.get("minutes", 0)}</div>
<div class="feature-label">Minutes</div>
</div>

<div class="feature">
<div class="feature-value">💬 {best.get("sms", 0)}</div>
<div class="feature-label">SMS</div>
</div>

</div>

<div class="why-box">
<div class="why-title">Why this plan?</div>
{best_for}
</div>

</div>
""",
                unsafe_allow_html=True
            )

        else:
            st.warning(
                "Your usage is higher than the available plans."
            )

    st.markdown("### All Plans")

    if plans:

        rows = []

        for p in plans:
            rows.append(
                {
                    "Plan": p.get("name_en"),
                    "Internet": f"{p.get('data_gb', 0)} GB",
                    "Calls": f"{p.get('minutes', 0)} Min",
                    "SMS": p.get("sms", 0),
                    "Price": f"{p.get('price', 0)} EGP",
                    "Match": f"{calculate_match(p, gb, mins, sms)}%"
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.error("No plans found. Please check plans.json")
# ============================================================
# TAB 2 — BILL ANALYSIS
# ============================================================

with tab2:

    st.markdown(
        """
<div class="we-card">
<div class="card-title">Bill Cost Optimizer</div>
<div class="card-subtitle">
Enter your actual monthly usage and current bill.
The engine will find the cheapest plan that fully covers your needs.
</div>
</div>
""",
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        price = st.number_input(
            "Current Bill (EGP)",
            min_value=0,
            value=180,
            step=10,
            key="bill_price"
        )

    with c2:
        used_gb = st.number_input(
            "Data Used (GB)",
            min_value=0.0,
            value=13.0,
            step=0.5,
            key="bill_gb"
        )

    with c3:
        used_mins = st.number_input(
            "Minutes Used",
            min_value=0,
            value=900,
            step=50,
            key="bill_mins"
        )

    with c4:
        used_sms = st.number_input(
            "SMS Used",
            min_value=0,
            value=30,
            step=10,
            key="bill_sms"
        )

    if st.button(
        "⚡ Analyze My Bill",
        use_container_width=True,
        key="analyze_bill_btn"
    ):

        if not plans:
            st.error("No plans loaded. Please check plans.json.")

        else:

            # Find every plan that fully covers actual usage
            fits = [
                p for p in plans
                if p.get("data_gb", 0) >= used_gb
                and p.get("minutes", 0) >= used_mins
                and p.get("sms", 0) >= used_sms
            ]

            if not fits:

                st.warning(
                    "⚠️ None of the available plans fully covers your current usage."
                )

                # Show largest available plan as reference
                largest = max(
                    plans,
                    key=lambda p: (
                        p.get("data_gb", 0)
                        + p.get("minutes", 0) / 100
                        + p.get("sms", 0) / 100
                    )
                )

                st.info(
                    f"Largest available option: "
                    f"**{largest['name_en']}** — "
                    f"{largest['price']} EGP | "
                    f"{largest['data_gb']} GB | "
                    f"{largest['minutes']} Min | "
                    f"{largest.get('sms', 0)} SMS"
                )

            else:

                # Choose the best-value plan based on current bill
                # Not always the cheapest one

                eligible = [
                    p for p in fits
                    if p.get("price", 0) <= price
                ]

                if eligible:
                    best_bill = max(
                        eligible,
                        key=lambda p: (
                                p.get("data_gb", 0) * 2
                                + p.get("minutes", 0) / 50
                                + p.get("sms", 0) / 100
                        )
                    )
                else:
                    best_bill = min(
                        fits,
                        key=lambda p: p.get("price", 0)
                    )

                difference = price - best_bill["price"]

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "Recommended Plan",
                        best_bill["name_en"]
                    )

                with m2:
                    st.metric(
                        "Recommended Cost",
                        f"{best_bill['price']} EGP"
                    )

                with m3:

                    if difference > 0:
                        st.metric(
                            "Monthly Saving",
                            f"{difference} EGP"
                        )

                    elif difference < 0:
                        st.metric(
                            "Extra Monthly Cost",
                            f"{abs(difference)} EGP"
                        )

                    else:
                        st.metric(
                            "Cost Difference",
                            "0 EGP"
                        )

                st.markdown("### 📊 Usage Coverage")

                x1, x2, x3 = st.columns(3)

                with x1:
                    st.write(
                        f"🌐 **Data:** {used_gb:g} GB used → "
                        f"{best_bill['data_gb']} GB included"
                    )

                with x2:
                    st.write(
                        f"📞 **Calls:** {used_mins} min used → "
                        f"{best_bill['minutes']} min included"
                    )

                with x3:
                    st.write(
                        f"💬 **SMS:** {used_sms} used → "
                        f"{best_bill.get('sms', 0)} included"
                    )

                if difference > 0:

                    st.success(
                        f"🎉 Switch to **{best_bill['name_en']}** and save "
                        f"**{difference} EGP per month** "
                        f"(**{difference * 12} EGP per year**)."
                    )

                elif difference == 0:

                    st.info(
                        f"✅ **{best_bill['name_en']}** covers your usage "
                        f"at exactly the same monthly cost."
                    )

                else:

                    extra = abs(difference)

                    st.warning(
                        f"⚠️ The cheapest plan that fully covers your usage is "
                        f"**{best_bill['name_en']}** at "
                        f"**{best_bill['price']} EGP/month**.\n\n"
                        f"That is **{extra} EGP more** than your current bill. "
                        f"Based on the available plans, there is currently "
                        f"**no cheaper plan that fully covers this usage**."
                    )

                # Optional: show next alternatives
                st.markdown("### Other Suitable Plans")

                alternatives = sorted(
                    fits,
                    key=lambda p: p.get("price", 0)
                )[:5]

                alt_rows = []

                for p in alternatives:
                    alt_rows.append({
                        "Plan": p["name_en"],
                        "Price": f"{p['price']} EGP",
                        "Data": f"{p['data_gb']} GB",
                        "Minutes": p["minutes"],
                        "SMS": p.get("sms", 0)
                    })

                st.dataframe(
                    pd.DataFrame(alt_rows),
                    use_container_width=True,
                    hide_index=True
                )
# ============================================================
# TAB 3
# ============================================================

with tab3:

    st.markdown(
        """
<div class="we-card">
<div class="card-title">🤖 WE Smart Assistant</div>
<div class="card-subtitle">
Ask about plans, usage, prices, comparisons or budget.
</div>
</div>
""",
        unsafe_allow_html=True
    )

    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [
            {
                "role": "assistant",
                "content":
                    "Hi 👋 I'm **WE Smart Assistant**.\n\n"
                    "Ask me about plans, prices, usage or your budget."
            }
        ]

    for msg in st.session_state.chat_msgs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Example: I need 30 GB and 600 minutes"
    )

    if prompt:

        st.session_state.chat_msgs.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        text = prompt.lower()

        if not plans:

            ans = "No plans are loaded. Please check plans.json."

        elif "cheapest" in text or "lowest price" in text:

            cheapest = min(
                plans,
                key=lambda p: p.get("price", 0)
            )

            ans = (
                f"💰 The cheapest plan is **{cheapest['name_en']}** "
                f"for **{cheapest['price']} EGP/month**.\n\n"
                f"🌐 {cheapest['data_gb']} GB\n\n"
                f"📞 {cheapest['minutes']} minutes\n\n"
                f"💬 {cheapest.get('sms', 0)} SMS"
            )

        elif "compare" in text:

            first_three = sorted(
                plans,
                key=lambda p: p.get("price", 0)
            )[:3]

            ans = "### 📊 Plan Comparison\n\n"

            for p in first_three:
                ans += (
                    f"**{p['name_en']} — {p['price']} EGP**\n\n"
                    f"🌐 {p['data_gb']} GB | "
                    f"📞 {p['minutes']} Min | "
                    f"💬 {p.get('sms', 0)} SMS\n\n"
                    "---\n\n"
                )

        elif "budget" in text or "under" in text:

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                text
            )

            if numbers:

                budget = float(numbers[0])

                affordable = [
                    p for p in plans
                    if p.get("price", 0) <= budget
                ]

                if affordable:

                    best_budget = max(
                        affordable,
                        key=lambda p: (
                            p.get("data_gb", 0)
                            + p.get("minutes", 0) / 100
                        )
                    )

                    ans = (
                        f"🎯 Best plan within **{budget:.0f} EGP** is "
                        f"**{best_budget['name_en']}**.\n\n"
                        f"💵 {best_budget['price']} EGP/month\n\n"
                        f"🌐 {best_budget['data_gb']} GB\n\n"
                        f"📞 {best_budget['minutes']} minutes\n\n"
                        f"💬 {best_budget.get('sms', 0)} SMS"
                    )

                else:
                    ans = (
                        f"No plan found within "
                        f"**{budget:.0f} EGP**."
                    )

            else:
                ans = (
                    "Tell me your budget. Example: "
                    "**My budget is 200 EGP**."
                )

        elif "gb" in text or "minute" in text or "minutes" in text:

            gb_match = re.search(
                r"(\d+(?:\.\d+)?)\s*gb",
                text
            )

            min_match = re.search(
                r"(\d+)\s*(?:min|mins|minute|minutes)",
                text
            )

            requested_gb = (
                float(gb_match.group(1))
                if gb_match else 0
            )

            requested_mins = (
                int(min_match.group(1))
                if min_match else 0
            )

            fits = [
                p for p in plans
                if p.get("data_gb", 0) >= requested_gb
                and p.get("minutes", 0) >= requested_mins
            ]

            if fits:

                recommended = min(
                    fits,
                    key=lambda p: p.get("price", 0)
                )

                ans = (
                    f"✨ I recommend **{recommended['name_en']}**.\n\n"
                    f"💵 **{recommended['price']} EGP/month**\n\n"
                    f"🌐 {recommended['data_gb']} GB\n\n"
                    f"📞 {recommended['minutes']} minutes\n\n"
                    f"💬 {recommended.get('sms', 0)} SMS\n\n"
                    "✅ This is the cheapest plan that covers your usage."
                )

            else:
                ans = (
                    "I couldn't find a plan that fully covers this usage."
                )

        elif "best" in text or "recommend" in text:

            ans = (
                "Tell me your expected monthly usage.\n\n"
                "Example:\n\n"
                "**I need 40 GB and 800 minutes**\n\n"
                "or\n\n"
                "**My budget is 250 EGP**"
            )

        elif any(
            word in text
            for word in ["hello", "hi", "hey"]
        ):

            ans = (
                "Hi 👋 I can help you:\n\n"
                "- Find the cheapest plan\n"
                "- Recommend the best plan\n"
                "- Compare plans\n"
                "- Work within a budget\n"
                "- Match a plan to your usage"
            )

        else:

            ans = (
                "I can help with WE plans. Try asking:\n\n"
                "**What is the cheapest plan?**\n\n"
                "**My budget is 200 EGP**\n\n"
                "**I need 30 GB and 600 minutes**\n\n"
                "**Compare plans**"
            )

        st.session_state.chat_msgs.append(
            {
                "role": "assistant",
                "content": ans
            }
        )

        with st.chat_message("assistant"):
            st.markdown(ans)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<br><br>
<div style="
text-align:center;
color:#9A92A2;
font-size:12px;
">
WE Plan Calculator • Smart Recommendation Engine<br>
Plans and prices are based on the available local dataset.
</div>
""",
    unsafe_allow_html=True
)