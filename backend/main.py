from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, jsonify, request
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
        molecules.append({
            'id' : uuid.uuid4().hex,
            'fName': post_data.get('fName'),
            'Mass': post_data.get('Mass'),
            'Plot': post_data.get('plot')
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


if __name__ == '__main__':
    app.run()