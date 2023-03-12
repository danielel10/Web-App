import Vue from 'vue';
import Router from 'vue-router';
import Molecules from '../components/Molecules.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Molecules',
      component: Molecules,
    },
    
  ],
});