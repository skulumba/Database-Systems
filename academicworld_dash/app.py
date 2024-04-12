import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from mysql_utils import connect_to_database,execute_query,get_last_three_keywords
from dash import dash_table
from mongodb_utils import mongo_execute_query
from pymongo.errors import ServerSelectionTimeoutError
from neo4j_utils import Neo4jConnection
import plotly.express as px


# define Dash app
app = dash.Dash(__name__)
app.title = 'Researcher\'s Dashboard'
db = connect_to_database()

# define the layout
app.layout = html.Div([
    html.H1('Researcher\'s Dashboard', style={'text-align': 'center', 'margin-top': '50px'}),
    html.H4('Get top 5 publications by keyword[Mysql db]'),
    #Top 5 publications by keyword
    html.Div([
        dcc.Input(id='keyword-input', type='text', placeholder='Enter a keyword', style={'width': '40%'}),
        html.Button('Find', id='search-button', n_clicks=0, style={'margin-left': '10px', 'background-color': '#3f7fbf', 'color': 'white', 'border-radius': '10px'}),
    ], style={'display': 'flex', 'justify-content': 'left' }),
    
    html.Div([
        html.Div(id='search-results', style={'margin-top': '10px', 'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='citations-graph', style={'margin-top': '10px','width': '49%', 'display': 'inline-block', 'vertical-align': 'top', 'border-radius': '3px', 'border': '1px solid #ccc'}),
    ]),

    html.Div([
    html.H4('Top 5 Faculty Positions[Mysql db]'),    
    # Top 5 faculty positions in a given University
    html.Div([ 
        dcc.Input(id='university-name-input', type='text', placeholder='Enter a university name',style={'width': '40%'}),       
        html.Button('Find', id='position-count-button', n_clicks=0, style={'background-color': '#3f7fbf', 'color': 'white', 'border-radius': '10px'}), 
        ], style={'display': 'flex', 'justify-content': 'left'}),
        html.Div(id='position-count-table', style={'margin-top': '10px', 'width': '49%', 'display': 'inline-block'}),
        html.Div(id='pie-chart-container', style={'margin-top': '10px','width': '49%', 'display': 'inline-block', 'vertical-align': 'top', 'border-radius': '3px', 'border': '1px solid #ccc'})
    ]),

    #Add Keyword to DB and show las 3 keyword using a stored procedure 
    html.Div([
        html.H4('Add a new Keyword to the database[Mysql db]'),
        html.Div([
            html.Label('ID:'),
            dcc.Input(id='new-keyword-id',placeholder='Enter a ID', type='number', value='', style={'width': '35%'}),
            html.Label('Name:'),
            dcc.Input(id='new-keyword-name',placeholder='Enter Keyword', type='text', value='', style={'width': '30%'}),
            html.Button('Add', id='add-button', n_clicks=0, style={'margin-left': '10px', 'background-color': '#3f7fbf', 'color': 'white', 'border-radius': '10px'})
        ]),
        html.Div(id='add-output'),
        dash_table.DataTable(
        id='keyword-table',
        columns=[{"name": i, "id": i} for i in ['ID', 'Keyword']],
          style_data_conditional=[ {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)' } ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'
            },
        data=get_last_three_keywords(),
    )
    ], style={'width': '50%', 'float': 'left'}),
     
    #Delete Keyword from DB
     html.Div([
        html.H4('Delete a Keyword from the database[Mysql db]'),
        html.Div([
        dcc.Input(id='delete-keyword-id',placeholder='Enter ID', type='number', value='', style={'width': '40%'}),
        html.Button('Delete', id='delete-button', n_clicks=0, style={'margin-left': '10px', 'background-color': '#3f7fbf', 'color': 'white', 'border-radius': '10px'})
        ]),

        html.Div(id='delete-output', style={'margin-top': '10px'}),
    ], style={'width': '50', 'float': 'right'}),

     #Top Faculty Members by publications
     html.Div([
        html.H4('Top Faculty Members with the Highest Number of Publications[Mongo db]'),
        html.Div([
             dcc.Graph(
            id='publication-bar-graph',
            figure={
                'data': [
                    go.Bar(
                        x=[],y=[],orientation='h')
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Number of Publications'},yaxis={'title': 'Faculty Member'},margin={'l': 140, 'b': 50, 't': 50, 'r': 50},hovermode='closest'
                )
            }
        ),
        html.Div(id='publication-output')
        ]),
    ], style={'width': '35', 'float': 'left'}),


  #Top Faculty Members with given keywords
     html.Div([
        html.H4('Top Faculty Members Associated with a Keyword[Neo4j db]'),
        html.Div([dcc.Input(id="keyword-input2", type="text" ,value="data mining",style={'width': '60%'}),
        html.Button("Find",id="submit-button",n_clicks=0 ,style={'background-color': '#3f7fbf', 'color': 'white', 'border-radius': '10px'})
        ],style={'display': 'flex', 'justify-content': 'middle'}),
        html.Div(id="output-pie",style={ 'margin-top': '10px', 'border-radius': '2px', 'border': '1px solid #ccc'})

    ], style={'width': '50', 'float': 'right'}),

    ], style={'font-family': 'Arial, sans-serif', 'max-width': '1100px', 'margin': '0 auto'})


# Define the callback function for adding a keyword
@app.callback(
    Output('keyword-table', 'data'),
    [Input('add-button', 'n_clicks')],
    [State('new-keyword-id', 'value'), State('new-keyword-name', 'value')],
    prevent_initial_call=True,  allow_duplicate=True
)
def add_keyword(n_clicks, id_val, name_val):
    db = connect_to_database()
    if not name_val:
        return []
    if not id_val:
        return []
    with db.cursor(prepared=True) as cursor:
        sql = "SELECT * FROM keyword WHERE id = %s"
        cursor.execute(sql, (id_val,))
        result = cursor.fetchone()
        if result:
            return []
        sql = "INSERT INTO keyword (id, name) VALUES (%s, %s)"
        values = (id_val, name_val)
        cursor.execute(sql, values)
        db.commit()
    db.close()
    return get_last_three_keywords()


def update_keyword_table(n_clicks):
    result = get_last_three_keywords()
    df = pd.DataFrame(result[0], columns=["ID", "Keyword"])
    return df.to_dict('records')


# Define the callback function for deleting a keyword
@app.callback(
    Output('delete-output', 'children'),
    [Input('delete-button', 'n_clicks')],
    [State('delete-keyword-id', 'value')]
)
def delete_keyword(n_clicks, id_val):
    if not id_val:
        return html.Div('Please enter an ID')
    with db.cursor(prepared=True) as cursor:
        # check if the keyword exists in the database
        sql = "SELECT * FROM keyword WHERE id = %s"
        cursor.execute(sql, (id_val,))
        result = cursor.fetchone()
        if not result:
            return html.Div('Keyword does not exist')
        sql = "DELETE FROM keyword WHERE id = %s"
        cursor.execute(sql, (id_val,))
        db.commit()
    return html.Div('Keyword deleted successfully')


# Define the callback function for top 5 positons
@app.callback(
    [Output('position-count-table', 'children'),
     Output('pie-chart-container', 'children')],
    [Input('position-count-button', 'n_clicks')],
    [State('university-name-input', 'value')]
)
def show_position_count(n_clicks, university_name):
    if not university_name:
        return html.Div('Please enter a university name'), {}
    #Use the faculty_position_count view to retrieve data
    query = """
        SELECT position, count
        FROM faculty_position_count
        WHERE university_name = %s
        ORDER BY count DESC
        LIMIT 5;
    """
    result = execute_query(query, (university_name,))
    
      
    if not result:
        return [], html.Div('No data found for the given university name')
    # create table data
    table_data = [{'Position': row[0], 'Count': row[1]} for row in result]
    
    # create table
    table = dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in ['Position', 'Count']],
        data=table_data,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'
            }
    )

    # create pie chart data
    labels = [row[0] for row in result]
    values = [row[1] for row in result]
    pie_data = {
        'labels': labels,
        'values': values,
        'type': 'pie'
    }

    # create pie chart
    pie_chart = dcc.Graph(
        id='pie-chart',
        figure={
            'data': [pie_data],
            'layout': {
                'title': 'Positions at {}'.format(university_name)
            }
        }
    )
    return table, pie_chart

