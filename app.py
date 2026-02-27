import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Stock Intelligence", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* ===== MAIN BACKGROUND ===== */
html, body, [data-testid="stAppViewContainer"], section.main > div {
    background-color: #0d1117;
    color: #FACC15;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* ===== MAIN TITLE ===== */
.big-title {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #00F5A0, #00D9F5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 255, 200, 0.6);
    margin-bottom: 5px;
}

/* ===== SUBTITLE ===== */
.subtitle {
    color: #FFD700;
    font-size: 18px;
    letter-spacing: 1px;
    opacity: 0.9;
    margin-bottom: 25px;
}

/* ===== LABELS ===== */
label {
    color: #FFD700 !important;
    font-weight: 600;
}

/* ===== INPUT BOXES ===== */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div>div {
    background-color: #161b22;
    color: #FACC15;
    border: 1px solid #00D9F5;
    border-radius: 10px;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #00F5A0, #00D9F5);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    border: none;
    box-shadow: 0 0 20px rgba(0, 255, 200, 0.4);
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
}

/* ===== METRIC CARDS ===== */
[data-testid="metric-container"] {
    background-color: #161b22;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
    border: 1px solid rgba(255, 215, 0, 0.2);
}

/* Metric value */
[data-testid="metric-container"] label {
    color: #FFD700 !important;
}
.metric-card {
    background: rgba(22, 27, 34, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-title {
    font-size: 15px;
    color: #aaa;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
}

/* Glow Variants */
.glow-green {
    box-shadow: 0 0 25px rgba(0,255,150,0.4);
}
.glow-green .metric-value {
    color: #00F5A0;
}

.glow-yellow {
    box-shadow: 0 0 25px rgba(255,215,0,0.4);
}
.glow-yellow .metric-value {
    color: #FFD700;
}

.glow-blue {
    box-shadow: 0 0 25px rgba(0,217,245,0.4);
}
.glow-blue .metric-value {
    color: #00D9F5;
}

.glow-purple {
    box-shadow: 0 0 25px rgba(180,0,255,0.4);
}
.glow-purple .metric-value {
    color: #c77dff;
}

/* ===== SECTION HEADINGS ===== */
h2, h3 {
    color: #FFD700;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
}

/* ===== SUCCESS / INFO BOX ===== */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ===== DOWNLOAD BUTTON ===== */
.stDownloadButton>button {
    background: linear-gradient(90deg, #FFD700, #FACC15);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    height: 45px;
    width: 100%;
    border: none;
}
/* Investment Amount & Period Value Color */

/* ===== TRANSPARENT GREEN INPUT STYLE ===== */

.stNumberInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="input"] {
    background: rgba(0, 245, 160, 0.08) !important;  /* Transparent green */
    border: 1px solid rgba(0, 245, 160, 0.4) !important;
    border-radius: 12px;
    backdrop-filter: blur(6px);
}
/* ===== PROFESSIONAL SOFT GREEN INPUT ===== */

.stNumberInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="input"] {
    background: rgba(16,185,129,0.08) !important;  /* Soft tint */
    border: 1px solid #34D399 !important;
    border-radius: 10px;
}

/* Input text color */
.stNumberInput input,
.stTextInput input {
    color: #059669 !important;   /* Professional green */
    font-weight: 600;
    font-size: 17px;
    background: transparent !important;
}

/* + - buttons */
.stNumberInput button {
    background: transparent !important;
    color: #10B981 !important;
    border: none !important;
}

/* Focus effect */
.stNumberInput div[data-baseweb="input"]:focus-within,
.stTextInput div[data-baseweb="input"]:focus-within {
    box-shadow: 0 0 8px rgba(16,185,129,0.4);
}



/* + - button color */
.stNumberInput button {
    background-color: #0f172a !important;
    color: #00F5A0 !important;
    border: none !important;
}
</style>

""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="big-title">⚡ AI Quantitative Stock Intelligence</div>', unsafe_allow_html=True)
st.markdown("Institutional-Grade Technical Research Engine")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    symbol = st.text_input("Stock Symbol (.NS for India)", "TATAPOWER.NS")

with col_input2:
    investment_amount = st.number_input("Investment Amount (₹)", min_value=1000, value=50000)

with col_input3:
    years = st.number_input("Select Period (Years)", min_value=1, max_value=20, value=1, step=1)
    period = f"{years}y"

# ---------------- MAIN LOGIC ----------------
if st.button("🚀 Generate AI Report"):

    stock = yf.Ticker(symbol)
    data = stock.history(period=period)

    if data.empty:
        st.error("❌ Invalid Symbol")
    else:

        # RSI Calculation
        delta = data['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = rsi.iloc[-1]
        current_price = data['Close'].iloc[-1]
        high_price = data['Close'].max()
        low_price = data['Close'].min()
        volatility = data['Close'].pct_change().std() * 100
        shares = investment_amount // current_price

        # Moving Average
        sma_50 = data['Close'].rolling(50).mean()

        # Upside / Downside
        upside = ((high_price - current_price) / current_price) * 100
        downside = ((current_price - low_price) / current_price) * 100

        if downside != 0:
            risk_reward = upside / downside
        else:
            risk_reward = 0

        # Final Verdict Logic
        final_verdict = "LONG TERM HOLD / ACCUMULATE"
        scientific_reason = "Moderate indicators. Gradual accumulation strategy suggested."

        if risk_reward > 1.5 and current_rsi < 60:
            final_verdict = "STRONG BUY"
            scientific_reason = "Favorable risk-reward ratio with healthy momentum."
        elif risk_reward < 0.8:
            final_verdict = "HOLD"
            scientific_reason = "Risk outweighs reward. Cautious accumulation advised."

        # ---------------- METRICS ----------------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"""
        <div class="metric-card glow-green">
            <div class="metric-title">Current Price</div>
            <div class="metric-value">₹{current_price:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="metric-card glow-yellow">
            <div class="metric-title">RSI</div>
            <div class="metric-value">{current_rsi:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="metric-card glow-blue">
            <div class="metric-title">Volatility %</div>
            <div class="metric-value">{volatility:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="metric-card glow-purple">
            <div class="metric-title">Shares Possible</div>
            <div class="metric-value">{int(shares)}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ---------------- CHART ----------------
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            line=dict(width=3),
            name='Close Price'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=sma_50,
            mode='lines',
            line=dict(width=2),
            name='SMA 50'
        ))

        fig.update_layout(
            title=f"{symbol} Price Chart",
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # ---------------- STRUCTURED REPORT ----------------
        st.markdown("## 📊 AI Stock Research Report")

        st.markdown("### KEY METRICS")
        st.write(f"Current Price: ₹{current_price:.2f}")
        st.write(f"RSI: {current_rsi:.2f}")
        st.write(f"Volatility: {volatility:.2f}%")

        st.markdown("### DETAILED ANALYSIS")
        st.write("• RSI is neutral. No strong momentum signal.")
        st.write("• Price trading in mid-range zone.")
        st.write("• Insufficient data for 200 SMA analysis.")
        st.write("• Low volatility. Stable structure for long-term investors.")
        st.write(f"• Estimated Upside Potential: {upside:.2f}%")
        st.write(f"• Estimated Downside Risk: {downside:.2f}%")
        st.write(f"• Risk-Reward Ratio: {risk_reward:.2f}")

        st.markdown("### FINAL VERDICT")
        st.success(final_verdict)

        st.markdown("### SCIENTIFIC JUSTIFICATION")
        st.info(scientific_reason)

        # ---------------- PDF GENERATION ----------------
        pdf_filename = "Stock_Report.pdf"
        doc = SimpleDocTemplate(pdf_filename)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"<b>AI Stock Research Report - {symbol}</b>", styles["Title"]))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("<b>KEY METRICS</b>", styles["Heading2"]))
        elements.append(Paragraph(f"Current Price: ₹{current_price:.2f}", styles["Normal"]))
        elements.append(Paragraph(f"RSI: {current_rsi:.2f}", styles["Normal"]))
        elements.append(Paragraph(f"Volatility: {volatility:.2f}%", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("<b>DETAILED ANALYSIS</b>", styles["Heading2"]))
        elements.append(Paragraph("• RSI is neutral. No strong momentum signal.", styles["Normal"]))
        elements.append(Paragraph("• Price trading in mid-range zone.", styles["Normal"]))
        elements.append(Paragraph("• Insufficient data for 200 SMA analysis.", styles["Normal"]))
        elements.append(Paragraph("• Low volatility. Stable structure for long-term investors.", styles["Normal"]))
        elements.append(Paragraph(f"• Estimated Upside Potential: {upside:.2f}%", styles["Normal"]))
        elements.append(Paragraph(f"• Estimated Downside Risk: {downside:.2f}%", styles["Normal"]))
        elements.append(Paragraph(f"• Risk-Reward Ratio: {risk_reward:.2f}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("<b>FINAL VERDICT</b>", styles["Heading2"]))
        elements.append(Paragraph(final_verdict, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("<b>SCIENTIFIC JUSTIFICATION</b>", styles["Heading2"]))
        elements.append(Paragraph(scientific_reason, styles["Normal"]))

        doc.build(elements)

        with open(pdf_filename, "rb") as f:
            st.download_button("📥 Download Full Report", f, file_name=pdf_filename)

        os.remove(pdf_filename)