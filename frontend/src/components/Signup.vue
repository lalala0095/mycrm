<template>
  <div class="signup-page">
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignup">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Sign Up</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    async handleSignup() {
      // API call to FastAPI signup endpoint
      try {
        const response = await fetch("http://127.0.0.1:8000/api/users/signup", {  // Full URL to backend
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });
        if (!response.ok) throw new Error("Signup failed");
        alert("Signup successful!");
      } catch (error) {
        alert(error.message);
      }
    }
  }
};
</script>