# define the callback function for find keyword button click
@app.callback(
    Output('search-results', 'children'),
    Output('citations-graph', 'figure'),
    Input('search-button', 'n_clicks'),
    State('keyword-input', 'value')
)

def search(n_clicks, keyword):
    if n_clicks > 0:
        query = """
            SELECT p.title, p.year, p.num_citations 
            FROM publication p 
            JOIN publication_keyword pk ON p.id = pk.publication_id 
            JOIN keyword k ON pk.keyword_id = k.id 
            WHERE k.name = '{}' 
            ORDER BY p.num_citations DESC 
            LIMIT 5;
        """.format(keyword)
        results = execute_query(query)
        if results:
            # create a pandas dataframe from the search results
            df = pd.DataFrame(results, columns=['Title', 'Year', 'Citations'])
            # filter out the empty years
            df = df[df['Year'] != '']
            # get the top 5 years in the dataframe
            years = df['Year'].value_counts().head(5).index
            #get the top 5 years in the dataframe that have at least one publication with non-zero citations
            years = df[df['Citations'] > 0]['Year'].value_counts().head(5).index

            # create the bar graph figure
            data = []
            for year in years:
                year_df = df[df['Year'] == year]
                citations = year_df['Citations'].values[0]
                data.append(go.Bar(x=[year], y=[citations], name=year))
            fig = {
                'data': data,
                'layout': go.Layout(
                    title='Top Publications',
                    xaxis_title='Year',
                    yaxis_title='Number of Citations',
                    barmode='group',
                    xaxis=dict(tickvals=years, ticktext=years, dtick=1),
                    margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
                    height=400
                )
            }

            # create the search results table
            table = dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            style_data_conditional=[    {  'if': {'row_index': 'odd'},   'backgroundColor': 'rgb(248, 248, 248)'   }  ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'
            }
        )

            return table, fig
        else:
            return html.Div('No results found.')
    else:
        return dash.no_update, {}

