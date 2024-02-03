import { describe, expect, it } from 'vitest'

import { UrlscanForDomain, UrlscanForIP, UrlscanForURL } from '@/links/urlscan'

describe('Urlscan for ip address', function () {
  const subject = new UrlscanForIP()

  describe('#type', function () {
    it('equals to ip_address', function () {
      expect(subject.type).toEqual('ip')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = '1.1.1.1'
      expect(subject.href(value)).toEqual('https://urlscan.io/ip/1.1.1.1')
    })
  })
})

describe('Urlscan for domain', function () {
  const subject = new UrlscanForDomain()

  describe('#type', function () {
    it('equals to domain', function () {
      expect(subject.type).toEqual('domain')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = 'example.com'
      expect(subject.href(value)).toEqual('https://urlscan.io/domain/example.com')
    })
  })
})

describe('Urlscan for URL', function () {
  const subject = new UrlscanForURL()

  describe('#type', function () {
    it('equals to domain', function () {
      expect(subject.type).toEqual('url')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = 'http://example.com'
      expect(subject.href(value)).toEqual(
        'https://urlscan.io/search/#task.url%3A%22http%3A%2F%2Fexample.com%22'
      )
    })
  })
})
