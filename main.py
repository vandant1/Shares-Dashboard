import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Set up the GUI
st.set_page_config(page_title="Stock Dashboard", layout="wide", page_icon="📈")
hide_menu_style = "<style> footer {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title("📈 Stock Dashboard")

# Create a sidebar for user input
symbol = st.sidebar.text_input("Enter a stock symbol (e.g. AAPL, GOOGL, MSFT):")
start_date = st.sidebar.date_input("Enter a start date:")
end_date = st.sidebar.date_input("Enter an end date:")

# Fetch stock data
if symbol and start_date and end_date:
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    if not stock_data.empty:
        # Calculate price differences
        latest_price = stock_data.iloc[-1]["Close"].item()
        previous_year_price = (
            stock_data.iloc[-252]["Close"].item()
            if len(stock_data) > 252
            else stock_data.iloc[0]["Close"].item()
        )
        price_difference = latest_price - previous_year_price
        percentage_difference = (price_difference / previous_year_price) * 100

        # Create a candlestick chart
        candlestick_chart = go.Figure(
            data=[
                go.Candlestick(
                    x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close']
                )
            ]
        )
        candlestick_chart.update_layout(
            title=f"{symbol} Candlestick Chart", 
            xaxis_rangeslider_visible=False
        )

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Close Price", f"${latest_price:.2f}")
        with col2:
            st.metric(
                "Price Difference (YoY)", 
                f"${price_difference:.2f}", 
                f"{percentage_difference:+.2f}%"
            )
        with col3:
            st.metric("52-Week High", f"${stock_data['High'].tail(252).max():.2f}")
        with col4:
            st.metric("52-Week Low", f"${stock_data['Low'].tail(252).min():.2f}")

        # Display the candlestick chart
        st.plotly_chart(candlestick_chart, use_container_width=True)

        # Provide a download button for the stock data
        st.download_button(
            "Download Stock Data Overview", 
            stock_data.to_csv(index=True), 
            file_name=f"{symbol}_stock_data.csv", 
            mime="text/csv"
        )
    else:
        st.error("No data found for the given symbol and date range.")
else:
    st.info("Please enter a stock symbol and date range to fetch data.")