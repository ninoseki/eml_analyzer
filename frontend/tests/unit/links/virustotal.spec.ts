import { describe, expect, it } from 'vitest'

import {
  VirusTotalForDomain,
  VirusTotalForIP,
  VirusTotalForSHA256,
  VirusTotalForURL
} from '@/links/virustotal'

describe('VT for domain', function () {
  const subject = new VirusTotalForDomain()

  describe('#type', function () {
    it('equals to domain', function () {
      expect(subject.type).toEqual('domain')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = 'example.com'
      expect(subject.href(value)).toEqual(
        'https://www.virustotal.com/gui/domain/example.com/details'
      )
    })
  })
})

describe('VT for ip address', function () {
  const subject = new VirusTotalForIP()

  describe('#type', function () {
    it('equals to ip_address', function () {
      expect(subject.type).toEqual('ip')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = '1.1.1.1'
      expect(subject.href(value)).toEqual(
        'https://www.virustotal.com/gui/ip-address/1.1.1.1/details'
      )
    })
  })
})

describe('VT for URL', function () {
  const subject = new VirusTotalForURL()

  describe('#type', function () {
    it('equals to url', function () {
      expect(subject.type).toEqual('url')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      expect(subject.href('https://virustotal.com/')).toEqual(
        'https://www.virustotal.com/gui/url/77af0145fa9290ca3a4c214eb4561fc01070132300f6265e2c4cfb447372422e/details'
      )

      expect(subject.href('https://virustotal.com')).toEqual(
        'https://www.virustotal.com/gui/url/77af0145fa9290ca3a4c214eb4561fc01070132300f6265e2c4cfb447372422e/details'
      )

      expect(subject.href('https://qiita.com/trend')).toEqual(
        'https://www.virustotal.com/gui/url/5dd2d006b4430a593be125eee20494016d3ac933796da6deef590c3e045a685d/details'
      )
    })
  })
})

describe('VT for SHA256', function () {
  const subject = new VirusTotalForSHA256()

  describe('#type', function () {
    it('equals to sha256', function () {
      expect(subject.type).toEqual('sha256')
    })
  })

  describe('#href', function () {
    it('returns URL', function () {
      const value = '275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f'
      expect(subject.href(value)).toEqual(
        'https://www.virustotal.com/gui/file/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/details'
      )
    })
  })
})
