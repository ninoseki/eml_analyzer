import { describe, expect, it } from 'vitest'

import { buildURL, stringifyParams, truncate } from '@/utils'

describe('stringifyParams', function () {
  it.each([
    { name: 'empty object', params: {}, expected: '' },
    { name: 'single pair', params: { q: 'example.com' }, expected: 'q=example.com' },
    {
      name: 'multiple pairs',
      params: { q: 'example.com', page: 2 },
      expected: 'q=example.com&page=2'
    },
    { name: 'special characters', params: { q: 'a b&c' }, expected: 'q=a+b%26c' },
    { name: 'non-string values', params: { n: 42, b: true }, expected: 'n=42&b=true' }
  ])('returns "$expected" for $name', function ({ params, expected }) {
    expect(stringifyParams(params)).toEqual(expected)
  })
})

describe('buildURL', function () {
  it.each([
    {
      name: 'no params',
      args: ['https://example.com', '/foo'] as const,
      expected: 'https://example.com/foo'
    },
    {
      name: 'empty params',
      args: ['https://example.com', '/foo', {}] as const,
      expected: 'https://example.com/foo'
    },
    {
      name: 'with params',
      args: ['https://example.com', '/search', { q: 'eml' }] as const,
      expected: 'https://example.com/search?q=eml'
    }
  ])('returns "$expected" with $name', function ({ args, expected }) {
    expect(buildURL(...args)).toEqual(expected)
  })
})

describe('truncate', function () {
  it.each([
    {
      name: 'shorter than limit',
      input: 'short',
      length: 16,
      suffix: undefined,
      expected: 'short'
    },
    {
      name: 'equal to limit',
      input: 'exactly10!',
      length: 10,
      suffix: undefined,
      expected: 'exactly10!'
    },
    {
      name: 'longer than limit (default suffix)',
      input: 'abcdefghijklmnop',
      length: 8,
      suffix: undefined,
      expected: 'abcde...'
    },
    {
      name: 'longer than limit (custom suffix)',
      input: 'abcdefghij',
      length: 6,
      suffix: '…',
      expected: 'abcde…'
    }
  ])('returns "$expected" when $name', function ({ input, length, suffix, expected }) {
    expect(
      suffix === undefined ? truncate(input, length) : truncate(input, length, suffix)
    ).toEqual(expected)
  })
})
