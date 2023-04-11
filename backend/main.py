from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, jsonify, request
import numpy as np
import uuid
from morfeus import BuriedVolume, read_xyz
import tempfile
import json



# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})




molecules = [
    {   
        'id' : uuid.uuid4().hex,
        'fName': 'On the Road',
        'Mass': 'Jack Kerouac',
        'Plot': True
    },
]


@app.route('/Molecules', methods=['GET', 'POST'])
def all_molecules():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        file = request.files['file']
        excluded_atoms = json.loads(request.form['numToIgnoreList'])
        file_content = file.read()  # read the contents of the uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
            temp_file.read()
            with open(temp_file_path, 'r') as xyz_file:
                lines = xyz_file.readlines()
                molecule_name = lines[1].strip()
                
            
                # print(temp_file.read())
                elements, coordinates = read_xyz(temp_file_path)

                # Create a BuriedVolume object
                bv = BuriedVolume(elements, coordinates, 47, excluded_atoms)

                # Get the fraction of buried volume
                fraction_buried_volume = bv.fraction_buried_volume
                molecules.append({
                    'id' : uuid.uuid4().hex,
                    'fName': molecule_name,
                    'Mass': fraction_buried_volume,
                    'Plot': True
                })
                response_object['message'] = 'molecule added!'
    else:
        response_object['molecules'] = molecules
    return jsonify(response_object)

#PUT and DELETE route handler
@app.route('/<mol_id>', methods=['PUT','DELETE'])
def single_Mol(mol_id):
    response_object = {'status':'succss'}
    if request.method == 'DELETE':
        remove_mol(mol_id)
        response_object['message'] = 'molecule Removed!'
    return jsonify(response_object)

def remove_mol(mol_id):
    for mol in molecules:
        if mol['id'] == mol_id:
            molecules.remove(mol)
            return True
    return False


#calculate buried volume

def calculate_buried_volume():
    elements, coordinates = read_xyz("backend\2.xyz")
    bv = BuriedVolume(elements, coordinates, 50)
    return bv


if __name__ == '__main__':
    app.run()