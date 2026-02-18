import { describe, expect, it } from 'vitest'

import { DomainTools } from '@/links/domaintools'

describe('DomainTools', function () {
  const subject = new DomainTools()

  describe('#type', function () {
    it('equals to url', function () {
      expect(subject.type).toEqual('url')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const hash = 'https://example.com'
      expect(subject.href(hash)).toEqual(
        'https://DomainTools.domaintools.com/example.com'
      )
    })
  })
})
