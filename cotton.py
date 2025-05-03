# cotton_questionnaire.py

import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Cotton Farming Questionnaire", layout="wide")
st.title("Cotton Farming Questionnaire (कपास किसान सर्वे)")

questions = [
    "Farmer Tracenet Code",
    "Farmer Full Name",
    "Mobile no.",
    "Gender",
    "Highest education",
    "Village",
    "Taluka/Block",
    "District",
    "State",
    "Pincode",
    "No. of males (adult) in household",
    "No. of females (adult) in household",
    "Children (<16) in household",
    "Total Member of Household",
    "No. of school-going children",
    "No. of earning members in the family",
    "Total Landholding (in acres)",
    "Primary crop",
    "Secondary crops",
    "nonorganic Cotton land (in acre) (if any)",
    "Organic Cotton land (in acre)",
    "Years since practicing organic cotton (#)",
    "Certification status (certified/IC1..)",
    "source of irrigation",
    "cultivable area (acre)",
    "No. of cattle (cow and Buffalo)",
    "source of drinking water",
    "Preferred selling point (Aggregrator/Suminter/ APMC/ other Gin)",
    "has space for harvested cotton storage (Y/N)",
    "Receives any agro advisory (Y/N)",
    "Received any training on best practices for organic cotton?",
    "Membership in FPO/FPC/SHG",
    "Maintaining any Diary or Register for record keeping (Y/N)",
    "Annual household income(in Rs)",
    "Primary source of income",
    "secondary source of income",
    "income from Primary source (Rs.)",
    "Certification cost per annum/acre",
    "Avg. production of organic cotton/acre (Kg)",
    "Cost of cultivation/acre (Rs)",
    "Quantity sold of organic cotton (in kg)",
    "Selling price per kg (Rs.)",
    "material cost for bio-inputs",
    "Name of bio-input used for pest and disease management",
    "Name of  bio-fertilizer/compost used",
    "dose of bio-fertilizer/compost used/acre",
    "No. of pheromon trap used / acre",
    "cost per pheromone trap",
    "No. of Yellow sticky trap used / acre",
    "cost per yellow sticky trap",
    "No. of blue sticky trap used / acre",
    "cost per blue sticky trap",
    "No. of bird perches used / acre",
    "irrigation cost/acre",
    "No. of irrigation require for organic cotton",
    "irrigation method used",
    "any farm machinery hired (Y/N)",
    "cost of machinery hiring (Rs.)",
    "Local labour cost per day",
    "Migrant labour cost per day",
    "No. of workers require during sowing/acre",
    "No. of workers require during havesting/acre",
    "Harvesting time (1st, 2nd & 3rd picking) (month)",
    "weeding method used (manual/mechanical)",
    "weeding cost/acre",
    "cost of mulching/acre",
    "No. of Tillage practiced",
    "tillage cost/acre",
    "Land preparation cost/acre",
    "cost of organic seed per acre",
    "seed rate of organic cotton/acre",
    "Variety of organic cotton seed (Name)",
    "Name of border crop used",
    "Name of the inter crop used",
    "Name of cover crop",
    "Name of trap crop",
    "Mulching used (Y/N)",
    "Type of mulching used (Bio-plastic/ green/ dry)",
    "What precautions used during storage",
    "hired vehicle used for transportation of seed cotton (Y/N)",
    "Transportation cost (Rs.)/Kg of seed cotton",
    "Any quantity rejection due to contamination/impurities (Kg)",
    "Price discovery mechanism",
    "Payment Transaction type (Cash/online)",
    "Days of credit after sell",
    "Availing any govt. scheme or subsidi benefits (Y/N)",
    "Opted for crop insurance (Y/N)",
    "cost of crop insurance per acre",
    "Possess KCC (Y/N)",
    "Possess active bank account (Y/N)",
    "Any agri loan from Bank (Y/N)",
    "What was the Previous crop in the same land",
    "Crop rotation used (Y/N)",
    "Crops used for rotation",
    "Using any water tracking devices (Y/N)",
    "capacity of pump (in HP)",
    "Maintaining Buffer zone (Y/N)",
    "Utilization of crop residue (Fuel/cattle feed/biochar/ in-situ composting/burning)",
    "Mode of payment to workers (cash/ online)",
    "Any wage difference for Men and Women workers (Y/N)",
    "Using any labour register (Y/N)",
    "any arrangement of safety-kit / first-aid for workers",
    "any provision of shelter & safe drinking water for workers",
    "any provision for lavatory for workers",
    "Involve family members (Women) in agril. operations",
    "any community water harvesting structure (Y/N)",
    "use of soil moisture meter (Y/N)"
]

responses = {}

with st.form("questionnaire_form"):
    for question in questions:
        responses[question] = st.text_input(question)
    submitted = st.form_submit_button("Submit")

if submitted:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"cotton_response_{timestamp}.csv"
    df = pd.DataFrame([responses])
    df.to_csv(filename, index=False)
    st.success("Thank you! Your response has been recorded.")
    with open(filename, "rb") as file:
        st.download_button(
            label="Download your response CSV",
            data=file,
            file_name=filename,
            mime="text/csv"
        )
