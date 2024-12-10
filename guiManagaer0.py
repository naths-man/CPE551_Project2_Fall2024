import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

class GUIManager:
    """
    Class to manage the graphical user interface using Dash.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the GUIManager with the provided data.

        Args:
            data (pd.DataFrame): The cleaned data to be visualized.
        """
        self.data = data
        self.app = dash.Dash(__name__)

    def setup_layout(self):
        """
        Defines the layout of the Dash app, including interactive components.
        """
        self.app.layout = html.Div([
            html.H1("Carrier Data Analysis", style={"textAlign": "center"}),

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

            # Graph to display trends
            dcc.Graph(id="trend-graph"),

            # Range slider for selecting months
            html.Label("Select Month Range:"),
            dcc.RangeSlider(
                id="month-slider",
                min=0,
                max=11,
                marks={i: month for i, month in enumerate(self.data['Month'])},
                value=[0, 11]
            ),

            # Button to reset filters
            html.Button("Reset Filters", id="reset-button", n_clicks=0)
        ])

    def setup_callbacks(self):
        """
        Defines the callbacks for interactive elements in the GUI.
        """
        @self.app.callback(
            Output("trend-graph", "figure"),
            [Input("data-type-dropdown", "value"),
             Input("month-slider", "value")]
        )
        def update_graph(selected_data_type, month_range):
            """
            Updates the graph based on user selection.

            Args:
                selected_data_type (str): The selected data type (DOMESTIC, INTERNATIONAL, TOTAL).
                month_range (list): The selected range of months.

            Returns:
                dict: The updated figure object for the graph.
            """
            # Filter data based on month range
            filtered_data = self.data.iloc[month_range[0]:month_range[1] + 1]
            fig = {
                "data": [
                    {
                        "x": filtered_data["Month"],
                        "y": filtered_data[selected_data_type],
                        "type": "line",
                        "name": selected_data_type
                    }
                ],
                "layout": {
                    "title": f"{selected_data_type} Trends",
                    "xaxis": {"title": "Month"},
                    "yaxis": {"title": "Count"}
                }
            }
            return fig

        @self.app.callback(
            [Output("data-type-dropdown", "value"),
             Output("month-slider", "value")],
            [Input("reset-button", "n_clicks")]
        )
        def reset_filters(n_clicks):
            """
            Resets all filters to default values.

            Args:
                n_clicks (int): Number of times the reset button has been clicked.

            Returns:
                tuple: Default values for the dropdown and slider.
            """
            return "TOTAL", [0, 11]

    def run(self):
        """
        Runs the Dash app.
        """
        self.setup_layout()
        self.setup_callbacks()
        self.app.run_server(debug=False)


# Example usage:
if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "DOMESTIC": range(12, 24),
        "INTERNATIONAL": range(24, 36),
        "TOTAL": range(36, 48)
    })

    gui = GUIManager(sample_data)
    gui.run()