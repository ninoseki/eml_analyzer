import { describe, expect, it } from 'vitest'

import { humanizeSeconds, toCSV } from '@/utils'

describe('toCSV', function () {
  it.each([
    [['a', 'b', 'c'], 'a, b, c'],
    [[], '']
  ])('returns CSV string', (values: string[], expected: string) => {
    expect(toCSV(values)).toBe(expected)
  })
})

describe('secondsToHumanize', () => {
  it.each([
    [60, 'a minute'],
    [120, '2 minutes'],
    [180, '3 minutes']
  ])('returns humanized seconds', (seconds, expected) => {
    expect(humanizeSeconds(seconds)).toBe(expected)
  })
})
