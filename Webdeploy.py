#from turtle import onclick
import streamlit as st
import joblib as jb
import pandas as pd
import webbrowser as wb

#from torch import matrix_power

st.set_page_config(
        page_title="VRL Novel Recommender",
        page_icon="MyLogoLight.png",
        layout="wide",
    )


st.image("MyLogoLight.png")



#st.markdown("<h1><font color=#03b1fc>Book Recommendation Engine</h1>",unsafe_allow_html=True)
st.title(":books: Novel Recommender Engine :books:")
with st.expander("Select the Type of Recommendation"):
    type_of_recommd = st.sidebar.selectbox("Recommender based on",["Trending","Previous Reads"])

def RecommendBooks(bookname,simi_df):
    simi_books=simi_df.sort_values(bookname,ascending=False)[1:13]["Book-Title"]
    info= pd.read_csv("CollabFiltBooks.csv",index_col=0)
    sim_info= info[info["Book-Title"].isin(simi_books)]
    
    # sort on the basis of avg rating
    sim_info= sim_info.sort_values("Book-Rating",ascending=False)
    return sim_info


def BuyButton(url):
    buy_p1='''
    <head>
<style>
    button{
        border: 1px solid grey;
        border-radius: 10%;
        padding: 10px 50px; 
        background-color: white;
        text-align: center;
        font-size: 14px;
    }
    button:hover{
        border:1px solid red;
        color: red;
    }
</style>
</head>
    '''
    a='<a href="{}"  target="_blank">'.format(url)
    
    buy_p2='''
    <button> Buy Now </button> </a> </body>
    '''
    
    return buy_p1+a+buy_p2

def ReadCollabMatrix():
    dfs=[]
    for i in range(1,8):
        dfs.append(jb.load("Col{}".format(i)))
    matrix = pd.concat(dfs)
    return matrix

def layout(top_books_df):
    trend = top_books_df
    print(trend)
    amazon_url_search=r"https://www.amazon.in/s?k="
    
    for i in range(0,12,4):
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.image(trend.iloc[i]["Image-URL-L"],width=150,caption=trend.iloc[i]["Book-Title"])
            s=""
            for r in range(int(trend.iloc[i]["Book-Rating"])):
                s+=":star: "
            st.markdown("###### "+s)
            with st.expander("More Details"):
                #Info
                st.markdown("###### Author's Name")
                st.markdown("{}".format(trend.iloc[i]["Book-Author"])) 
                st.markdown("###### Publisher")
                st.markdown( "{}".format(trend.iloc[i]["Publisher"]))

                # Buy section
                url=amazon_url_search+trend.iloc[i]["Book-Title"]+" By {}".format(trend.iloc[i]["Book-Author"])
                st.markdown(BuyButton(url),unsafe_allow_html=True)
                
            st.write("\n")
                    
        with col2:
            st.image(trend.iloc[i+1]["Image-URL-L"],width=150,caption=trend.iloc[i+1]["Book-Title"])
            s=""
            for r in range(int(trend.iloc[i+1]["Book-Rating"])):
                s+=":star: "
            st.markdown("###### "+s)
            with st.expander("More Details"):
                st.markdown("###### Author's Name")
                st.markdown("{}".format(trend.iloc[i+1]["Book-Author"])) 
                st.markdown("###### Publisher")
                st.markdown( "{}".format(trend.iloc[i+1]["Publisher"]))
                
                # Buy section
                url=amazon_url_search+trend.iloc[i+1]["Book-Title"]+" By {}".format(trend.iloc[i+1]["Book-Author"])
                st.markdown(BuyButton(url),unsafe_allow_html=True)
                
                
            st.write("\n")


        with col3:
            st.image(trend.iloc[i+2]["Image-URL-L"],width=150,caption=trend.iloc[i+2]["Book-Title"])
            s=""
            for r in range(int(trend.iloc[i+2]["Book-Rating"])):
                s+=":star: "
            st.markdown("###### "+s)
            with st.expander("More Details"):
                st.markdown("###### Author's Name")
                st.markdown("{}".format(trend.iloc[i+2]["Book-Author"])) 
                st.markdown("###### Publisher")
                st.markdown( "{}".format(trend.iloc[i+2]["Publisher"]))
                
                # Buy section
                url=amazon_url_search+trend.iloc[i+2]["Book-Title"]+" By {}".format(trend.iloc[i+2]["Book-Author"])
                st.markdown(BuyButton(url),unsafe_allow_html=True)

            st.write("\n")


        with col4:
            st.image(trend.iloc[i+3]["Image-URL-L"],width=150,caption=trend.iloc[i+3]["Book-Title"])
            s=""
            for r in range(int(trend.iloc[i+3]["Book-Rating"])):
                s+=":star: "
            st.markdown("###### "+s)
            with st.expander("More Details"):
                st.markdown("###### Author's Name")
                st.markdown("{}".format(trend.iloc[i+3]["Book-Author"])) 
                st.markdown("###### Publisher")
                st.markdown( "{}".format(trend.iloc[i+3]["Publisher"]))

                # Buy section
                url=amazon_url_search+trend.iloc[i+3]["Book-Title"]+" By {}".format(trend.iloc[i+3]["Book-Author"])
                st.markdown(BuyButton(url),unsafe_allow_html=True)

            st.write("\n")

    
if type_of_recommd == "Trending":
    trend=pd.read_csv("TrendingBooks.csv",index_col=0)
    _,_,col3,_,_= st.columns(5)
    if col3.button("Recommend Trendy Novels"):
        st.header("")
        st.header("")
        layout(trend)

elif type_of_recommd == "Previous Reads":
    #simi_matrix = jb.load("CollabMatrix.pkl")
    simi_matrix = ReadCollabMatrix()
    bookname = st.selectbox("Novel Read Recently",simi_matrix.index)
    _,_,col3,_,_= st.columns(5)
    if col3.button("Recommend Some \n Novels"):
        topbooks = RecommendBooks(bookname,simi_matrix[bookname].reset_index())
        st.header("")
        st.header("")
        layout(topbooks)

        


