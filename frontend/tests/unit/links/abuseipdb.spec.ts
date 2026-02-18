import { describe, expect, it } from 'vitest'

import { Shodan } from '@/links/shodan'

describe('Shodan', function () {
  const subject = new Shodan()

  describe('#type', function () {
    it('equals to ip_address', function () {
      expect(subject.type).toEqual('ip')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = '1.1.1.1'
      expect(subject.href(value)).toEqual('https://www.abuseipdb.com/check/1.1.1.1')
    })
  })
})
