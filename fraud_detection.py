import streamlit as st
import pandas as pd
import joblib
import time


model = joblib.load("fraud_detection_pipeline.pkl")


st.set_page_config(page_title="Fraud Detection App", page_icon="🔍", layout="wide")


st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>🔍 Fraud Detection App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Enter the transaction details below and click <b>Predict</b> to check if it is fraudulent.</p>", unsafe_allow_html=True)
st.divider()

with st.expander("ℹ️ How to use this app?"):
    st.markdown("""
    - Fill in the transaction details in the form below.
    - Click on the **Predict** button.
    - The app will tell you whether the transaction is **FRAUDULENT** or **VALID**.
    """)


st.sidebar.header("Settings")
show_progress = st.sidebar.checkbox("Show progress animation", value=True)


col1, col2 = st.columns(2)

with col1:
    transaction_type = st.selectbox("Transaction Type", ['PAYMENT', 'TRANSFER', 'CASH_OUT'])
    amount = st.number_input("Amount", min_value=0.0, value=0.0, step=100.0)
    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=0.0, step=100.0)

with col2:
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=0.0, step=100.0)
    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0, step=100.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=0.0, step=100.0)


if st.button("🚀 Predict"):
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
    }])

    if show_progress:
        with st.spinner("Analyzing transaction..."):
            time.sleep(1)

    prediction = model.predict(input_data)[0]

    st.divider()
    if prediction == 1:
        st.error("⚠️ FRAUD TRANSACTION DETECTED!")
        st.markdown("<h3 style='color:red; text-align:center;'>🚫 Fraudulent Transaction</h3>", unsafe_allow_html=True)
    else:
        st.success("✅ VALID TRANSACTION")
        st.markdown("<h3 style='color:green; text-align:center;'>✔️ Legitimate Transaction</h3>", unsafe_allow_html=True)

