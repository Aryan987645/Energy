import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 10px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>⚡ Energy Consumption Calculator</h1>
    <p>Calculate your monthly energy consumption based on your home and appliances</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'cal_energy' not in st.session_state:
    st.session_state.cal_energy = 0

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Personal Information")
    
    name = st.text_input("Enter Name:", placeholder="Your full name")
    age = st.number_input("Enter Age:", min_value=1, max_value=120, value=25)
    city = st.text_input("Enter City:", placeholder="Your city")
    area = st.text_input("Enter Area:", placeholder="Your area/locality")
    
    st.header("🏠 Housing Details")
    
    house = st.selectbox("What do you have?", ["", "Flat", "Tenament"])
    ran = st.selectbox("House Configuration:", ["", "1BHK", "2BHK", "3BHK"])
    
    st.header("🔌 Appliances")
    
    ac_present = st.checkbox("Do you have an AC?")
    fridge_present = st.checkbox("Do you have a Fridge?")
    washing_machine_present = st.checkbox("Do you have a Washing Machine?")
    
    # Calculate button
    if st.button("🔍 Calculate Energy Consumption"):
        if name and city and area and house and ran:
            # Calculate energy consumption
            cal_energy = 0
            
            # Base consumption based on house type
            if ran == "1BHK":
                cal_energy += (2 * 0.4 + 2 * 0.8) * 30
            elif ran == "2BHK":
                cal_energy += (3 * 0.4 + 3 * 0.8) * 30
            elif ran == "3BHK":
                cal_energy += (4 * 0.4 + 4 * 0.8) * 30
            
            # Add appliance consumption
            if ac_present:
                cal_energy += 3 * 30
            if fridge_present:
                cal_energy += 4 * 30
            if washing_machine_present:
                cal_energy += 2 * 30
            
            # Store in session state
            st.session_state.cal_energy = cal_energy
            st.session_state.calculated = True
            st.session_state.user_data = {
                'name': name,
                'age': age,
                'city': city,
                'area': area,
                'house': house,
                'ran': ran,
                'ac_present': ac_present,
                'fridge_present': fridge_present,
                'washing_machine_present': washing_machine_present
            }
            
            st.success("✅ Calculation completed!")
        else:
            st.error("❌ Please fill in all required fields!")

# Main content area
if st.session_state.calculated:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display result
        st.markdown(f"""
        <div class="result-card">
            <h2>🎯 Energy Consumption Result</h2>
            <div class="result-value">{st.session_state.cal_energy:.1f} kWh</div>
            <p>Monthly Energy Consumption for {st.session_state.user_data['name']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown chart
        st.subheader("📊 Energy Consumption Breakdown")
        
        # Calculate breakdown
        base_energy = 0
        if st.session_state.user_data['ran'] == "1BHK":
            base_energy = (2 * 0.4 + 2 * 0.8) * 30
        elif st.session_state.user_data['ran'] == "2BHK":
            base_energy = (3 * 0.4 + 3 * 0.8) * 30
        elif st.session_state.user_data['ran'] == "3BHK":
            base_energy = (4 * 0.4 + 4 * 0.8) * 30
        
        # Create breakdown data
        breakdown_data = {
            'Category': ['Base Lighting & Fans'],
            'Energy (kWh)': [base_energy]
        }
        
        if st.session_state.user_data['ac_present']:
            breakdown_data['Category'].append('Air Conditioner')
            breakdown_data['Energy (kWh)'].append(90)
        
        if st.session_state.user_data['fridge_present']:
            breakdown_data['Category'].append('Refrigerator')
            breakdown_data['Energy (kWh)'].append(120)
        
        if st.session_state.user_data['washing_machine_present']:
            breakdown_data['Category'].append('Washing Machine')
            breakdown_data['Energy (kWh)'].append(60)
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=breakdown_data['Category'],
            values=breakdown_data['Energy (kWh)'],
            hole=0.3,
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#f5576c']
        )])
        
        fig.update_layout(
            title="Energy Consumption by Category",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # User information summary
        st.markdown("""
        <div class="info-box">
            <h3>👤 Personal Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Name:** {st.session_state.user_data['name']}")
        st.write(f"**Age:** {st.session_state.user_data['age']}")
        st.write(f"**Location:** {st.session_state.user_data['city']}, {st.session_state.user_data['area']}")
        
        st.markdown("""
        <div class="info-box">
            <h3>🏠 Housing Info</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Type:** {st.session_state.user_data['house']}")
        st.write(f"**Configuration:** {st.session_state.user_data['ran']}")
        
        st.markdown("""
        <div class="info-box">
            <h3>🔌 Appliances</h3>
        </div>
        """, unsafe_allow_html=True)
        
        appliances = []
        if st.session_state.user_data['ac_present']:
            appliances.append("Air Conditioner")
        if st.session_state.user_data['fridge_present']:
            appliances.append("Refrigerator")
        if st.session_state.user_data['washing_machine_present']:
            appliances.append("Washing Machine")
        
        if appliances:
            for appliance in appliances:
                st.write(f"✅ {appliance}")
        else:
            st.write("❌ No major appliances")
        
        # Energy efficiency tips
        st.markdown("""
        <div class="info-box">
            <h3>💡 Energy Saving Tips</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("• Use LED bulbs to reduce lighting costs")
        st.write("• Set AC temperature to 24°C or higher")
        st.write("• Unplug devices when not in use")
        st.write("• Use natural light during the day")
        st.write("• Regular maintenance of appliances")
        
        # Reset button
        if st.button("🔄 Calculate Again"):
            st.session_state.calculated = False
            st.session_state.cal_energy = 0
            st.rerun()

else:
    # Welcome message when no calculation is done
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>🚀 Welcome to Energy Calculator!</h3>
            <p>Fill in your details in the sidebar to calculate your monthly energy consumption.</p>
            <br>
            <h4>📋 What we calculate:</h4>
            <ul>
                <li><strong>Base Consumption:</strong> Lighting and fans based on house size</li>
                <li><strong>Air Conditioner:</strong> 90 kWh per month</li>
                <li><strong>Refrigerator:</strong> 120 kWh per month</li>
                <li><strong>Washing Machine:</strong> 60 kWh per month</li>
            </ul>
            <br>
            <p><em>Start by entering your information in the sidebar! ⬅️</em></p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚡ Energy Calculator | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)