import streamlit as st
######################

def display(products):

    for product in products:
        col1, col2 = st.columns(2)
        with col1:
            st.image(product[3])

        with col2:
            st.write(product[0])
            st.write(product[1])
            st.write(f"shipment from {product[2]}")
            st.link_button("purchase", product[4])