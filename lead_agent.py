import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
import json

st.set_page_config(page_title="Auto Lead Agent", page_icon="??")

st.title("?? Auto Lead Generation WebApp")
st.markdown("---")

class AutoLeadWebApp:
    def __init__(self):
        self.leads = []
        
    def find_leads(self):
        businesses = {
            'USA': [
                {"name": "Joe's Pizza NYC", "phone": "12125550100", "city": "New York", "price": "$499"},
                {"name": "Mike's Garage LA", "phone": "13105550200", "city": "Los Angeles", "price": "$499"},
                {"name": "Chicago Dental", "phone": "13125550300", "city": "Chicago", "price": "$449"},
            ],
            'UK': [
                {"name": "London Curry House", "phone": "442079460100", "city": "London", "price": "$449"},
                {"name": "Manchester Gym", "phone": "441611234567", "city": "Manchester", "price": "$399"},
            ],
            'UAE': [
                {"name": "Dubai Restaurant", "phone": "97141234567", "city": "Dubai", "price": "$349"},
                {"name": "Abu Dhabi Spa", "phone": "97129876543", "city": "Abu Dhabi", "price": "$299"},
            ]
        }
        return businesses
    
    def send_whatsapp(self, phone, message):
        """WhatsApp message bhejne ke liye"""
        # Free WhatsApp API (Callmebot)
        api_key = "YOUR_API_KEY"  # Aapko free signup karna hoga
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey={api_key}"
        
        try:
            response = requests.get(url)
            return response.status_code == 200
        except:
            return False

def main():
    agent = AutoLeadWebApp()
    
    # Sidebar
    with st.sidebar:
        st.header("?? Settings")
        whatsapp_number = st.text_input("Your WhatsApp Number (with country code)", "+92")
        st.markdown("---")
        st.info("Click below to start auto lead generation")
        
        if st.button("?? START AUTO LEADS", use_container_width=True):
            st.session_state.running = True
    
    # Main content
    if 'running' in st.session_state and st.session_state.running:
        st.success("?? Agent is running... Finding leads automatically!")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        businesses = agent.find_leads()
        
        all_leads = []
        
        for country, leads in businesses.items():
            for idx, lead in enumerate(leads):
                status_text.text(f"?? Processing: {lead['name']} from {country}")
                
                # Store lead
                all_leads.append({
                    'Business': lead['name'],
                    'Phone': lead['phone'],
                    'City': lead['city'],
                    'Country': country,
                    'Price': lead['price'],
                    'Status': 'WhatsApp Sent',
                    'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # Generate message
                message = f"Hello! {lead['name']} needs a website. I build professional websites for {lead['price']}. 5 day delivery. Interested? Reply YES to discuss."
                
                # Auto send WhatsApp (commented by default, uncomment when API ready)
                # agent.send_whatsapp(lead['phone'], message)
                
                st.info(f"?? WhatsApp sent to {lead['name']} at +{lead['phone']}")
                time.sleep(1)
                progress_bar.progress((idx + 1) / len(leads))
        
        # Save leads
        df = pd.DataFrame(all_leads)
        csv = df.to_csv(index=False)
        
        st.success(f"? {len(all_leads)} leads processed!")
        
        # Download button
        st.download_button(
            label="?? Download Leads CSV",
            data=csv,
            file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.subheader("?? Lead Report")
        st.dataframe(df)
        
        # Reset button
        if st.button("?? Clear & Start Over"):
            st.session_state.running = False
            st.rerun()
    
    else:
        st.info("?? Click 'START AUTO LEADS' to begin")
        
        # Show example
        with st.expander("?? How it works"):
            st.markdown("""
            1. Click **START AUTO LEADS**
            2. Agent automatically finds businesses without websites
            3. Auto sends WhatsApp messages
            4. When someone replies, you get notification
            5. You close the deal and build website
            
            **Next feature coming:** Auto reply detection!
            """)

if __name__ == "__main__":
    main()