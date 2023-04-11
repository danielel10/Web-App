<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Molecules</h1>
          <hr><br><br>
          <button type="button" class="btn btn-success btn-sm" @click="openFilePicker">
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
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        molecules: [],
        addMoleculeForm: {
          fName: '',
          Mass: '',
          plot: [],
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
      addMolecule(payload) {
        const path = 'http://localhost:5000/Molecules';
        axios.post(path, payload)
          .then(() => {
            this.getmolecules();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getmolecules();
          });
      },
      initForm() {
        this.addMoleculeForm.fName = '';
        this.addMoleculeForm.Mass = '';
        this.addMoleculeForm.plot = [];
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addMoleculeModal.hide();
        let plot = false;
        if (this.addMoleculeForm.plot[0]) plot = true;
        const payload = {
          fName: this.addMoleculeForm.fName,
          Mass: this.addMoleculeForm.Mass,
          plot, // property shorthand
        };
        this.addMolecule(payload);
        this.initForm();
      },
      onReset(evt) {
        evt.preventDefault();
        this.$refs.addMoleculeModal.hide();
        this.initForm();
      },
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
      openFilePicker() {
        this.$refs.fileInput.click();
      },
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