import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os


class GUIManager:
    """
    Class to manage the graphical user interface using Dash.
    """

    def __init__(self, data_dict):
        """
        Initializes the GUIManager with multiple datasets.

        Args:
            data_dict (dict): A dictionary containing airline names as keys and their data as values.
        """
        self.data_dict = data_dict
        self.app = dash.Dash(__name__)

    def setup_layout(self):
        """
        Defines the layout of the Dash app, including interactive components.
        """
        self.app.layout = html.Div([
            html.H1("Airline Traffic Analysis", style={"textAlign": "center"}),

            # Radio buttons to select airline
            html.Label("Select Airline:"),
            dcc.RadioItems(
                id="airline-radio",
                options=[
                    {"label": "All Carriers", "value": "AllCarriers.csv"},
                    {"label": "American Airlines", "value": "AmericanAirlines.csv"},
                    {"label": "Delta Airlines", "value": "DeltaAirlines.csv"},
                    {"label": "United Airlines", "value": "UnitedAirlines.csv"}
                ],
                value="AllCarriers.csv",
                style={"margin-bottom": "20px"}
            ),

            # Dropdown for selecting data type
            html.Label("Select Data Type:"),
            dcc.Dropdown(
                id="data-type-dropdown",
                options=[
                    {"label": "Domestic", "value": "DOMESTIC"},
                    {"label": "International", "value": "INTERNATIONAL"},
                    {"label": "Total", "value": "TOTAL"}
                ],
                value="TOTAL",
                style={"width": "50%"}
            ),

            # Dropdown to select chart type
            html.Label("Select Chart Type:"),
            dcc.Dropdown(
                id="chart-type-dropdown",
                options=[
                    {"label": "Line Chart", "value": "line"},
                    {"label": "Bar Chart", "value": "bar"}
                ],
                value="line",
                style={"width": "50%", "margin-bottom": "20px"}
            ),

            # Dropdown to select years
            html.Label("Select Year(s):"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(year), "value": year} for year in range(2018, 2024)] + [{"label": "All Years", "value": "all"}],
                value="all",
                multi=True,
                style={"width": "50%"}
            ),

            # Main graph area
            dcc.Graph(id="main-graph"),

            # Text area for additional insights
            html.Div([
                html.H3(id="highest-traffic-title", style={"margin-top": "20px"}),  # Dynamic title for highest traffic
                html.Div(id="highest-traffic-text", style={"font-size": "18px"}),

                html.H3(id="least-traffic-title", style={"margin-top": "20px"}),  # Dynamic title for least traffic
                html.Div(id="least-traffic-text", style={"font-size": "18px"})
            ])
        ])

    def setup_callbacks(self):
        """
        Defines the callbacks for interactive elements in the GUI.
        """
        @self.app.callback(
            [Output("main-graph", "figure"),
             Output("highest-traffic-title", "children"),
             Output("highest-traffic-text", "children"),
             Output("least-traffic-title", "children"),
             Output("least-traffic-text", "children")],
            [Input("airline-radio", "value"),
             Input("data-type-dropdown", "value"),
             Input("chart-type-dropdown", "value"),
             Input("year-dropdown", "value")]
        )
        def update_graphs(selected_airline, selected_data_type, chart_type, selected_years):
            """
            Updates the graph and provides textual insights based on user selection.

            Args:
                selected_airline (str): Selected airline file name.
                selected_data_type (str): Selected data type (DOMESTIC, INTERNATIONAL, TOTAL).
                chart_type (str): Selected chart type (line or bar).
                selected_years (list or str): Selected year(s) or "all".

            Returns:
                tuple: Updated figure and textual insights.
            """
            df = self.data_dict[selected_airline]
            airline_name = selected_airline.replace(".csv", "")

            # Filter data for the required years
            if selected_years != "all":
                df = df[df['YEAR'].isin(selected_years)]

            # Insights: Determine months with highest and least traffic for each year
            highest_traffic = []
            least_traffic = []
            grouped = df.groupby('YEAR')

            for year, group in grouped:
                max_month = group.loc[group[selected_data_type].idxmax()]
                min_month = group.loc[group[selected_data_type].idxmin()]

                highest_traffic.append(f"Year {year}: {max_month['MONTH']} ({max_month[selected_data_type]:,})")
                least_traffic.append(f"Year {year}: {min_month['MONTH']} ({min_month[selected_data_type]:,})")

            # Generate graph based on selected chart type
            if chart_type == "line":
                fig = go.Figure()

                for year, group in grouped:
                    fig.add_trace(go.Scatter(
                        x=group["MONTH"],
                        y=group[selected_data_type],
                        mode="lines+markers",
                        name=f"Year {year}",
                        line=dict(dash="solid")
                    ))

                fig.update_layout(
                    title=f"{selected_data_type} Trends ({airline_name})",
                    xaxis_title="Month",
                    yaxis_title="Traffic Count",
                    yaxis=dict(tickformat=","),
                    legend_title="Year",
                    hovermode="x unified"
                )
            elif chart_type == "bar":
                df_i = df.copy(True) #Create a deep copy of the DataFrames to avoid modifying the original.
                df_i["YEAR"] = df_i["YEAR"].astype(str)
                fig = px.bar(
                    df_i, x="MONTH", y=selected_data_type, color="YEAR",
                    title=f"{selected_data_type} Trends ({airline_name})",
                    barmode="stack"
                )
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Traffic Count",
                    yaxis=dict(tickformat=","),
                    legend_title="Year"
                )

            # Dynamic titles
            highest_traffic_title = f"Months with Highest {selected_data_type} Traffic for {airline_name}:"
            least_traffic_title = f"Months with Least {selected_data_type} Traffic for {airline_name}:"

            return (
                fig,
                highest_traffic_title,
                html.Ul([html.Li(text) for text in highest_traffic]),
                least_traffic_title,
                html.Ul([html.Li(text) for text in least_traffic])
            )

    def run(self):
        """
        Runs the Dash app.
        """
        self.setup_layout()
        self.setup_callbacks()
        self.app.run_server(debug=False)


# Example usage
if __name__ == "__main__":
    # Load datasets
    folder_path = "."  # The directory containing airline files
    data_files = ["AllCarriers.csv", "AmericanAirlines.csv", "DeltaAirlines.csv", "UnitedAirlines.csv"]

    data_dict = {}
    for file in data_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df["MONTH"] = pd.Categorical(df["MONTH"], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], ordered=True)
        data_dict[file] = df

    # Initialize and run the GUI
    gui_manager = GUIManager(data_dict)
    gui_manager.run()
