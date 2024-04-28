from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'])


with open("GrounWaterQUalityLabelEncoder.pkl", "rb") as file:
    encoder = pickle.load(file)

with open("GrounWaterQUalityLabelscaler.pkl", "rb") as file:
    scaler = pickle.load(file)

def prediction(data):
    with open('GrounWaterQUalityModel.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    new_data=np.array(data)
    new_data_normalised=scaler.transform(new_data.reshape(1,-1))
    predicted_class = loaded_model.predict(new_data_normalised)
    encoded_class=predicted_class
    original_class=encoder.inverse_transform(encoded_class)
    Class_Description={'C1S1':"Low salinity and low sodium waters are good for irrigation and can be used with most crops with no restriction on use on most of the soils. ",
                   'C2S1':"Medium salinity and low sodium waters are good for irrigation and can be used on all most all soils with little danger of development of harmful levels of exchangeable sodium if a moderate amount of leaching occurs. Crops can be grown without any special consideration for salinity control. ",
                   'C3S1':"The high salinity and low sodium waters require good drainage. Crops with good salt tolerance should be selected.",
                  'C3S2':"The high salinity and medium sodium waters require good drainage and can be used on coarse - textured or organic soils having good permeability. ",
                  'C3S3':"These high salinity and high sodium waters require special soil management, good drainage, high leaching and organic matter additions. Gypsum amendments make feasible the use of these waters. ",
                  'C4S1':"Very high salinity and low sodium waters are not suitable for irrigation unless the soil must be permeable and drainage must be adequate. Irrigation waters must be applied in excess to provide considerable leaching. Salt tolerant crops must be selected. ",
                  'C4S2':"Very high salinity and medium sodium waters are not suitable for irrigation on fine textured soils and low leaching conditions and can be used for irrigation on coarse textured or organic soils having good permeability. ",
                  'C4S3':"Very high salinity and high sodium waters produce harmful levels of exchangeable sodium in most soils and will require special soil management, good drainage, high leaching, and organic matter additions. The Gypsum amendment makes feasible the use of these waters. ",
                  'C4S4':"Very high salinity and very high sodium waters are generally unsuitable for irrigation purposes. These are sodium chloride types of water and can cause sodium hazards. It can be used on coarse-textured soils with very good drainage for very high salt tolerant crops. Gypsum amendments make feasible the use of these waters. "
                  }

    if original_class[0] in Class_Description:
        return (original_class[0]+" "+Class_Description[original_class[0]])

@app.route('/predict', methods=['POST'])
def predict_route():
    # Get data from the frontend
    data = request.json
    print(data)
    predictions = prediction(data)
    return jsonify({'prediction': predictions})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
