import streamlit as st

st.set_page_config(
    page_title= "My Next Pint",
    layout="wide",
    page_icon='🍻',
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'A personal project by abhaypai@vt.edu',
    }
)

st.html('<head><meta name="google-site-verification" content="vopOWvrbazdKv3WU5Uu7RchuHy8WnOsV8wL4rdj92Pk" /> </head> ')

st.markdown("""
        <style>
               .block-container {
                    padding-top: 2.5rem;
                    padding-bottom: 0rem;
                    padding-left: 2.5rem;
                    padding-right: 2.5rem;
                }
        </style>
        """, unsafe_allow_html=True)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

reco_page = st.Page(
    page = "Pages/1_Recommender.py",
    title = "Recommender Engine",
    default = True
)

review_stats_page = st.Page(
    page = "Pages/2_Stats.py",
    title = "Reviews Stats"
)

prod_stats_page = st.Page(
    page = "Pages/3_Prod_Stats.py",
    title = "Production Stats"

)

st.logo("images/MNP-icon.png", size = "large")

recommend=[reco_page]
charts=[review_stats_page, prod_stats_page]

pg = st.navigation(
    {
        "Recommender" : recommend,
        "Stats for Geeks" : charts
    }
)

pg.run()
