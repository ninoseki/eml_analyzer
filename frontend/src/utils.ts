import dayjs from 'dayjs'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'
import {
  isDomain,
  isEmail,
  isIPv4,
  isIPv6,
  isSHA256,
  isURL
} from 'ioc-extractor/dist/aux/validators'
import { Base64 } from 'js-base64'
import qs from 'qs'

dayjs.extend(utc)
dayjs.extend(duration)
dayjs.extend(relativeTime)

type BlobPart = ArrayBuffer | ArrayBufferView | Blob | string

export function b64toBlob(b64data: string, contentType = '', sliceSize = 512): Blob {
  const byteCharacters = Base64.atob(b64data)
  const byteArrays: BlobPart[] = []

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize)

    const byteNumbers = new Array(slice.length)
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }

    const byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }

  const blob = new Blob(byteArrays, { type: contentType })
  return blob
}

export function toCSV(values: string[]): string {
  return values.join(', ')
}

export function buildURL(baseURL: string, path: string, params = {}): string {
  const queryString: string = qs.stringify(params)
  if (queryString === '') {
    return `${baseURL}${path}`
  } else {
    return `${baseURL}${path}?${queryString}`
  }
}

export function base64fy(s: string): string {
  return Base64.encode(s).trim()
}

export function humanizeSeconds(seconds: number): string {
  if (seconds === 0) {
    return '-'
  }
  const duration = dayjs.duration(seconds, 'seconds')
  return duration.humanize(false)
}

export function toUTC(dt: string) {
  return dayjs.utc(dt).format()
}

export function getIndicatorType(value: string) {
  if (isURL(value)) {
    return 'url'
  }

  if (isEmail(value)) {
    return 'email'
  }

  if (isDomain(value)) {
    return 'domain'
  }

  if (isIPv4(value) || isIPv6(value)) {
    return 'ip'
  }

  if (isSHA256(value)) {
    return 'sha256'
  }

  return undefined
}
