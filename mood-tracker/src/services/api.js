const API_BASE = 'http://localhost:3001/api'

const getHeaders = () => {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` })
  }
}

export const api = {
  async register(username, password) {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || '注册失败')
    }
    return response.json()
  },

  async login(username, password) {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || '登录失败')
    }
    return response.json()
  },

  async addMoodRecord(data) {
    const response = await fetch(`${API_BASE}/mood`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data)
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || '记录失败')
    }
    return response.json()
  },

  async getMoodRecords(startDate, endDate) {
    const params = new URLSearchParams()
    if (startDate) params.append('startDate', startDate)
    if (endDate) params.append('endDate', endDate)
    
    const response = await fetch(`${API_BASE}/mood?${params}`, {
      headers: getHeaders()
    })
    if (!response.ok) throw new Error('获取记录失败')
    return response.json()
  },

  async getMoodStats(days = 30) {
    const response = await fetch(`${API_BASE}/mood/stats?days=${days}`, {
      headers: getHeaders()
    })
    if (!response.ok) throw new Error('获取统计数据失败')
    return response.json()
  },

  async deleteMoodRecord(id) {
    const response = await fetch(`${API_BASE}/mood/${id}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!response.ok) throw new Error('删除失败')
    return response.json()
  }
}
