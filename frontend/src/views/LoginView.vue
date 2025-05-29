<template>
  <v-container class="my-12 d-flex align-center justify-center">
    <v-card width="400" elevation="8">
      <v-card-title class="text-h5 font-weight-bold justify-center">Login</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login" ref="formRef">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            :rules="[requiredRule, emailRule]"
            required
            prepend-inner-icon="mdi-email"
          />
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            :rules="[requiredRule]"
            required
            prepend-inner-icon="mdi-lock"
          />
          <v-btn type="submit" color="primary" block class="mt-4">Login</v-btn>
        </v-form>
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          class="mt-4"
          density="comfortable"
        >
          {{ error }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const formRef = ref()
const router = useRouter()
const auth = useAuthStore()

// Validation rules
const requiredRule = (v: string) => !!v || 'Field is required'
const emailRule = (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid'

const login = async () => {
  const result = await formRef.value?.validate()
  if (!result?.valid) return

  error.value = ''
  try {
    const res = await fetch('https://spotitried.onrender.com/user/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || data)

    auth.login(data)
    router.push('/')
  } catch (err: any) {
    error.value = err.message
  }
}
</script>
