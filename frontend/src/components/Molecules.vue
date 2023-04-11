<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Molecules</h1>
          <hr><br><br>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.import-modal>
              Import Molecule file
          </button>
            <input type="file" ref="fileInput" style="display: none" @change="onFileChange">

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Comment</th>
                <th scope="col">Burried Volume</th>
                <th scope="col">Plot?</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
                 <tr v-for="(molecule, index) in molecules" :key="index">
                <td>{{ molecule.fName }}</td>
                <td>{{ molecule.Mass }}</td>
                <td>
                  <span v-if="molecule.Plot">Yes</span>
                  <span v-else>No</span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-danger btn-sm" @click="deleteMol(molecule)">Delete</button>                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <b-modal ref="importMoleculeModal" id="import-modal" title="Import Molecules" hide-footer no-wrap>
        <b-form @submit="onSubmit" @reset="onReset">
          <b-form-group id="form-file-group" label="File:" label-for="form-file-input">
            <b-form-file id="form-file-input" v-model="importMoleculeForm.file" required></b-form-file>
          </b-form-group>
          <b-form-group id="form-ignore-group" label="Ignored Molecules:" label-for="form-ignore-input">
            <b-form-textarea id="form-ignore-input" v-model="importMoleculeForm.ignore" placeholder="Enter molecules to ignore"></b-form-textarea>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        molecules: [],
        importMoleculeForm: {
        file: null,
        ignore: ''
        },
      };
    },
    methods: {
      getmolecules() {
        const path = 'http://localhost:5000/Molecules';
        axios.get(path)
          .then((res) => {
            this.molecules = res.data.molecules;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      initForm() {
        this.importMoleculeForm.file = null;
        this.importMoleculeForm.ignore = '';
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.$refs.importMoleculeModal.hide();
        const file = this.importMoleculeForm.file;
        const formData = new FormData();
        const numToIgnoreList = this.importMoleculeForm.ignore.split(',').map(Number);
        formData.append('numToIgnoreList', JSON.stringify(numToIgnoreList));
        formData.append('file', file)
          // Send the molecule to the backend
          axios.post('http://localhost:5000/Molecules', formData , {headers: {
          'Content-Type': 'multipart/form-data'
        }})
            .then(response => {
              this.getmolecules();
            })
            .catch(error => {
              this.getmolecules();
            });
        this.initForm();
      },
      onReset(evt) {
        evt.preventDefault();
        this.initForm();
      },

      //action of deleting the molecule
      removeMol(molId) {
        const path = `http://localhost:5000/${molId}`;
        axios.delete(path)
            .then(() => {
            this.getmolecules();
            })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getmolecules();
        });
      },

    // Handle Delete Button
      deleteMol(mol) {
        this.removeMol(mol.id);
      },

      //Handle the file choosing
      onFileChange(event) {
        const file = event.target.files[0];
        const formData = new FormData()
        const numToIgnore = prompt("Enter a comma-separated list of molecules to ignore:", "");
        const numToIgnoreList = numToIgnore.split(',').map(Number);
        formData.append('numToIgnoreList', JSON.stringify(numToIgnoreList));
        formData.append('file', file)
          // Send the molecule to the backend
          axios.post('http://localhost:5000/Molecules', formData , {headers: {
          'Content-Type': 'multipart/form-data'
        }})
            .then(response => {
              this.getmolecules();
            })
            .catch(error => {
              this.getmolecules();
            }); 
        this.$refs.fileInput.value = null;
      }

    },
    created() {
      this.getmolecules();
    },
  };
  </script>