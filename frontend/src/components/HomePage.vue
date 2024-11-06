<!-- frontend/src/components/HomePage.vue -->

<template>
    <div class="home-page">
      <h1>Welcome to the App</h1>
      <button @click="goToLogin">Login</button>
      <button @click="goToSignup">Sign Up</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      goToLogin() {
        this.$router.push("/login");
      },
      goToSignup() {
        this.$router.push("/signup");
      }
    }
  };
  </script>
  
  <style scoped>
  /* Style your page as desired */
  </style>
  