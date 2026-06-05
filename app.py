#Job: Streamlit UI for Travel Planner

import streamlit as st
from agent import plan_trip, index, destinations

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="⛺️",
    layout="centered"

)

st.title("🗺️ AI Travel Planner")
st.subheader("Plan your perfect Indian trip with AI")
st.markdown("---")

st.markdown("### Tell me about your dream trip")

user_request = st.text_area(
    "Describe your trip",
    placeholder="""Examples: 
     - Plan a 3 day trip to Goa in December, budget 15000 rupees
     - I want a romantic 5 day Kerala trip, comfort style
     - Budget trip to Kodaicanal for 4 days in January""",
     height=180
)

col1, col2, col3 = st.columns(3)

with col1:
    destination = st.selectbox("Destination", [
        "Let AI decide",
        "Goa",
        "Manali",
        "Kerala",
        "Andaman",
        "Rajasthan"
    ])

with col2:
    duration = st.selectbox("Duration", [
         "Let AI decide",
        "3 days",
        "4 days",
        "5 days",
        "7 days"
    ])

with col3:
    budget_style = st.selectbox("Budget Style", [
        "Budget",
        "Comfort",
        "Luxury"
    ])

st.markdown("----")

if st.button("🚀 Plan my Trip", type="primary"):
    if user_request:

        enhanced_request = user_request
        if destination != "Let AI decide":
            enhanced_request += f" Destination: {destination}."
        if duration != "Let AI decide":
            enhanced_request += f" Duration: {duration}."
        enhanced_request += f" Budget style: {budget_style}."

        #Show loading state

        with st.spinner("🌀 AI is planning your trip..."):
            try:
                itinerary = plan_trip(enhanced_request)

                #Display results

                st.markdown("---")
                st.markdown("##✈️ Your personal travel plan")
                st.markdown(itinerary)

                #Add download button

                st.download_button(
                    label="🏷️ Download Itinerary",
                    data=itinerary,
                    file_name=f"travel_plan_{destination}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    else:
        st.warning("Please describe your trip first")

st.markdown("---")
st.markdown(""" 
            **Destination available:** Goa. Manali. Kerala. Rajasthan. Andaman Islands""")