<template>
  <div class="login-page">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    
    <!-- Display success message -->
    <div v-if="successMessage" class="success">{{ successMessage }}</div>

    <!-- Display error message -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
      successMessage: ""
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/users/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded", // This is important for OAuth2PasswordRequestForm
          },
          body: new URLSearchParams({
            username: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (response.ok) {
          // Assuming the API returns an access token on successful login
          console.log("Login successful:", data); 
          this.successMessage = data.message;  // Display the success message from the API
          this.error = "";  // Clear any previous error messages
        } else {
          // Show the error message returned by the API
          this.error = data.detail || "Login failed";
          this.successMessage = "";  // Clear success message if login fails
        }
      } catch (error) {
        console.error("Error logging in:", error);
        this.error = "An error occurred during login";
        this.successMessage = "";  // Clear success message if there is an error
      }
    }
  }
};
</script>

<style scoped>
.success {
  color: green;
}

.error {
  color: red;
}
</style>
