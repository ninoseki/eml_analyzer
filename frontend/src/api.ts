import axios from 'axios'

import type { Response } from '@/types'

const client = axios.create()

export const API = {
  async analyze(file: File): Promise<Response> {
    const formData = new FormData()
    formData.append('file', file)
    const res = await client.post<Response>('/api/analyze/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return res.data
  },
  async lookup(id: string): Promise<Response> {
    const res = await client.get<Response>(`/api/lookup/${id}`)
    return res.data
  },
  async getCacheKeys(): Promise<string[]> {
    const res = await client.get<string[]>(`/api/cache/`)
    return res.data
  }
}
