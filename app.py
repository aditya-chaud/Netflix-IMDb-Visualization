import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Netflix IMDb Visualization",
    page_icon=":bar_chart:",
    layout="wide"
)

st.header("Visualizing Netflix IMDB Scores and Votes")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    # df = df.set_index(df.columns[0])

else:
    df=pd.read_csv("./Netflix TV Shows and Movies.csv")
    df=df.set_index(df.columns[0])

#Filter on the sidebar
selected_filters = st.sidebar.multiselect("Select the filter", df["type"].unique())
if not selected_filters:
    df1=df.copy()
    startYear=int(df1["release_year"].min())
    endYear=int(df1["release_year"].max())
if selected_filters:
    df1 = df[df["type"].isin(selected_filters)]
    startYear=int(df1["release_year"].min())
    endYear=int(df1["release_year"].max())


#slider for release year of tv shows and movie
values = st.sidebar.slider(
    'Select a range of values',
    startYear, endYear, value=(startYear, endYear), step=1
)
filtered_df = df[(df["release_year"] >= values[0]) & (df["release_year"] <= values[1])]
st.write("From", values[0], "year","To ", values[1], "year")

#Previewing datasets
if not selected_filters:
    st.expander("Data Preview").dataframe(
        filtered_df, 
        column_config={
                "release_year":st.column_config.NumberColumn(format="%d")
            },)
if selected_filters:
    df2=filtered_df[filtered_df["type"].isin(selected_filters)]
    st.expander("Data Preview").dataframe(
        df2,
        column_config={
            "release_year":st.column_config.NumberColumn(format="%d")
            },)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Average IMDB Scores")
    if not selected_filters:
        # st.expander("Data Preview").dataframe(filtered_df)
        avg_score = round(filtered_df["imdb_score"].mean(), 1)
        st.subheader(avg_score)
    if selected_filters:
        df2=filtered_df[filtered_df["type"].isin(selected_filters)]
        # st.expander("Data Preview").dataframe(df2)
        # Calculate the average IMDb score for the selected filters
        avg_score = round(df2["imdb_score"].mean(), 1)
        st.subheader(avg_score)
with col2:
    st.subheader("Average IMDB Votes")
    if not selected_filters:
        # Calculate the average IMDb votes for the selected filters
        avg_votes = round(filtered_df["imdb_votes"].mean())
        st.subheader(avg_votes)
    if selected_filters:
        df2=filtered_df[filtered_df["type"].isin(selected_filters)]
        avg_votes=round(df2["imdb_votes"].mean())
        st.subheader(avg_votes)

# st.expander("Data Preview").dataframe(filtered_df)

fig, (ax1, ax2) = plt.subplots(figsize=(12, 5), nrows=1, ncols=2, sharex=False, gridspec_kw={'hspace': 1})

type_counts = df['type'].value_counts()
#pie chart showing the total movie and show percentage
ax1.pie(type_counts.values, labels=type_counts.index, autopct='%.0f%%')
ax1.set_title('Distribution of Types')

# Boxplot showing imdb score by type
sns.boxplot(data=df, x="type", y="imdb_score", ax=ax2)
ax2.set_title('Boxplot of IMDb Scores by Type')
# plt.tight_layout()
st.pyplot(fig)



fig1, (ax1,ax2) = plt.subplots(figsize=(18, 10), nrows=2, ncols=1, sharex=False, gridspec_kw={'hspace': 0.5})
if not selected_filters:
    #lineplot
    yearly_avg_imdb_score = filtered_df.groupby('release_year')['imdb_score'].mean().reset_index()
    sns.lineplot(data=yearly_avg_imdb_score, x='release_year', y='imdb_score',ax=ax1)
    # Set plot title and labels
    ax1.set_title('Average IMDb Score Trends Over Years', fontsize=25)
    ax1.set_xlabel('Release Year',fontsize=15)
    ax1.set_ylabel('Average IMDb Score',fontsize=15)

    yearly_counts = filtered_df['release_year'].value_counts().sort_index().reset_index()
    yearly_counts.columns = ['Release Year', 'Count']

    sns.lineplot(data=yearly_counts, x='Release Year', y='Count', ax=ax2)
    ax2.set_title('Number of releases over years', fontsize=25)
    ax2.set_xlabel('Release Year', fontsize=15)
    ax2.set_ylabel('Number of releases', fontsize=15)

