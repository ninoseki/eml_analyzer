import axios from 'axios'

import { ResponseSchema, type ResponseType, StatusSchema, type StatusType } from '@/schemas'

const client = axios.create()

export const API = {
  async analyze(file: File): Promise<ResponseType> {
    const formData = new FormData()
    formData.append('file', file)
    const res = await client.post('/api/analyze/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return ResponseSchema.parse(res.data)
  },
  async lookup(id: string): Promise<ResponseType> {
    const res = await client.get(`/api/lookup/${id}`)
    return ResponseSchema.parse(res.data)
  },
  async getCacheKeys(): Promise<string[]> {
    const res = await client.get<string[]>(`/api/cache/`)
    return res.data
  },
  async getStatus(): Promise<StatusType> {
    const res = await client.get(`/api/status/`)
    return StatusSchema.parse(res.data)
  }
}
