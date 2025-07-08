import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dashboard styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .appliance-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .appliance-card:hover {
        border-color: #4CAF50;
        transform: translateY(-2px);
    }
    
    .energy-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
    }
    
    .tip-card {
        background: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .stSlider > div > div {
        background-color: #f8f9fa;
    }
    
    .consumption-gauge {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="energy-header">
    <h1>⚡ Smart Energy Dashboard</h1>
    <p>Monitor, Calculate & Optimize Your Home Energy Consumption</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = {
        'daily_consumption': [],
        'dates': [],
        'appliances': {}
    }

# Main dashboard layout
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home Setup", "📊 Energy Analysis", "💡 Smart Tips", "📈 Usage Trends"])

with tab1:
    st.markdown('<div class="section-header">🏠 Configure Your Home</div>', unsafe_allow_html=True)
    
    # User info in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("👤 Your Name", value="ARYAN", help="Enter your name")
        
    with col2:
        age = st.number_input("🎂 Age", min_value=1, max_value=120, value=19, help="Your age")
        
    with col3:
        family_size = st.number_input("👨‍👩‍👧‍👦 Family Size", min_value=1, max_value=10, value=3, help="Number of family members")
    
    # Housing details
    st.markdown('<div class="section-header">🏡 Housing Details</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        living_type = st.selectbox(
            "🏠 Housing Type",
            ["Flat", "Tenement", "Bungalow", "Villa"],
            help="Select your housing type"
        )
    
    with col2:
        bhk = st.selectbox(
            "🛏️ House Size",
            ["1 BHK", "2 BHK", "3 BHK", "4 BHK", "5+ BHK"],
            index=1,
            help="Select your house size"
        )
    
    with col3:
        house_area = st.number_input(
            "📐 House Area (sq ft)",
            min_value=300,
            max_value=5000,
            value=1000,
            step=50,
            help="Total house area in square feet"
        )
    
    # Appliances configuration
    st.markdown('<div class="section-header">🔌 Appliances Configuration</div>', unsafe_allow_html=True)
    
    # Create appliance configuration in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Essential Appliances")
        
        # Lights and fans based on BHK
        bhk_num = int(bhk.split()[0]) if bhk.split()[0].isdigit() else 3
        
        lights_count = st.slider(f"💡 LED Lights", 1, bhk_num * 3, bhk_num * 2, help="Number of LED lights")
        fans_count = st.slider(f"🌀 Ceiling Fans", 1, bhk_num * 2, bhk_num, help="Number of ceiling fans")
        
        # Major appliances
        has_ac = st.checkbox("❄️ Air Conditioner", value=False)
        ac_count = 0
        if has_ac:
            ac_count = st.slider("Number of ACs", 1, 5, 1)
        
        has_fridge = st.checkbox("🧊 Refrigerator", value=True)
        fridge_size = st.selectbox("Fridge Size", ["Small (150L)", "Medium (300L)", "Large (500L+)"], index=1) if has_fridge else "None"
        
        has_washing_machine = st.checkbox("🧺 Washing Machine", value=False)
        wm_type = st.selectbox("Type", ["Semi-Automatic", "Fully-Automatic", "Front-Load"], index=1) if has_washing_machine else "None"
    
    with col2:
        st.subheader("Entertainment & Others")
        
        tv_count = st.slider("📺 Televisions", 0, 5, 1, help="Number of TVs")
        tv_size = st.selectbox("TV Size", ["32 inch", "43 inch", "55 inch", "65 inch+"], index=1) if tv_count > 0 else "None"
        
        has_microwave = st.checkbox("🔥 Microwave Oven", value=False)
        has_water_heater = st.checkbox("🚿 Water Heater", value=False)
        has_dishwasher = st.checkbox("🍽️ Dishwasher", value=False)
        has_induction = st.checkbox("🔥 Induction Cooktop", value=False)
        
        # Usage hours
        st.subheader("⏰ Usage Hours")
        ac_hours = st.slider("AC Usage (hours/day)", 0, 24, 8) if has_ac else 0
        tv_hours = st.slider("TV Usage (hours/day)", 0, 24, 6) if tv_count > 0 else 0
        lighting_hours = st.slider("Lighting (hours/day)", 1, 24, 8)

with tab2:
    st.markdown('<div class="section-header">📊 Energy Analysis & Consumption</div>', unsafe_allow_html=True)
    
    # Energy calculation function
    def calculate_detailed_energy():
        energy_breakdown = {}
        
        # Lights (LED: 9W each)
        light_energy = lights_count * 0.009 * lighting_hours
        energy_breakdown["Lights"] = light_energy
        
        # Fans (75W each)
        fan_energy = fans_count * 0.075 * lighting_hours
        energy_breakdown["Fans"] = fan_energy
        
        # AC (1500W each)
        if has_ac:
            ac_energy = ac_count * 1.5 * ac_hours
            energy_breakdown["Air Conditioner"] = ac_energy
        
        # Refrigerator (based on size)
        if has_fridge:
            fridge_power = {"Small (150L)": 0.1, "Medium (300L)": 0.15, "Large (500L+)": 0.2}
            fridge_energy = fridge_power[fridge_size] * 24
            energy_breakdown["Refrigerator"] = fridge_energy
        
        # TV (based on size)
        if tv_count > 0:
            tv_power = {"32 inch": 0.06, "43 inch": 0.08, "55 inch": 0.12, "65 inch+": 0.15}
            tv_energy = tv_count * tv_power[tv_size] * tv_hours
            energy_breakdown["Television"] = tv_energy
        
        # Washing Machine
        if has_washing_machine:
            wm_power = {"Semi-Automatic": 0.5, "Fully-Automatic": 0.8, "Front-Load": 1.0}
            wm_energy = wm_power[wm_type] * 1.5  # 1.5 hours usage per day
            energy_breakdown["Washing Machine"] = wm_energy
        
        # Other appliances
        if has_microwave:
            energy_breakdown["Microwave"] = 1.2 * 0.5  # 1200W for 30 mins
        if has_water_heater:
            energy_breakdown["Water Heater"] = 2.0 * 2  # 2000W for 2 hours
        if has_dishwasher:
            energy_breakdown["Dishwasher"] = 1.5 * 1  # 1500W for 1 hour
        if has_induction:
            energy_breakdown["Induction Cooktop"] = 1.8 * 2  # 1800W for 2 hours
        
        return energy_breakdown
    
    # Calculate energy
    energy_data = calculate_detailed_energy()
    total_daily_energy = sum(energy_data.values())
    monthly_energy = total_daily_energy * 30
    yearly_energy = total_daily_energy * 365
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{total_daily_energy:.1f} kWh</h3>
            <p>Daily Consumption</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{monthly_energy:.0f} kWh</h3>
            <p>Monthly Consumption</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>₹{total_daily_energy * 5:.0f}</h3>
            <p>Daily Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>₹{monthly_energy * 5:.0f}</h3>
            <p>Monthly Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if energy_data:
            # Pie chart
            fig_pie = px.pie(
                values=list(energy_data.values()),
                names=list(energy_data.keys()),
                title="Energy Consumption Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        if energy_data:
            # Bar chart
            fig_bar = px.bar(
                x=list(energy_data.values()),
                y=list(energy_data.keys()),
                orientation='h',
                title="Energy Consumption by Appliance",
                labels={'x': 'Energy (kWh/day)', 'y': 'Appliances'},
                color=list(energy_data.values()),
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Gauge chart for efficiency
    efficiency_score = max(0, min(100, 100 - (total_daily_energy - 5) * 10))
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = efficiency_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Energy Efficiency Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">💡 Smart Energy Saving Tips</div>', unsafe_allow_html=True)
    
    # Personalized tips based on user's setup
    tips = []
    
    if has_ac:
        tips.append({
            "icon": "❄️",
            "title": "AC Optimization",
            "tip": f"You're using AC for {ac_hours} hours daily. Set temperature to 24°C and use ceiling fans to feel cooler. This can save up to 30% energy.",
            "savings": f"Potential savings: ₹{ac_count * 1.5 * ac_hours * 0.3 * 5 * 30:.0f}/month"
        })
    
    if lights_count > bhk_num * 2:
        tips.append({
            "icon": "💡",
            "title": "Smart Lighting",
            "tip": f"You have {lights_count} lights. Use motion sensors and timers to automatically turn off lights in unused rooms.",
            "savings": f"Potential savings: ₹{lights_count * 0.009 * 2 * 5 * 30:.0f}/month"
        })
    
    if has_fridge:
        tips.append({
            "icon": "🧊",
            "title": "Refrigerator Efficiency",
            "tip": "Keep your fridge temperature between 3-4°C. Clean coils regularly and avoid opening frequently.",
            "savings": "Potential savings: ₹150-300/month"
        })
    
    if tv_count > 0:
        tips.append({
            "icon": "📺",
            "title": "Smart TV Usage",
            "tip": f"You watch TV for {tv_hours} hours daily. Use power saving mode and turn off when not watching.",
            "savings": f"Potential savings: ₹{tv_count * 0.08 * 2 * 5 * 30:.0f}/month"
        })
    
    # Display tips in cards
    for tip in tips:
        st.markdown(f"""
        <div class="tip-card">
            <h4>{tip['icon']} {tip['title']}</h4>
            <p>{tip['tip']}</p>
            <small><strong>{tip['savings']}</strong></small>
        </div>
        """, unsafe_allow_html=True)
    
    # Energy efficiency recommendations
    st.subheader("🌟 Efficiency Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Immediate Actions:**")
        st.write("• Replace old bulbs with LEDs")
        st.write("• Use power strips to eliminate phantom loads")
        st.write("• Set water heater timer for 2 hours daily")
        st.write("• Clean AC filters monthly")
    
    with col2:
        st.success("**Long-term Upgrades:**")
        st.write("• Install smart thermostats")
        st.write("• Consider solar panels")
        st.write("• Upgrade to energy-efficient appliances")
        st.write("• Install home energy monitoring system")

with tab4:
    st.markdown('<div class="section-header">📈 Usage Trends & Projections</div>', unsafe_allow_html=True)
    
    # Generate sample trend data
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    # Simulate consumption variations
    base_consumption = total_daily_energy
    daily_variations = np.random.normal(0, base_consumption * 0.1, 30)
    consumption_data = [max(0, base_consumption + var) for var in daily_variations]
    
    # Create trend chart
    fig_trend = px.line(
        x=dates,
        y=consumption_data,
        title="30-Day Energy Consumption Trend",
        labels={'x': 'Date', 'y': 'Energy (kWh)'}
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Seasonal projections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Seasonal Variations")
        
        seasons = ['Spring', 'Summer', 'Monsoon', 'Winter']
        seasonal_multipliers = [0.9, 1.3, 1.0, 0.8]  # AC usage affects summer consumption
        seasonal_consumption = [total_daily_energy * mult for mult in seasonal_multipliers]
        
        fig_seasonal = px.bar(
            x=seasons,
            y=seasonal_consumption,
            title="Seasonal Energy Consumption",
            color=seasonal_consumption,
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost Projections")
        
        # Monthly cost breakdown
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_costs = [total_daily_energy * 30 * 5 * mult for mult in [0.8, 0.8, 0.9, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.8]]
        
        fig_cost = px.area(
            x=months,
            y=monthly_costs,
            title="Monthly Cost Projection",
            labels={'x': 'Month', 'y': 'Cost (₹)'}
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    # Summary statistics
    st.subheader("📊 Energy Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Daily", f"{np.mean(consumption_data):.1f} kWh")
    
    with col2:
        st.metric("Peak Consumption", f"{max(consumption_data):.1f} kWh")
    
    with col3:
        st.metric("Lowest Usage", f"{min(consumption_data):.1f} kWh")
    
    with col4:
        st.metric("Efficiency Rating", f"{efficiency_score:.0f}%")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Energy Dashboard for {name} • House: {living_type} ({bhk}) • Family: {family_size} members</p>
    <p>💡 Smart energy management leads to sustainable living and cost savings</p>
</div>
""", unsafe_allow_html=True)