if selected_filters:
    df2 = filtered_df[filtered_df["type"].isin(selected_filters)]
    yearly_avg_imdb_score = df2.groupby('release_year')['imdb_score'].mean().reset_index()
    #lineplot
    sns.lineplot(data=yearly_avg_imdb_score, x='release_year', y='imdb_score',ax=ax1)
    # Set plot title and labels
    ax1.set_title('Average IMDb Score Trends Over Years', fontsize=25)
    ax1.set_xlabel('Release Year', fontsize=15)
    ax1.set_ylabel('Average IMDb Score', fontsize=15)

    yearly_counts = df2['release_year'].value_counts().sort_index().reset_index()
    yearly_counts.columns = ['Release Year', 'Count']

    sns.lineplot(data=yearly_counts, x='Release Year', y='Count', ax=ax2)
    ax2.set_title('Number of releases over years', fontsize=25)
    
    ax2.set_xlabel('Release Year', fontsize=15)
    ax2.set_ylabel('Number of releases', fontsize=15)

st.pyplot(fig1)


fig3, axes = plt.subplots(figsize=(28, 20), nrows=2, ncols=2, sharex=False, gridspec_kw={'hspace': 0.5})
ax1, ax2, ax3, ax4 = axes.flatten()
# First subplot
if not selected_filters:
    # Visualizing distribution of IMDb scores
    sns.histplot(filtered_df['imdb_score'], kde=True, ax=ax1)
    ax1.set_title('IMDb Scores Distribution', fontsize=35)
    ax1.set_xlabel('IMDb Score',fontsize=15)
    ax1.set_ylabel('Count',fontsize=15)

    sns.countplot(data=filtered_df, x='age_certification', ax=ax2)
    ax2.set_title('Age Certification Distribution', fontsize=25)
    ax2.set_xlabel('Age Certification',fontsize=15)
    ax2.set_ylabel('Count',fontsize=15)


    sns.scatterplot(data=filtered_df,x='runtime', y='imdb_score', ax=ax3)
    ax3.set_title("IMDb Score vs Runtime", fontsize=35)
    ax3.set_xlabel('Runtime',fontsize=15)
    ax3.set_ylabel('IMDb Score',fontsize=15)

    sns.violinplot(data=filtered_df,x='age_certification', y='imdb_score', ax=ax4)
    ax4.set_title("IMDb Score based on Age Certification", fontsize=35)
    ax4.set_xlabel('Age Certification',fontsize=15)
    ax4.set_ylabel('IMDb Score',fontsize=15)

if selected_filters:
    df2 = filtered_df[filtered_df["type"].isin(selected_filters)]
    # Visualizing distribution of IMDb scores for the filtered DataFrame
    sns.histplot(df2['imdb_score'], kde=True, ax=ax1)
    ax1.set_title('Filtered IMDb Scores Distribution', fontsize=35)
    ax1.set_xlabel('IMDb Score',fontsize=15)
    ax1.set_ylabel('Count',fontsize=15)

    sns.countplot(data=df2, x='age_certification', ax=ax2)
    ax2.set_title('Age Certification Distribution', fontsize=25)
    ax2.set_xlabel('Age Certification',fontsize=15)
    ax2.set_ylabel('Count',fontsize=15)

    sns.scatterplot(data=df2,x='runtime', y='imdb_score', ax=ax3)
    ax3.set_title("IMDb Score vs Runtime", fontsize=35)
    ax3.set_xlabel('Runtime',fontsize=15)
    ax3.set_ylabel('IMDb Score',fontsize=15)

    sns.violinplot(data=df2,x='age_certification', y='imdb_score', ax=ax4)
    ax4.set_title("IMDb Score based on Age Certification", fontsize=35)
    ax4.set_xlabel('Age Certification',fontsize=15)
    ax4.set_ylabel('IMDb Score',fontsize=15)

# Display the Matplotlib figure in Streamlit
st.pyplot(fig3)


top_scores = filtered_df.sort_values(by='imdb_score', ascending=False).head(10)
if not selected_filters:
    
    fig4 = px.treemap(top_scores, path=['title'], values='imdb_score', title='Top IMDb Scores by Title')
    # st.expander("Data Preview").dataframe(top_scores)

if selected_filters:
    df2 = filtered_df[filtered_df["type"].isin(selected_filters)]
    top_scores = df2.sort_values(by='imdb_score', ascending=False).head(10)
    
    fig4 = px.treemap(top_scores, path=['title'], values='imdb_score', title='Top IMDb Scores by Title')
    # st.expander("Data Preview").dataframe(top_scores)

st.plotly_chart(fig4)