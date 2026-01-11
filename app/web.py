import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Book Demand Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border-color: #FF4B4B;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196F3;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📚 Book Demand Prediction System")
st.markdown("### Predict monthly sales based on book characteristics")
st.markdown("---")

# Info box
st.markdown("""
<div class="info-box">
    <strong>ℹ️ How it works:</strong> Enter your book details below to get a prediction of monthly sales demand. 
    Our model analyzes category, pricing, ratings, and other factors to provide accurate forecasts.
</div>
""", unsafe_allow_html=True)

# Sidebar for additional information
with st.sidebar:
    st.header("📊 About This Tool")
    st.markdown("""
    This tool uses machine learning to predict book demand based on:
    - **Category**: Genre of the book
    - **Pricing**: Current vs original price
    - **Ratings**: Average customer rating
    - **Reviews**: Number of customer reviews
    - **Pages**: Book length
    """)
    
    st.markdown("---")
    st.subheader("💡 Tips for Best Results")
    st.markdown("""
    - Higher ratings typically indicate higher demand
    - Competitive pricing improves sales
    - More reviews build customer trust
    - Different categories have different demand patterns
    """)
    
    st.markdown("---")
    st.subheader("🎯 Demand Levels")
    st.markdown("""
    - **🔴 Low**: < 200 units/month
    - **🟡 Medium**: 200-2000 units/month
    - **🟢 High**: > 2000 units/month
    """)

# Main input form
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Book Information")
    
    # Create two columns for inputs
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        category = st.selectbox(
            "📖 Category",
            ["Self-help", "Fiction", "Business", "Education", "Children"],
            help="Select the primary category/genre of your book"
        )
        
        current_price = st.number_input(
            "💰 Current Price (VND)",
            min_value=1000,
            value=150000,
            step=1000,
            help="The selling price of your book"
        )
        
        original_price = st.number_input(
            "💵 Original Price (VND)",
            min_value=1000,
            value=200000,
            step=1000,
            help="The list/original price before any discounts"
        )
    
    with input_col2:
        avg_rating = st.slider(
            "⭐ Average Rating",
            0.0, 5.0, 4.0, 0.1,
            help="Average customer rating (0-5 stars)"
        )
        
        n_review = st.number_input(
            "💬 Number of Reviews",
            min_value=0,
            value=100,
            step=10,
            help="Total number of customer reviews"
        )
        
        pages = st.number_input(
            "📄 Number of Pages",
            min_value=1,
            value=300,
            step=10,
            help="Total page count of the book"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Calculate discount percentage
    if original_price > 0:
        discount_pct = ((original_price - current_price) / original_price) * 100
        st.info(f"💸 Discount: {discount_pct:.1f}%")

with col2:
    st.subheader("📋 Input Summary")
    st.markdown(f"""
    **Category:** {category}  
    **Price:** {current_price:,.0f} VND  
    **Original:** {original_price:,.0f} VND  
    **Rating:** {'⭐' * int(avg_rating)} {avg_rating}/5.0  
    **Reviews:** {n_review:,}  
    **Pages:** {pages:,}
    """)

# Prediction button
st.markdown("<br>", unsafe_allow_html=True)
predict_button = st.button("🔮 Predict Demand", use_container_width=True)

if predict_button:
    # Validate inputs
    if current_price > original_price:
        st.error("⚠️ Current price cannot be higher than original price!")
    else:
        with st.spinner("🔄 Analyzing book characteristics..."):
            payload = {
                "category": category,
                "current_price": current_price,
                "original_price": original_price,
                "avg_rating": avg_rating,
                "n_review": n_review,
                "pages": pages
            }
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("---")
                    st.subheader("📊 Prediction Results")
                    
                    # Display results in columns
                    res_col1, res_col2, res_col3 = st.columns(3)
                    
                    with res_col1:
                        st.metric(
                            label="📦 Predicted Monthly Sales",
                            value=f"{result['predicted_quantity']:,.0f} units"
                        )
                    
                    with res_col2:
                        demand_level = result['demand_level']
                        demand_emoji = {
                            'Low': '🔴',
                            'Medium': '🟡',
                            'High': '🟢'
                        }.get(demand_level, '⚪')
                        
                        st.metric(
                            label="📈 Demand Level",
                            value=f"{demand_emoji} {demand_level}"
                        )
                    
                    with res_col3:
                        # Calculate potential revenue
                        potential_revenue = result['predicted_quantity'] * current_price
                        st.metric(
                            label="💰 Potential Revenue",
                            value=f"{potential_revenue:,.0f} VND"
                        )
                    
                    # Additional insights
                    st.markdown("---")
                    st.subheader("💡 Insights")
                    
                    if demand_level == "High":
                        st.success("✅ Great potential! This book is expected to perform well. Consider stocking up!")
                    elif demand_level == "Medium":
                        st.info("📊 Moderate demand expected. Monitor performance and adjust inventory accordingly.")
                    else:
                        st.warning("⚠️ Lower demand predicted. Consider promotional strategies or price adjustments.")
                    
                    # Recommendations
                    with st.expander("📋 View Recommendations"):
                        st.markdown("**Suggestions to improve demand:**")
                        if avg_rating < 4.0:
                            st.markdown("- ⭐ Focus on improving book quality to increase ratings")
                        if n_review < 50:
                            st.markdown("- 💬 Encourage more customer reviews")
                        if discount_pct < 10:
                            st.markdown("- 💸 Consider offering promotional discounts")
                        if avg_rating >= 4.5 and n_review >= 100:
                            st.markdown("- 🎉 Excellent ratings and reviews! Leverage these in marketing")
                
                else:
                    st.error(f"❌ Error: Received status code {response.status_code}")
                    st.error(f"Details: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Cannot reach the API server. Make sure it's running on http://127.0.0.1:8000")
            except requests.exceptions.Timeout:
                st.error("❌ Timeout Error: The request took too long. Please try again.")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>📚 Book Demand Prediction System | Powered by Machine Learning</small>
</div>
""", unsafe_allow_html=True)
