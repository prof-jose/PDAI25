import cohere
import json
import pandas as pd
import streamlit as st


SYSTEM_PROMPT = """
    The user will write a text simulating an electronic health record.
    Extract the information necessary to populate this json object:
    {
    "age": X,
    "temperature": X,
    "reason_visit": "X",
    "tests_performed": ["X", "X", "X"],
    "diagnosis": "X"
    }
    If the information is not present, return "Not found".
    Respond only with the json dictionary,
    don't put it inside triple quotation marks.
"""


DB_COLUMNS = [
    "age", "temperature", "reason_visit", "tests_performed", "diagnostic"
]

DF_COLUMN_CONFIG = {
    "age": st.column_config.NumberColumn("Age"),
    "temperature": st.column_config.ProgressColumn(
        "Temperature", min_value=36.5, max_value=42.0, format="%.1f ºC",
        width="small"),
    "reason_visit": st.column_config.TextColumn("Reason"),
    "tests_performed": st.column_config.ListColumn("Tests", width="medium"),
    "diagnosis": st.column_config.TextColumn("Diagnosis")
}


@st.cache_resource
def get_client():
    """Initialize the cohere LLM."""
    with open("cohere.key") as f:
        COHERE_API_KEY = f.read()
    cohere_client = cohere.ClientV2(COHERE_API_KEY)

    return cohere_client


def clean_tests(x):
    """
    Clean the tests_performed string
    (necessary to display the information correctly
    according to pandas and streamlit way of working).
    """
    return x.replace("[", "")\
            .replace("]", "")\
            .replace("\"", "")\
            .replace("'", "")


def get_database():
    """
    Read database from a file or create an empty one.
    """
    try:
        df = pd.read_csv("db.csv")
        df['tests_performed'] = df['tests_performed'].apply(clean_tests)
    except FileNotFoundError:
        st.warning("DB file not found, creating new DB.")
        df = pd.DataFrame(
            columns=DB_COLUMNS,
            )
        df = pd.DataFrame({
            'age': pd.Series([], dtype='int'),
            'temperature': pd.Series([], dtype='int'),
            'reason_visit': pd.Series([], dtype='str'),
            'tests_performed': pd.Series([], dtype='str'),
            'diagnosis': pd.Series([], dtype='str')
            })

    return df


def call_llm(text, client):
    """Perform the actual LLM call and output the text response."""
    response = client.chat(
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': text}
        ],
        model='command-r-plus'
    )
    text_response = response.message.content[0].text
    return text_response


def process_text(text, df, client):
    """
    Process the output of the LLM, and:
    - Display the processed information, already structured
    - Add the structured information to the database
    """

    if text:
        with st.spinner("Calling LLM..."):

            text_response = call_llm(text, client)

            with st.expander("See last patient processed"):
                st.json(text_response)

            st.subheader("Patients in queue:")

            # Add row to dataframe
            d = json.loads(text_response)
            d['tests_performed'] = str(d['tests_performed'])
            df.loc[len(df), :] = d
            df['tests_performed'] = df['tests_performed'].apply(clean_tests)

            df.to_csv("db.csv", index=False)


def main():
    """Execute main program flow."""

    client = get_client()
    df = get_database()

    st.sidebar.title("Using LLMs to structure data")
    text = st.sidebar.text_area("Triage report:")
    if st.sidebar.button("Submit"):
        process_text(text, df, client)

    st.dataframe(df, column_config=DF_COLUMN_CONFIG)


if __name__ == "__main__":
    main()
