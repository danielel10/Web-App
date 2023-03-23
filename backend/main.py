from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, jsonify, request
import numpy as np
import uuid

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
        post_data = request.get_json()
        # add the molecule
        # Get the coordinates from the dictionary
        coords = [[atom['x'], atom['y'], atom['z']] for atom in post_data['Atoms']]
        # Convert the coordinates to a numpy array
        coords_array = np.array(coords)
        burried_volume = calculate_buried_volume(coords_array)
        molecules.append({
            'id' : uuid.uuid4().hex,
            'fName': post_data.get('fname'),
            'Mass': burried_volume,
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
        print(mol_id)
        remove_mol(mol_id)
        response_object['message'] = 'molecule Removed!'
    return jsonify(response_object)

def remove_mol(mol_id):
    for mol in molecules:
        if mol['id'] == mol_id:
            molecules.remove(mol)
            return True
    return False


# buried volume calculation

def calculate_buried_volume(coords):
    # Calculate the centroid of the molecule
    centroid = np.mean(coords, axis=0)

    # Choose a bounding box that contains the molecule
    min_x = np.min(coords[:,0])
    max_x = np.max(coords[:,0])
    min_y = np.min(coords[:,1])
    max_y = np.max(coords[:,1])
    min_z = np.min(coords[:,2])
    max_z = np.max(coords[:,2])

    # Choose a set of random points inside the bounding box
    num_points = 10000
    points = np.random.uniform(low=[min_x, min_y, min_z], high=[max_x, max_y, max_z], size=(num_points, 3))

    # Calculate the number of points inside the molecule
    num_inside = 0
    for point in points:
        if is_point_inside_molecule(point, coords):
            num_inside += 1

    # Calculate the volume of the molecule
    volume = (num_inside / num_points) * ((max_x - min_x) * (max_y - min_y) * (max_z - min_z))

    return volume

def is_point_inside_molecule(point, coords):
    # Check if the point is inside the molecule using the ray casting algorithm
    # Adapted from: https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html
    num_vertices = len(coords)
    inside = False
    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        if ((coords[i,1] > point[1]) != (coords[j,1] > point[1])) and \
           (point[0] < (coords[j,0] - coords[i,0]) * (point[1] - coords[i,1]) / (coords[j,1] - coords[i,1]) + coords[i,0]):
            inside = not inside
    return inside


if __name__ == '__main__':
    app.run()