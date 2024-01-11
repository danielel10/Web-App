<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Buried Volume Calculator</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.import-modal>
            Import Molecule file
        </button>
          

        <br><br>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by name or buried volume"
          class="form-control"
        >
        <br>

        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Buried Volume</th>
              <th scope="col">Plot</th>
              <th scope="col">Actions</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="(molecule, index) in filteredMolecules" :key="index">
                <td>{{ molecule.fName }}</td>
                <td>{{ molecule.Mass }}</td>

                <!-- Plot button -->
                <td>
                  <div class="btn-group" role="group">
                    
                    <button type="button" class="btn btn-primary btn-sm" @click="showPlot(molecule)">Show Plot</button>
                  </div>
                </td>

                
                <td> 
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-danger btn-sm" @click="deleteMol(molecule)">Delete</button>
                  </div>
                </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Add molecule modal-->
    <b-modal ref="importMoleculeModal" id="import-modal" title="Import Molecules" 
      hide-footer>
      <b-form @submit="onSubmit" @reset="onReset">
        <b-form-group id="form-file-group" label="File:" label-for="form-file-input">
          <b-form-file id="form-file-input" v-model="importMoleculeForm.file" required></b-form-file>
        </b-form-group>
        <b-form-group id="form-ignore-group" label="Excluded atoms:" label-for="form-ignore-input">
          <b-form-textarea id="form-ignore-input" v-model="importMoleculeForm.ignore" placeholder="Enter atoms to ignore"></b-form-textarea>
        </b-form-group>
        <b-form-group id="form-zaxis-group" label="Z axis atoms:" label-for="form-zaxis-input">
          <b-form-textarea id="form-zaxis-input" v-model="importMoleculeForm.zaxis" placeholder="Enter z axis atoms for plotting"></b-form-textarea>
        </b-form-group>
        <b-form-group id="form-nonmetalic-group" label="If you dont want a metalic ligand enter a new index for the center atom:" label-for="form-nonmetalic-input">
          <b-form-textarea id="form-nonmetalic-input" v-model="importMoleculeForm.nonmetalic" placeholder="Enter new index for centering"></b-form-textarea>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    

    <!-- plot modal -->
    <b-modal ref="plotModal" id="plot-modal" title="Plot" hide-footer>
      <div class="plot-container">
        <img :src="plotImage">
      </div>
      <b-button-group>
        <b-button variant="primary" @click="savePlot">Save</b-button>
      </b-button-group>
    </b-modal>


    <!-- Error notification -->
    <b-alert v-model="showError" variant="danger" dismissible>
      {{ errorMessage }}
    </b-alert>



  </div>
</template>

<script>
import axios from 'axios';
import { BIconTextCenter } from 'bootstrap-vue';
export default {
  data() {
    return {
      showError: false,
      errorMessage: '',
      plot: null,
      plotImage: null,
      molecules: [],
      importMoleculeForm: {
      file: null,
      ignore: '',
      zaxis: '',
      nonmetalic: '',
      },
      searchQuery: '', // Search query for filtering molecules
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
      this.importMoleculeForm.zaxis = '';
      this.importMoleculeForm.nonmetalic = '';
    },

    onSubmit(evt) {
      evt.preventDefault( );
      this.$refs.importMoleculeModal.hide();
      const file = this.importMoleculeForm.file;
      const formData = new FormData();
      const numToIgnoreList = this.importMoleculeForm.ignore.split(',') == '' ? 
                            null : this.importMoleculeForm.ignore.split(',').map(Number);
      const zaxisatoms = this.importMoleculeForm.zaxis.split(',') == '' ? 
                          null : this.importMoleculeForm.zaxis.split(',').map(Number);
      const nonmetalic = this.importMoleculeForm.nonmetalic.split(',') == '' ? 
                            null : this.importMoleculeForm.nonmetalic.split(',').map(Number);
      formData.append('numToIgnoreList', JSON.stringify(numToIgnoreList));
      formData.append('zaxisatoms', JSON.stringify(zaxisatoms));
      formData.append('nonmetalic', JSON.stringify(nonmetalic));
      formData.append('file', file)
        // Send the molecule to the backend
        axios.post('http://localhost:5000/Molecules', formData , {headers: {
        'Content-Type': 'multipart/form-data'
      }})
          .then(response => {
            this.getmolecules();
          })
          .catch(error => {
            const errorMessage  = "center atom was not provided for a metal-free moluecule"
            this.errorHandler(errorMessage);
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
    
    // Get the plot data from the server
    getPlot(molId) {
      const path = `http://localhost:5000/${molId}`;
      return axios.get(path, { responseType: 'arraybuffer' })
        .then((response) => {
          return new Blob([response.data], { type: 'image/png' });
        })
        .catch((error) => {
          throw(error);
        });
    },


    //handle plot button
    showPlot(mol) {
      this.getPlot(mol.id)
        .then(blob => {
          const imageUrl = URL.createObjectURL(blob);
          this.plotImage = imageUrl; // set the image URL to a data property
          this.$nextTick(() => {
            // wait for Vue to update the DOM before showing the modal
            this.$refs.plotModal.show();
          });
        })
        .catch(error => {
          const errorMessage = "no z axis atoms provided";
          this.errorHandler(errorMessage);
            });
    },

    
    errorHandler(errorMessage) {
      this.errorMessage = errorMessage;
      this.showError = true;

      // Hide the error notification after a delay
      setTimeout(() => {
        this.showError = false;
      }, 3500); // Set the delay to 5000 milliseconds (5 seconds)
        
    },

    savePlot() {
      const link = document.createElement('a');
      link.href = this.plotImage;
      link.download = 'plot.png';
      link.target = '_blank';
      link.click();
    },

  },
  computed: {

    //Search handler function
    filteredMolecules() {
      const searchTerm = this.searchQuery.toLowerCase();
      return this.molecules.filter((molecule) => {
        return (
          molecule.fName.toLowerCase().includes(searchTerm) ||
          molecule.Mass.toString().toLowerCase().includes(searchTerm) // Convert to string before comparison
        );
      });
    },
  },

  created() {
    this.getmolecules();
  },
};
</script>

<style>
.modal-backdrop {
background-color: rgba(221, 221, 221, 0.5) !important;
}

.plot-container {
  position: center;
}

#plot-modal .modal-dialog {
  max-width: none;
  width: auto;
  height: auto;
  margin: auto;
  position: absolute;
  top: 50px;
  left: auto;
  right: 400px;
  bottom: auto;
  z-index: -1;
}

</style>