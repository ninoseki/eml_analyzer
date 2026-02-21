import { describe, expect, it } from 'vitest'

import { DomainTools } from '@/links/domaintools'

describe('DomainTools', function () {
  const subject = new DomainTools()

  describe('#type', function () {
    it('equals to url', function () {
      expect(subject.type).toEqual('domain')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const hash = 'example.com'
      expect(subject.href(hash)).toEqual(
        'https://whois.domaintools.com/example.com'
      )
    })
  })
})