#Monogo DB call back 
@app.callback(
    [dash.dependencies.Output('publication-bar-graph', 'figure'),
     dash.dependencies.Output('publication-output', 'children')],
    [dash.dependencies.Input('publication-bar-graph', 'figure')])
def update_publication_bar_graph(figure):
    query = [
        {
            '$project': {
                'name': 1,
                'num_publications': {'$size': '$publications'}
            }
        },
        {
            '$sort': {'num_publications': -1}
        },
        {
            '$limit': 10
        }
    ]

    try:
        num_publications = []
        names = []

        results = mongo_execute_query(query)

        for result in results:
            names.append(result['name'])
            num_publications.append(result['num_publications'])

        figure['data'][0]['x'] = num_publications
        figure['data'][0]['y'] = names

        return figure, ''

    except ServerSelectionTimeoutError:
        return figure, 'Could not connect to MongoDB server'

 
#Neo4J DB connect
neo4j_conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", password="your pass")

# Define the callback to update the pie chart
@app.callback(
    Output("output-pie", "children"),
    Input("submit-button", "n_clicks"),
    Input("keyword-input2", "value")
)
def find_faculty_members(n_clicks, neokeyword):
    if n_clicks > 0:
        query = f"MATCH (k:KEYWORD {{name: '{neokeyword}'}})<-[:LABEL_BY]-(p:PUBLICATION)<-[:PUBLISH]-(f:FACULTY) WITH f, count(DISTINCT p) AS num_pubs RETURN f.name, num_pubs ORDER BY num_pubs DESC LIMIT 5"
        result = neo4j_conn.query(query,db='academicworld')
        if not result:
            return "No results found"
        else:
            data = {"names": [], "values": []}
            for row in result:
                data["names"].append(row["f.name"])
                data["values"].append(row["num_pubs"])
            fig = px.pie(data_frame=data, names="names", values="values", title=f"Top Members Associated with '{neokeyword}'")
            return dcc.Graph(figure=fig)
    else:
        return ""

#Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
