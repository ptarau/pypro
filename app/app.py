import os

import streamlit as st

from natlog.natlog import *

print('starting')

st.set_page_config(layout="wide")

st.title('Natlog')

left, right = st.columns((1, 1))

upload_dir='natprogs/'

uploaded_file = st.sidebar.file_uploader('Select a File', type=['.nat'])


def handle_uploaded():
    if uploaded_file is None: return None
    fpath = save_uploaded_file()
    suf = fpath[-4:]
    fname = fpath[:-4]
    if suf == '.nat':
        return fpath
    else:
        with right:
            st.write('Please upload a .nat file!')


def save_uploaded_file():
    name = uploaded_file.name
    fname = os.path.join(upload_dir, name)
    if exists_file(fname): return fname
    ensure_path(upload_dir)
    with open(fname, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return fname


def ensure_path(fname):
    folder, _ = os.path.split(fname)
    os.makedirs(folder, exist_ok=True)


def exists_file(fname):
    """ if it exists as file or dir"""
    return os.path.exists(fname)


with st.sidebar:
    with st.form('Query'):
        if 'fname' in st.session_state:
            fname = st.session_state.fname
        else:
            fname = ""
        fname = st.text_input('File to consult?', fname)
        st.session_state.fname = fname

        if 'question' in st.session_state:
            question = st.session_state.question
        else:
            question = ""
        question = st.text_area(
            'Query?',
            question)
        st.session_state.question=question

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
    nat = Natlog(file_name=fname)
    answers = list(nat.solve(question))

    with left:
        st.write('Answers:')
        # answers = ['one','two']
        if not answers:
            st.write("I do not know.")
        else:
            for sent in answers:
                st.write(sent)


if uploaded_file:
    fname = handle_uploaded()
    if fname is not None: st.session_state.fname = fname

if query_it:
    do_query()
