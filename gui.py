'''
ITMD513-02 Final_project
Tinghan Li A20475947
7/23/2023
Description:
This crime analysis application allows users to explore and visualize crime data
in Chicago through intuitive charts. Users can select different data visualization 
techniques, including trend over time, crime distribution by day and time, top crime locations,
and crime comparison by type. The application provides insights into crime patterns
and assists law enforcement in making informed decisions to enhance public safety.
'''
import tkinter as tk
from tkinter import ttk
import pandas as pd
import plots

class CrimeAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crime Analysis Dashboard")
        self.geometry("800x600")

        # Create a variable to store the selected graph option
        self.selected_graph = tk.StringVar()

        # Create variables to store the selected options for filtering data
        self.crime_types_var = []
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        # Load data from data.py (assuming data.py is in the same directory)
        from data import df

        # Store the DataFrame in the class for later use
        self.df = df

        # Create the login widgets
        self.label_username = ttk.Label(self, text="Username:")
        self.label_password = ttk.Label(self, text="Password:")
        self.entry_username = ttk.Entry(self)
        self.entry_password = ttk.Entry(self, show="*")
        self.button_login = ttk.Button(self, text="Login", command=self.login)

        # Place login widgets
        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)

        # Create a Text widget to display detailed data
        self.data_text = tk.Text(self, wrap=tk.WORD, height=10)
        self.data_text.pack(pady=10, expand=True, fill='both')
        self.data_text.pack_forget()  # Hide the widget initially

    def login(self):
        # Add your login authentication logic here
        # For simplicity, let's assume a username "admin" and password "password" for demo purposes
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "password":
            # Destroy the login widgets
            self.label_username.destroy()
            self.label_password.destroy()
            self.entry_username.destroy()
            self.entry_password.destroy()
            self.button_login.destroy()

            # Create the main application widgets
            self.create_widgets()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")

    def create_widgets(self):
        # Create options for filtering data
        crime_types = self.df['primary_type'].unique()
        ttk.Label(self, text="Select Crime Types:").pack(pady=5)
        for crime_type in crime_types:
            var = tk.BooleanVar()
            ttk.Checkbutton(self, text=crime_type, variable=var, onvalue=True, offvalue=False).pack()
            self.crime_types_var.append((crime_type, var))

        ttk.Label(self, text="Select Start Date:").pack(pady=5)
        ttk.Entry(self, textvariable=self.start_date_var).pack()

        ttk.Label(self, text="Select End Date:").pack(pady=5)
        ttk.Entry(self, textvariable=self.end_date_var).pack()

        # Create a label for the dropdown
        graph_label = ttk.Label(self, text="Select a graph to display:")
        graph_label.pack(pady=10)

        # Create the dropdown to select the graph
        graph_choices = ['Crime Trend Over Time', 'Crime Distribution by Day of the Week', 'Crime Distribution by Time of Day',
                         'Top Locations for Different Crime Types', 'Crime Comparison by Primary Type']
        graph_dropdown = ttk.Combobox(self, textvariable=self.selected_graph, values=graph_choices)
        graph_dropdown.pack()

        # Create a button to plot the selected graph
        plot_button = ttk.Button(self, text='Plot Graph', command=self.plot_selected_graph)
        plot_button.pack(pady=10)

    def plot_selected_graph(self):
        selected_graph = self.selected_graph.get()

        # Filter the data based on user selections
        selected_crime_types = [crime_type for crime_type, var in self.crime_types_var if var.get()]
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()

        filtered_df = self.df.copy()
        if selected_crime_types:
            filtered_df = filtered_df[filtered_df['primary_type'].isin(selected_crime_types)]

        if start_date and end_date:
            try:
                filtered_df['date'] = pd.to_datetime(filtered_df['date'])
                filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]
            except pd.errors.ParserError:
                tk.messagebox.showerror("Invalid Date Format", "Please enter dates in YYYY-MM-DD format")

        if selected_graph == 'Crime Trend Over Time':
            plots.plot_crime_trend(filtered_df)

        elif selected_graph == 'Crime Distribution by Day of the Week':
            plots.plot_crime_by_day(filtered_df)

        elif selected_graph == 'Crime Distribution by Time of Day':
            plots.plot_crime_by_time(filtered_df)

        elif selected_graph == 'Top Locations for Different Crime Types':
            plots.plot_top_locations(filtered_df)

        elif selected_graph == 'Crime Comparison by Primary Type':
            plots.plot_crime_comparison(filtered_df)

        # Show the detailed data in the Text widget
        self.show_data(filtered_df)

    def show_data(self, df):
        # Convert DataFrame to string and display in the Text widget
        self.data_text.delete(1.0, tk.END)
        data_str = df.head().to_string(index=False)  # Display only the first few rows
        self.data_text.insert(tk.END, data_str)
        self.data_text.pack(pady=10, expand=True, fill='both')


if __name__ == "__main__":
    app = CrimeAnalysisApp()
    app.mainloop()
