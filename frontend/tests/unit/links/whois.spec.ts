import { describe, expect, it } from 'vitest'

import { WhoIs } from '@/links/whois'

describe('WhoIs', function () {
  const subject = new WhoIs()

  describe('#type', function () {
    it('equals to url', function () {
      expect(subject.type).toEqual('url')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const hash = 'https://example.com'
      expect(subject.href(hash)).toEqual(
        'https://whois.domaintools.com/example.com'
      )
    })
  })
})
