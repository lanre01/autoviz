""" import nltk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import math
from datetime import datetime
import matplotlib.image as mpimg
import seaborn as sns
import os
nltk.download('punkt')
nltk.download('stopwords')


def openFile():
    filePath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filePath:
        try:
            pd.read_csv(filePath)
            print(f"File selected: {filePath}")
            dialog.withdraw()  # Hides the dialog
            selectColumns(filePath)
        except Exception as e:
            messagebox.showerror(" ", "Failed to open the file. Please make sure it's a valid CSV file.")
            print(f"Error opening file: {e}")
    else:
        messagebox.showwarning("Warning", "No file selected. Please select a CSV file.")


def createDialog():
    global dialog
    dialog = tk.Tk()
    dialog.title("Open CSV File")
    dialogWidth, dialogHeight = 300, 100
    screenWidth = dialog.winfo_screenwidth()
    screenHeight = dialog.winfo_screenheight()

    centerX = int(screenWidth / 2 - dialogWidth / 2)
    centerY = int(screenHeight / 2 - dialogHeight / 2)
    dialog.geometry(f'{dialogWidth}x{dialogHeight}+{centerX}+{centerY}')

    browseButton = ttk.Button(dialog, text="Browse", command=openFile)
    browseButton.pack(expand=True)

    dialog.protocol("WM_DELETE_WINDOW", onClosing)  # Handle the window close event

    dialog.mainloop()


def createMainWindow(filePath, columnsToInclude):
    try:
        global mainWindow
        if 'mainWindow' in globals():
            mainWindow.destroy()  # Ensure previous instance is destroyed
        mainWindow = tk.Toplevel()  # Use Toplevel for secondary windows
        mainWindow.title("CSV Data Visualization")
        mainWindow.geometry("1280x720")

        label = tk.Label(mainWindow, text=f"CSV file: {filePath}\nVisualizing columns: {', '.join(columnsToInclude)}")
        label.pack(pady=10)

        # Generate scatter plot image
        scatter_output_file = "scatterplot.png"
        scatterPlotVis(filePath, columnsToInclude, scatter_output_file)

        # Load other visualization images
        wordcloud_fig = WordCloudVis(filePath, columnsToInclude)
        histogram_fig = histograms(filePath, columnsToInclude)
        treemap_fig = TreeMapDataVis(filePath, columnsToInclude)
        pcp_fig = PCPVis(filePath, columnsToInclude)

        # Setup canvas for matplotlib figures
        fig = plt.figure(figsize=(15, 10))  # Adjust overall figsize for better fit and aspect ratio

        # Grid specification
        grid = plt.GridSpec(2, 2, height_ratios=[3, 2])  # Adjust height ratios to give more space to plots

        # Display histogram
        ax1 = fig.add_subplot(grid[0, 0])
        ax1.imshow(mpimg.imread("histogram.png"))
        ax1.axis('off')
        ax1.set_title('Histogram')

        # Display wordcloud across the bottom
        ax2 = fig.add_subplot(grid[0, 1])
        ax2.imshow(mpimg.imread("wordcloud.png"))
        ax2.axis('off')
        ax2.set_title('Wordcloud')

        # Display scatter plot
        ax3 = fig.add_subplot(grid[1, :])  # Spanning entire bottom row
        ax3.imshow(mpimg.imread(scatter_output_file))
        ax3.axis('off')
        ax3.set_title('Scatter Plot')

        treemap_fig.show()
        pcp_fig.show()

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=mainWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        mainWindow.protocol("WM_DELETE_WINDOW", lambda: mainWindow.destroy())
    except Exception as e:
        messagebox.showerror("Error", "There was a problem setting up the main window.")
        print(f"Error creating main window: {e}")


def TreeMapDataVis(filePath, columnsToInclude):
    print("called ", filePath)

    filename = filePath

    df = pd.read_csv(filename)

    df = df[columnsToInclude]

    columns = df.select_dtypes(include=['float64']).columns
    dfBrokenDownlist = []

    # Floats (treated as discrete data)

    for colname in columns:
        bins = pd.cut(df[colname], bins=10)
        dfBrokenDown = df.groupby(bins).size().reset_index(name='Frequency')
        dfBrokenDown['Column'] = colname
        dfBrokenDown['Bin'] = bins

        dfBrokenDownlist.append(dfBrokenDown)

    columns2 = df.select_dtypes(include=['object']).columns

    # Objects (treated as concrete data)

    for colname in columns2:

        counts = df[colname].value_counts().reset_index()
        counts.columns = ['Bin', 'Frequency']
        counts['Column'] = colname
        text_data = []

        for bin_value in counts['Bin']:
            text = ', '.join(df[df[colname] == bin_value][colname].astype(str).values)
            text_data.append(text)
        counts['Text'] = text_data

        dfBrokenDownlist.append(counts)

    columns3 = df.select_dtypes(include=['int64']).columns

    # Ints (treated as concrete data)

    for colname in columns3:
        dfBrokenDown = df[colname].value_counts().reset_index()
        dfBrokenDown.columns = ['Bin', 'Frequency']
        dfBrokenDown['Column'] = colname
        dfBrokenDown['Bin'] = dfBrokenDown['Bin'].astype(str)

        dfBrokenDownlist.append(dfBrokenDown)

    df = pd.concat(dfBrokenDownlist)


    fig = px.treemap(df, path=['Column', 'Bin'], values='Frequency', color='Frequency',
                     color_continuous_scale='rainbow')

    return fig

def histograms(filePath, columnsToInclude):
    file_path = filePath

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist. Please check the path and try again.")
        exit()

    try:
        data = pd.read_csv(file_path)
        data = data[columnsToInclude]
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        exit()

    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()

    try:
        plt.figure(figsize=(12, 8))
        data[numeric_columns].hist(bins=15, color='blue', edgecolor='black', alpha=0.7, grid=False)
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15, hspace=1, wspace=1)
        plt.xticks(rotation=45)
        plt.savefig("histogram.png")
        return plt
    except Exception as e:
        print(f"An error occurred while plotting the histogram: {e}")


def PCPVis(filePath, columnsToInclude):
    print("called ", filePath)

    filename = filePath

    df = pd.read_csv(filename)

    df = df[columnsToInclude]
    # fills any empty columns in rows
    for col in df.columns:
        if df[col].isna().any():
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('Missing')
            elif df[col].dtype == 'int64':
                df[col] = df[col].fillna(0)
            elif df[col].dtype == 'float64':
                df[col] = df[col].fillna(0.0)
            else:
                df[col] = df[col].fillna(method='ffill').fillna(method='bfill')

    #If integer replaces value with 0
    #If object data type just writes missing

    columns = df.columns

    if len(columns) >= 2:
        for col in columns:
            if df[col].dtype == 'object':
                df[col].astype('category')
                df[col] = pd.Categorical(df[col], categories=sorted(df[col].unique()))
                df[col] = df[col].cat.codes
                #If column is of type object, converts it to a column of type category
                #It then groups them together into different categories

        df_updated = (df[columns])

        #If the CSV file doesn't have an ID column and has no name, gives it the name ID
        if df_updated.columns[0] == 'Unnamed: 0':
            df_updated = df_updated.rename(columns={df.columns[0]: 'ID'})

        #Colour column used is equal to the ID column as each line represented by their ID which is represented by a certain colour
        color_column = df_updated.columns[0]

        #Plots the parallel coordinates plot using the updated dataframe
        #Uses the color_column to indicate colour of each line is based on ID of row
        #Sets the title to the filename and uses the colour scale of t=rainbow
        fig = px.parallel_coordinates(df_updated, color=color_column, dimensions=df_updated,
                                      color_continuous_scale='rainbow',
                                      title=filename)

        fig.update_layout(width=120 * df_updated.shape[1],
                          height=700)

        #Updates the layout to give the height of the parallel coordinates plot and the width of the parallel coordinates plot


    else:
        print("Error: There are not enough columns in the data frame")

    return fig


def WordCloudVis(filePath, columnsToInclude):

    stop_words = set(stopwords.words('english'))
    csv_file_path = filePath
    df = pd.read_csv(csv_file_path)
    df = df[columnsToInclude]
    string_columns_df = df.select_dtypes(exclude=['float64'], include=['object'])
    datetime_columns = [col for col in string_columns_df.columns if pd.api.types.is_datetime64_any_dtype(string_columns_df[col])]
    string_columns_df = string_columns_df.drop(columns=datetime_columns)

    # Remove other type of dates
    def contains_dates(column):
        for value in column:
            try:
                if pd.notnull(value):
                    datetime.strptime(value, date_format)
                    return True
            except ValueError:
                continue
        return False


    date_format = "%d-%b-%Y"
    columns_to_exclude = [col for col in string_columns_df.columns if contains_dates(string_columns_df[col])]
    string_columns_df = string_columns_df.drop(columns=columns_to_exclude)


    # check if a value is float
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    #clean the data and generate token for wordcloud
    def cleanandgeneratetoken(column):
        text_data = ' '.join(df[column].dropna().astype(str).values)
        text_data = text_data.replace('-', '_').lower()
        text_data = text_data.replace('.', ' ').lower()
        tokens = nltk.word_tokenize(text_data)
        tokens = [word for word in tokens if len(word) > 0 and not word.isnumeric() and not is_float(word)]
        tokens = [word.lower() for word in tokens]
        tokens = [word for word in tokens if word not in stop_words]
        return tokens

    # function to generate a wordcloud for each column
    def generate_wordcloud(tokens):
        # Generate bigrams
        bigram_tokens = list(nltk.bigrams(tokens))
        bigram_text = ' '.join([' '.join(pair) for pair in bigram_tokens])

        # Generate word cloud
        wordcloud = WordCloud(stopwords=stop_words, background_color='white', width=800, height=400).generate(bigram_text)
        return wordcloud

    # No data available plot
    def plot_no_data_available():
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No data available for word cloud.', ha='center', va='center',
                fontsize=12)
        ax.axis('off')
        plt.savefig("wordcloud.png")
        return plt

    # Constants for plot setup
    DIVISOR = 4  # Change this to adjust the number of rows based on your preference (2, 4, etc.)
    num_columns = len(string_columns_df.columns)
    num_plots = len(string_columns_df.columns)

    # Calculate the number of rows and columns for the subplots
    num_rows = math.ceil(num_columns / DIVISOR)
    num_subplot_columns = min(num_columns, DIVISOR)
    if num_subplot_columns <= 0 or num_rows <= 0:
        plot_no_data_available()

    else:
        fig, axs = plt.subplots(nrows=num_rows, ncols=num_subplot_columns, figsize=(40, 20))
        if num_subplot_columns == 1:
            for i, column in enumerate(string_columns_df.columns):
                tokens = cleanandgeneratetoken(column)
                if len(tokens) == 0:
                    fig.delaxes(axs)
                    plot_no_data_available()
                    break
                wordcloud = generate_wordcloud(tokens)
                axs.imshow(wordcloud, interpolation='bilinear')
                axs.set_title(column.upper(), fontsize=50)
                axs.axis('off')
        else:
            axs = axs.flatten()
            last_index_used = -1
            plot_index = 0

            for i, column in enumerate(string_columns_df.columns):

                tokens = cleanandgeneratetoken(column)
                if len(tokens) == 0 or len(set(tokens)) <= 4:
                    continue

                try:
                    wordcloud = generate_wordcloud(tokens)
                    axs[plot_index].imshow(wordcloud, interpolation='bilinear')
                    axs[plot_index].set_title(column.upper(), fontsize=20)
                    axs[plot_index].axis('off')
                    last_index_used = plot_index
                    plot_index += 1
                except ValueError:
                        continue

            #remove unused plots
            for ax in axs[last_index_used + 1:]:
                fig.delaxes(ax)
            if plot_index == 0 :
                plot_no_data_available()

        plt.tight_layout()
        plt.savefig("wordcloud.png")
        return plt


def scatterPlotVis(filePath, columnsToInclude, output_file):
    df = pd.read_csv(filePath)
    num_plots = len(columnsToInclude) // 2

    if num_plots <= 6:
        num_cols = num_plots  # Use the number of plots as the number of columns if 6 or less
    else:
        num_cols = 6  # Fix the number of columns at 6 if there are more than 6 plots

    # Now calculate the number of rows needed if there are more than 6 plots
    num_rows = (num_plots + num_cols - 1) // num_cols  # This ensures all plots fit into the grid

    # Increase the figure size to give more space to each plot
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10 * num_cols, 8 * num_rows))
    axs = axs.flatten() if num_plots > 1 else [axs]  # Handle the case of a single subplot

    for i in range(num_plots):
        x_col = columnsToInclude[2 * i]
        y_col = columnsToInclude[2 * i + 1]
        ax = axs[i]
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        ax.set_title(f'{x_col} vs {y_col}', fontsize=35)  # Increase font size for the title
        ax.set_xlabel(x_col, fontsize=20)  # Increase font size for x-axis label
        ax.set_ylabel(y_col, fontsize=20)  # Increase font size for y-axis label
        ax.tick_params(axis='x', rotation=30)  # Rotate labels
        ax.tick_params(axis='y', rotation=30)  # Rotate labels
        ax.tick_params(axis='both', labelsize=16)  # Increase font size for tick labels
        ax.grid(True)

    plt.tight_layout(pad=4)  # Adjust layout to prevent overlap
    plt.savefig(output_file)
    plt.close()


def selectColumns(filePath):
    data = pd.read_csv(filePath)
    columns = data.columns.tolist()

    def updateColumnsToVisualize():
        selectedIndices = list(map(int, columnList.curselection()))
        selectedColumns = [columns[i] for i in selectedIndices] or columns

        createMainWindow(filePath, selectedColumns)

    columnWindow = tk.Toplevel()
    columnWindow.title("Select Columns to Visualize")
    columnWindow.geometry("300x400")

    columnList = tk.Listbox(columnWindow, selectmode='multiple')
    for col in columns:
        columnList.insert(tk.END, col)
        columnList.select_set(columns.index(col))
    columnList.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(columnWindow, orient='vertical', command=columnList.yview)
    scrollbar.pack(side="left", fill='y')
    columnList.configure(yscrollcommand=scrollbar.set)

    okButton = ttk.Button(columnWindow, text="OK", command=updateColumnsToVisualize)
    okButton.pack(side="bottom", pady=10)


def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        dialog.destroy()




createDialog()
 """