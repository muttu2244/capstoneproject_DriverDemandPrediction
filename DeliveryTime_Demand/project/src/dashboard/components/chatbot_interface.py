"""Chatbot interface component."""
import streamlit as st
from ...chatbots.customer_bot import CustomerBot
from ...chatbots.restaurant_bot import RestaurantBot

def display_chatbot_interface(data):
    """Display chatbot interface with both customer and restaurant bots."""
    st.header("💬 Chat Assistant")
    
    # Bot selection
    bot_type = st.radio(
        "Select chat type:",
        ["Customer Support", "Restaurant Analytics"]
    )
    
    # Initialize appropriate bot
    if bot_type == "Customer Support":
        bot = CustomerBot(data)
        placeholder_text = "Ask about your delivery status, estimated time, etc..."
    else:
        bot = RestaurantBot(data)
        placeholder_text = "Ask about peak hours, forecasts, historical analysis, etc..."
    
    # Chat interface
    user_input = st.text_input("Your question:", placeholder=placeholder_text)
    
    if user_input:
        response = bot.handle_query(user_input)
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            st.write(response)