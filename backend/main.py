from flask import Flask, jsonify , send_file
from flask_cors import CORS
from flask import Flask, jsonify, request
import numpy as np
import uuid
from morfeus import BuriedVolume, read_xyz
import tempfile
import json
import shutil
import os




# List of all metallic element symbols
Metallic_atoms = ['Ac', 'Al', 'Sb', 'Ag', 'Ba', 'Bi', 'Bh', 'B', 'Cd', 'Ca', 'Cf', 'Cr', 'Co', 'Cm',
                   'Ds', 'Db', 'Dy', 'Fr', 'Gd', 'Ga', 'Au', 'Hf', 'Hs', 'Ho', 'Ir', 'Fe', 'Kr', 'La',
                     'Li', 'Mc', 'Nh', 'Nb', 'N', 'Os', 'Pd', 'P', 'Pt', 'Pu', 'Po', 'K', 'Pa', 'Ra',
                       'Rn', 'Re', 'Rh', 'Rb', 'Sm', 'Sc', 'Si', 'Na', 'Sr', 'Ta', 'Tl', 'Th', 'Tm',
                         'Sn', 'Ti', 'U', 'V', 'Y', 'Zn', 'Zr']

 
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLASK_DEBUG'] = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})




molecules = [
    
]


@app.route('/Molecules', methods=['GET', 'POST'])
def all_molecules():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        file = request.files['file']
        excluded_atoms = json.loads(request.form['numToIgnoreList'])
        zaxis_atoms = json.loads(request.form['zaxisatoms'])
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
                metal_index = 0
                for i in range(len(elements)):
                    if elements[i] in Metallic_atoms:
                        metal_index = i
                    continue
                
                id = uuid.uuid4().hex

                if zaxis_atoms[0] != 0:
                    # Create a BuriedVolume object
                    bv = BuriedVolume(elements, coordinates, metal_index, excluded_atoms, z_axis_atoms= zaxis_atoms)
                    
                    plot_id = f"plot_{id}.png"
                    bv.plot_steric_map(filename = plot_id)
                    shutil.move(plot_id, "backend/plots/")
                    
                    
                else:
                    bv = BuriedVolume(elements, coordinates, metal_index, excluded_atoms)
                # Get the fraction of buried volume
                fraction_buried_volume = bv.fraction_buried_volume

                
                
                

                

                molecules.append({
                    'id' : id,
                    'fName': molecule_name,
                    'Mass': fraction_buried_volume,
                })
                response_object['message'] = 'molecule added!'
    else:
        response_object['molecules'] = molecules
    return jsonify(response_object)

#PUT and DELETE route handler
@app.route('/<mol_id>', methods=['GET','DELETE'])
def single_Mol(mol_id):
    response_object = {'status':'succss'}
    # delete the mol
    if request.method == 'DELETE':
        remove_mol(mol_id)
        response_object['message'] = 'molecule Removed!'

    # Send the file in the response
    elif request.method == "GET":
        plot_path = "backend/plots/plot_" + mol_id + ".png"
        if os.path.isfile(plot_path):
            plot_path = "plots\plot_" + mol_id + ".png"
            return send_file(plot_path, mimetype='image/png')
    return jsonify(response_object)

def remove_mol(mol_id):
    for mol in molecules:
        if mol['id'] == mol_id:
            plot_path = "backend/plots/plot_" + mol_id + ".png"
            if os.path.exists(plot_path):
                os.remove(plot_path)
            molecules.remove(mol)
            return True
    return False

if __name__ == '__main__':
    app.run()