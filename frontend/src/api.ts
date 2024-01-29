import axios from "axios"

import { Response } from "@/types"

const client = axios.create()

export const API = {
  async analyzeFile(file: File | undefined): Promise<Response> {
    const formData = new FormData()
    if (file !== undefined) {
      formData.append("file", file)
    }

    const res = await client.post<Response>("/api/analyze/file", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })
    return res.data
  },
  async lookupFile(identifier: string) : Promise<Response> {
    const res = await client.get<Response>(`/api/lookup/${identifier}/`);
    return res.data
  }
}
