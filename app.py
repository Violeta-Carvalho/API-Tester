from datetime import datetime
import streamlit as st
import utils

st.title("API Tester")

session_defaults = {
    "url": None,
    "method": None,
    "header_keys": [],
    "header_values": [],
    "request_time": None,
    "request_body": None,
    "request_headers": None,
    "response_time": None,
    "response_headers": None,
    "response_code": None,
    "responde_body": None,
}

for key, default_value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

header_keys_quantity = st.number_input(
    "Amount of Headers",
    min_value=1,
    step=1,
    value=utils.check_value(st.session_state["header_keys"]),
)

current_quantity = len(st.session_state["header_keys"])

if header_keys_quantity > current_quantity:
    for _ in range(header_keys_quantity - current_quantity):
        st.session_state["header_keys"].append("")
        st.session_state["header_values"].append("")


elif header_keys_quantity < current_quantity:
    st.session_state["header_keys"] = st.session_state["header_keys"][
        :header_keys_quantity
    ]
    st.session_state["header_values"] = st.session_state["header_values"][
        :header_keys_quantity
    ]

with st.form(key="basic_form"):
    st.session_state["method"] = st.selectbox(
        label="Method",
        options=["GET", "POST", "PUT", "DELETE", "PATCH"],
    )
    st.session_state["url"] = st.text_input("URL", value=st.session_state["url"])

    with st.expander("Headers", expanded=True):
        cols = st.columns(2)
        for i in range(header_keys_quantity):
            with cols[0]:
                st.session_state["header_keys"][i] = st.text_input(
                    f"#{i + 1} Key", value=st.session_state["header_keys"][i]
                )

            with cols[1]:
                st.session_state["header_values"][i] = st.text_input(
                    f"#{i + 1} Value", value=st.session_state["header_values"][i]
                )

    st.session_state["request_body"] = st.text_area(
        "Body", value=st.session_state["request_body"]
    )

    submit_button = st.form_submit_button(label="Send")

# Handle form submission
if submit_button:
    st.session_state = utils.make_request(st.session_state)
    st.write(f"Request sent on: {st.session_state["request_time"].isoformat()}")
    st.write(f"Response received on: {st.session_state["response_time"].isoformat()}")
    st.write(f"Response Code: {st.session_state["response_code"]}")
    st.write(
        f"Total Wait Time: {st.session_state["response_time"] - st.session_state["request_time"]}"
    )
    st.write("Response Headers:")
    st.code(st.session_state["response_headers"])

    st.write("Response Body:")
    st.code(st.session_state["response_body"])

    json = utils.format_download_json(st.session_state)

    st.download_button(
        label="Download Test Results",
        data=json,
        file_name="test.json",
        mime="application/json",
    )
