import streamlit as st
import pandas as pd
from multiprocessing import Process
from SPIDERtopic_wise import call_query
import base64

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def app():
	st.title("Spider-MAHE")
	st.markdown("# Search Professors:")
	st.write()
	user_input = st.text_input("Just enter the query!")
	if st.button("Submit") and user_input!="":
		p = Process(target=call_query, args=(user_input,))
		p.start()
		p.join()
		df = pd.read_csv("Current.csv")
		st.write(df)
		tmp_download_link = download_link(df, "QueryResults.csv", "Click here to download!")
		st.markdown(tmp_download_link, unsafe_allow_html=True)
		os.remove("Current.csv")

if __name__ == '__main__':
	app()