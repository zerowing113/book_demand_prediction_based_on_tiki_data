import streamlit as st
import pandas as pd
import joblib

# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="Book Demand Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Load model (cached)
# =========================
@st.cache_resource
def load_model():
    return joblib.load("models/final_model.pkl")

model = load_model()

# =========================
# Custom CSS
# =========================
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

# =========================
# Header
# =========================
st.title("📚 Book Demand Prediction System")
st.markdown("### Decision-support tool for bookstore inventory planning")
st.markdown("---")

st.markdown("""
<div class="info-box">
<strong>ℹ️ How it works:</strong>  
Enter book characteristics to receive an estimated demand level.
The model is designed to support (not replace) human inventory decisions.
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("📊 About This Tool")
    st.markdown("""
This application predicts book demand using:
- Category
- Pricing information
- Ratings and reviews
- Book length
""")

    st.markdown("---")
    st.subheader("🎯 Demand Levels")
    st.markdown("""
- 🔴 **Low**: < 200 units/month  
- 🟡 **Medium**: 200 – 2,000 units/month  
- 🟢 **High**: > 2,000 units/month  
""")

# =========================
# Input Section
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Book Information")

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        category = st.selectbox(
            "📖 Category",
            ["Self-help", "Fiction", "Business", "Education", "Children"]
        )

        current_price = st.number_input(
            "💰 Current Price (VND)",
            min_value=1000,
            value=150000,
            step=1000
        )

        original_price = st.number_input(
            "💵 Original Price (VND)",
            min_value=1000,
            value=200000,
            step=1000
        )

    with input_col2:
        avg_rating = st.slider(
            "⭐ Average Rating",
            0.0, 5.0, 4.0, 0.1
        )

        n_review = st.number_input(
            "💬 Number of Reviews",
            min_value=0,
            value=100,
            step=10
        )

        pages = st.number_input(
            "📄 Number of Pages",
            min_value=1,
            value=300,
            step=10
        )

    if original_price > 0:
        discount_pct = ((original_price - current_price) / original_price) * 100
        st.info(f"💸 Discount: {discount_pct:.1f}%")

with col2:
    st.subheader("📋 Input Summary")
    st.markdown(f"""
**Category:** {category}  
**Current Price:** {current_price:,.0f} VND  
**Original Price:** {original_price:,.0f} VND  
**Rating:** {avg_rating}/5.0  
**Reviews:** {n_review:,}  
**Pages:** {pages:,}
""")

# =========================
# Prediction
# =========================
st.markdown("<br>", unsafe_allow_html=True)
predict_button = st.button("🔮 Predict Demand", use_container_width=True)

if predict_button:
    if current_price > original_price:
        st.error("⚠️ Current price cannot be higher than original price!")
    else:
        with st.spinner("🔄 Analyzing book characteristics..."):
            try:
                input_df = pd.DataFrame([{
                    "category": category,
                    "current_price": current_price,
                    "original_price": original_price,
                    "avg_rating": avg_rating,
                    "n_review": n_review,
                    "pages": pages
                }])

                predicted_quantity = model.predict(input_df)[0]

                if predicted_quantity < 200:
                    demand_level = "Low"
                elif predicted_quantity < 2000:
                    demand_level = "Medium"
                else:
                    demand_level = "High"

                st.markdown("---")
                st.subheader("📊 Prediction Results")

                res_col1, res_col2, res_col3 = st.columns(3)

                with res_col1:
                    st.metric(
                        "📦 Predicted Monthly Sales",
                        f"{predicted_quantity:,.0f} units"
                    )

                with res_col2:
                    emoji = {"Low": "🔴", "Medium": "🟡", "High": "🟢"}[demand_level]
                    st.metric(
                        "📈 Demand Level",
                        f"{emoji} {demand_level}"
                    )

                with res_col3:
                    revenue = predicted_quantity * current_price
                    st.metric(
                        "💰 Potential Revenue",
                        f"{revenue:,.0f} VND"
                    )

                st.markdown("---")
                st.subheader("💡 Business Insight")

                if demand_level == "High":
                    st.success("✅ High demand expected. Prioritize stocking this book.")
                elif demand_level == "Medium":
                    st.info("📊 Moderate demand. Monitor performance and adjust inventory.")
                else:
                    st.warning("⚠️ Low demand expected. Consider promotions or limited stock.")

            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#666; padding:1rem;'>
<small>📚 Book Demand Prediction System | Machine Learning Project</small>
</div>
""", unsafe_allow_html=True)
