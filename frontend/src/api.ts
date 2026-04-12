import { ResponseSchema, type ResponseType, StatusSchema, type StatusType } from '@/schemas'

export class FetchError extends Error {
  public response?: { data: unknown }

  constructor(message: string, data?: unknown) {
    super(message)
    this.name = 'FetchError'
    if (data !== undefined) {
      this.response = { data }
    }
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let data: unknown
    try {
      data = await res.json()
    } catch {
      // no JSON body
    }
    throw new FetchError(res.statusText, data)
  }
  return res.json()
}

export const API = {
  async analyze(file: File): Promise<ResponseType> {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch('/api/analyze/file', {
      method: 'POST',
      body: formData
    })
    return ResponseSchema.parse(await handleResponse(res))
  },
  async lookup(id: string): Promise<ResponseType> {
    const res = await fetch(`/api/lookup/${id}`)
    return ResponseSchema.parse(await handleResponse(res))
  },
  async getCacheKeys(): Promise<string[]> {
    const res = await fetch(`/api/cache/`)
    return handleResponse<string[]>(res)
  },
  async getStatus(): Promise<StatusType> {
    const res = await fetch(`/api/status/`)
    return StatusSchema.parse(await handleResponse(res))
  }
}
