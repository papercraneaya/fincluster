import streamlit as st
import numpy as np
import pandas as pd

# === Get ticker from global session state ===
ticker = st.session_state.get("ticker", "")

if not ticker:
    st.warning("⚠️ Please enter a stock ticker in the sidebar.")
    st.stop()

# === MAIN PAGE ===
try:
    # Mock stock info values
    company_name = "Sample Corporation"
    forward_eps = 5.20  # Example EPS
    forward_pe = 28.5   # Example P/E ratio
    current_price = 147.32  # Example current price

    st.title(f"💰 Price Forecast for {company_name}")

    # === Collect model-based return from Page 2 toggle ===
    model_return = st.session_state.get("expected_return", 0.09)  # Fallback example return
    terminal_growth = 0.03
    model_price = None

    if forward_eps and model_return is not None and model_return > terminal_growth:
        model_price = forward_eps / (model_return - terminal_growth)

    # Analyst forecast
    analyst_price = None
    if forward_pe and forward_eps:
        analyst_price = forward_pe * forward_eps

    # Peer forecast
    peer_min_return = st.session_state.get("peer_min_return", 0.08)
    peer_max_return = st.session_state.get("peer_max_return", 0.12)

    peer_price_min = None
    peer_price_max = None

    if forward_eps and peer_min_return is not None and peer_max_return is not None:
        if peer_max_return > terminal_growth:
            peer_price_min = forward_eps / (peer_max_return - terminal_growth)
        if peer_min_return > terminal_growth:
            peer_price_max = forward_eps / (peer_min_return - terminal_growth)

    # === Forecasted Price Summary ===
    st.subheader("📌 Forecasted Prices")
    
    forecast_data = []
    if model_price:
        forecast_data.append(("🧠 Model-Based", f"{model_price:.2f}"))
    if peer_price_min and peer_price_max:
        peer_range = f"{peer_price_min:.2f} - {peer_price_max:.2f}"
        forecast_data.append(("📊 Peer-Based Range", peer_range))
    if analyst_price:
        forecast_data.append(("📣 Analyst-Based", f"{analyst_price:.2f}"))

    if forecast_data:
        forecast_df = pd.DataFrame(forecast_data, columns=["Estimate Type", "Price"])
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    # === Price Chart ===
    st.markdown("---")
    st.subheader(f"📉 {ticker.upper()} Share Price")

    if current_price:
        st.markdown(f"💵 **Current Price:** ${current_price:.2f}")

    # Timeframe selection
    timeframe = st.radio(
        "Select Time Frame",
        options=["1M", "3M", "6M", "1Y", "2Y", "5Y", "Max"],
        index=3,
        horizontal=True
    )

    # Simulated historical price data (mock line chart)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=60)
    prices = np.linspace(current_price * 0.85, current_price * 1.1, len(dates)) + np.random.normal(0, 1, len(dates))
    hist = pd.DataFrame({"Close": prices}, index=dates)

    if not hist.empty:
        st.line_chart(hist["Close"], use_container_width=True)
    else:
        st.info(f"{timeframe} price data not available.")

except Exception as e:
    st.error(f"⚠️ Error simulating data: {e}")
