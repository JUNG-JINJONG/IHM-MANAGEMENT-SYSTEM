import { defineStore } from 'pinia'
import apiClient from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    userType: (state) => state.user?.user_type || null,
    isOperator: (state) => state.user?.user_type === 'operator',
    isSupplier: (state) => state.user?.user_type === 'supplier',
    isCustomer: (state) => state.user?.user_type === 'customer',
  },

  actions: {
    async login(username, password) {
      try {
        const response = await apiClient.post('/token/', { username, password })
        const { access, refresh } = response.data

        // 사용자 정보 가져오기
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`
        const userResponse = await apiClient.get('/users/me/')
        
        this.accessToken = access
        this.refreshToken = refresh
        this.user = userResponse.data

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(userResponse.data))

        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || '로그인 실패' 
        }
      }
    },

    async register(userData) {
      try {
        await apiClient.post('/users/register/', userData)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || '회원가입 실패'
        }
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    async fetchCurrentUser() {
      try {
        const response = await apiClient.get('/users/me/')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (error) {
        console.error('Failed to fetch user:', error)
      }
    },
  },
})
