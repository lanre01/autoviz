from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from autoviz import TreeMapDataVis, histograms, PCPVis, WordCloudVis, scatterPlotVis


# Initializing flask app
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Route for seeing a data
@app.route('/compute', methods=['POST'])
def compute():
    #csv_file = request.files['file.csv']
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        try:
            wordcloud = WordCloudVis(file, None)
            treemap = TreeMapDataVis(file, None)

            return {
                "wordcloud": wordcloud,
                "treemap": treemap
            }
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Running app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
