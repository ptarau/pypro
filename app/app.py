import os
import streamlit as st
from natlog.natlog import *


print('starting')

st.set_page_config(layout="wide")

st.title('Natlog')

left, right = st.columns((1, 1))

uploaded_file = st.sidebar.file_uploader('Select a File', type=['.nat'])


def handle_uploaded():
    if uploaded_file is None: return None
    fpath = save_uploaded_file()
    suf = fpath[-4:]
    fname = fpath[:-4]
    if suf == '.nat':
        return fname
    else:
        with right:
            st.write('Please upload a .nat file!')

def save_uploaded_file():
    upload_dir = './natprogs/'
    fname = uploaded_file.name
    fpath = os.path.join(upload_dir, fname)
    if exists_file(fpath): return fpath
    ensure_path(upload_dir)
    with open(fpath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return fpath

def ensure_path(fname):
    folder, _ = os.path.split(fname)
    os.makedirs(folder, exist_ok=True)

def exists_file(fname):
    """ if it exists as file or dir"""
    return os.path.exists(fname)


with st.sidebar:
    with st.form('Query'):
        nat_file_name = 'natprogs/'+st.text_input('File to consult?','family.nat')
        question = st.text_area(
            'Query?',
            "brother_of X B?")

        query_it = st.form_submit_button('Submit your question!')

        if query_it:
            with left:
                st.write('Query:' + " " + question)


def do_load():

    fname = handle_uploaded()

    while not fname:
        st.write('Please upload a file!')

    print('loading fname:', fname)


def do_query():
    nat = Natlog(file_name=nat_file_name)
    answers=list(nat.solve(question))

    with left:
        st.write('Answers:')
        #answers = ['one','two']
        if not answers:
            st.write("I do not know.")
        else:
            for sent in answers:
                st.write(sent)


if uploaded_file:
    handle_uploaded()

if query_it:
    do_query()
