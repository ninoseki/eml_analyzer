import { Header } from '@/types'

export const header: Header = {
  messageId: 'test',
  subject: 'test',
  defect: undefined,
  from: 'test@test.com',
  to: ['test@test.com'],
  cc: [],
  date: '2020-06-26T19:01:46+09:00',
  receivedEmail: undefined,
  receivedForemail: ['test@test.com'],
  receivedDomain: ['test@test.com'],
  receivedIp: ['1.1.1.1'],
  receivedSrc: undefined,
  received: [
    {
      by: ['mx.google.com'],
      date: '2020-06-26T03:01:53-07:00',
      for: ['test@test.com'],
      from: ['bmmph0401.jpx1.mta.foo.com', '1.1.1.1'],
      src: 'from bmmph0401.jpx1.mta.foo.com (bmmph0401.jpx1.mta.foo.com. [1.1.1.1]) by mx.google.com with esmtps id t23si17369479plr.47.2020.06.26.03.01.52 for <test@test.com> (version=tls1_2 cipher=ecdhe-ecdsa-aes128-gcm-sha256 bits=128/128); fri, 26 jun 2020 03:01:53 -0700 (pdt)',
      with: 'esmtps id t23si17369479plr.47.2020.06.26.03.01.52',
      delay: 0
    },
    {
      by: ['2002:a67:d211:0:0:0:0:0'],
      date: '2020-06-26T03:01:53-07:00',
      for: [],
      from: [],
      src: 'by 2002:a67:d211:0:0:0:0:0 with smtp id y17csp352571vsi; fri, 26 jun 2020 03:01:53 -0700 (pdt)',
      with: 'smtp id y17csp352571vsi',
      delay: 0
    }
  ],
  header: {
    'received-spf': [
      'pass (google.com: domain of z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com designates 1.1.1.1 as permitted sender) client-ip=1.1.1.1;'
    ],
    'x-google-smtp-source': [
      'ABdhPJynAuSfgxdlFyZKa8N4JPifULWPwMyWEKsHolJ8pNC9GERVBXeb4+L0MhU9oBo8rNc3zQSJ'
    ],
    'message-id': ['<1593165706709.2020101741.excite3.0.9279.00000000@ad144se.mpse.jp>'],
    received: [
      'by 2002:a67:d211:0:0:0:0:0 with SMTP id y17csp352571vsi;        Fri, 26 Jun 2020 03:01:53 -0700 (PDT)',
      'from bmmph0401.jpx1.mta.foo.com (bmmph0401.jpx1.mta.foo.com. [1.1.1.1])        by mx.google.com with ESMTPS id t23si17369479plr.47.2020.06.26.03.01.52        for <test@test.com>        (version=TLS1_2 cipher=ECDHE-ECDSA-AES128-GCM-SHA256 bits=128/128);        Fri, 26 Jun 2020 03:01:53 -0700 (PDT)'
    ],
    'return-path': ['<z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com>'],
    precedence: ['bulk'],
    'arc-message-signature': [
      'i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=precedence:content-transfer-encoding:mime-version:subject         :message-id:to:from:date:errors-to:dkim-signature;        bh=5X/o+J4YmAran7geSjikplGuCf5NG3YpI+9GzTfzt34=;        b=jHiB2xk5BKONH9V1GWizSSG6Se6s7p0lFR6t8IGweC3mpoi5FCsLYRNorTFl8xi2NS         qy1aQAbd66dzi6DwAlFiOu8o1FH2lELz8OOttGUmCR4sVm9SZM/wN4QBe5Ws+3EXviWa         MypP71tqM2w0ZztyO0TdeIlP//K9nGMqBw8PTnXFU8fxJ/USDPPBWpDb36py6/xYJ4+E         FhR9GPY+bRhSLT8PZ4diYw7EJkDe5oNw1HDGMlpjLU6r1sXpeKOiAezfaA5mBuQ5Uovc         Pe+QiemKOo5kQFIVw7KcBaAwYAHw9EVa5CFW6OwXs4Wo2+e3W3m9C2HFvVYK5QG/V3q5         AUeg=='
    ],
    'content-transfer-encoding': ['7bit'],
    'arc-authentication-results': [
      'i=1; mx.google.com;       dkim=pass header.i=@excite.jp header.s=excite.201701 header.b=CTe5NYEx;       spf=pass (google.com: domain of z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com designates 1.1.1.1 as permitted sender) smtp.mailfrom=z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com;       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=excite.jp'
    ],
    'mime-version': ['1.0'],
    'errors-to': ['z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com'],
    'authentication-results': [
      'mx.google.com;       dkim=pass header.i=@excite.jp header.s=excite.201701 header.b=CTe5NYEx;       spf=pass (google.com: domain of z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com designates 1.1.1.1 as permitted sender) smtp.mailfrom=z-excite3-xepsh9-0-75r-008foogmail.com@bma.foo.com;       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=excite.jp'
    ],
    'delivered-to': ['test@test.com'],
    'x-received': [
      'by 2002:aa7:9473:: with SMTP id t19mr1999753pfq.148.1593165713699;        Fri, 26 Jun 2020 03:01:53 -0700 (PDT)'
    ],
    from: ['エキサイトからのお知らせ <support-japan@excite.jp>'],
    'content-type': ['multipart/alternative; boundary="-44e2071d5e8e429d7d1dc98f76e0fb07-1"'],
    'dkim-signature': [
      'v=1; a=rsa-sha256; q=dns/txt; c=relaxed/relaxed; t=1593165713;\ts=excite.201701; d=excite.jp;\th=Date:From:To:Message-Id:Subject:MIME-Version:Content-Type:Content-Transfer-Encoding;\tbh=5X/o+J4YmAran7geSjikplGuCf5NG3YpI+9GzTfzt34=;\tb=CTe5NYExX5M1pLnI5ivQ9aFL9zzE79ruSCe1H/AnjaTYlYAW3ik3PrmRBJU0YKpC\tl6qA6aKNdWH7Yraj3e42jQ0Xvb5d3SCSPvDa1EzYDtXHhn8vRZ+HPh00WByfeExjrC8\t9nLaj30P4YODjvH8oCMc8z79mz0hdlEvRR+fsBGs='
    ],
    date: ['Fri, 26 Jun 2020 19:01:46 +0900'],
    subject: ['foo'],
    'arc-seal': [
      'i=1; a=rsa-sha256; t=1593165713; cv=none;        d=google.com; s=arc-20160816;        b=xeegMa+rviltYXtidrs3Y0HQHa8kz/UtJlxXuqi0BJjH6x1i5T2fu6mvQZE2UXvckL         NNr6mKB8M80RsMeyVTlgGBch4VJde/1eMQuu6D02h6voPYT3yY2zSh/ILUopEgEHiJdG         hab2+Ai/iPkYl0qef+fUr78+ei06Ke2/9zepsKIgbM7sjOPnpkK5ISA5jR5q7cKGxzeU         qiHLRYP9cYokw1SQ/LGhpFQ5oQo0IPbM8SleRPvrqNNUob4/7oFcwMIi73qHRrLz4aNw         bcEmVmtfyzfU5o5ZoykWyuyCKKHQYjZH5pUdZci9fVtkHY7FnpVr/nPtVj9620iBHfMP         dHOg=='
    ],
    to: ['test@test.com']
  }
}
