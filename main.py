import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_and_process_data(file):
    # Load and Clean the Data
    df = pd.read_csv(
        file,
        skiprows=3,
        names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'],
        parse_dates=['Date'],
        index_col='Date'
    )
    df.sort_index(inplace=True)
    return df

def calculate_signals(df, short_window, long_window):
    # Calculate Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_50'] = df['Close'].rolling(window=long_window).mean()
    
    # Define Trading Signals
    df['Signal'] = 0
    df.loc[df['SMA_20'] > df['SMA_50'], 'Signal'] = 1
    df.loc[df['SMA_20'] <= df['SMA_50'], 'Signal'] = -1
    
    # Calculate Returns
    df['Daily_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Daily_Return']
    df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()
    
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("📈 Trading Strategy Dashboard")
    
    # Sidebar controls
    st.sidebar.header("Strategy Parameters")
    short_window = st.sidebar.slider("Short-term SMA Window", 5, 50, 20)
    long_window = st.sidebar.slider("Long-term SMA Window", 20, 200, 50)
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)
        df = calculate_signals(df, short_window, long_window)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["📊 Price Analysis", "💰 Returns Analysis", "📑 Data"])
        
        with tab1:
            # Create main chart with candlesticks and SMAs
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                              vertical_spacing=0.03, 
                              row_heights=[0.7, 0.3])
            
            # Candlestick chart
            fig.add_trace(go.Candlestick(x=df.index,
                                       open=df['Open'],
                                       high=df['High'],
                                       low=df['Low'],
                                       close=df['Close'],
                                       name='OHLC'),
                         row=1, col=1)
            
            # Add SMAs
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'],
                                   name=f'SMA {short_window}',
                                   line=dict(color='rgba(0, 255, 0, 0.7)')),
                         row=1, col=1)
            
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'],
                                   name=f'SMA {long_window}',
                                   line=dict(color='rgba(255, 0, 0, 0.7)')),
                         row=1, col=1)
            
            # Add volume bars
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
                               name='Volume',
                               marker_color='rgba(100, 100, 100, 0.5)'),
                         row=2, col=1)
            
            # Update layout
            fig.update_layout(
                title='Price and Volume Analysis',
                yaxis_title='Price',
                yaxis2_title='Volume',
                xaxis_rangeslider_visible=False,
                height=800
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            # Create returns comparison chart
            fig_returns = go.Figure()
            
            fig_returns.add_trace(go.Scatter(
                x=df.index,
                y=df['Cumulative_Market_Return'],
                name='Buy and Hold Returns',
                line=dict(color='blue')
            ))
            
            fig_returns.add_trace(go.Scatter(
                x=df.index,
                y=df['Cumulative_Strategy_Return'],
                name='Strategy Returns',
                line=dict(color='green')
            ))
            
            fig_returns.update_layout(
                title='Cumulative Returns Comparison',
                yaxis_title='Cumulative Return',
                height=600
            )
            
            st.plotly_chart(fig_returns, use_container_width=True)
            
            # Performance metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Buy and Hold Return",
                    f"{(df['Cumulative_Market_Return'].iloc[-1] - 1) * 100:.2f}%"
                )
            with col2:
                st.metric(
                    "Strategy Return",
                    f"{(df['Cumulative_Strategy_Return'].iloc[-1] - 1) * 100:.2f}%"
                )
                
        with tab3:
            st.dataframe(df)
            
if __name__ == "__main__":
    main()
