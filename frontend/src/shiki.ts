import html from '@shikijs/langs/html'
import githubDarkDefault from '@shikijs/themes/github-dark-default'
import type { CodeToHastOptions } from 'shiki/core'
import { createHighlighterCore } from 'shiki/core'
import { createJavaScriptRegexEngine } from 'shiki/engine/javascript'

// don't use WASM (CSP blocks it)
// ref. https://shiki.matsu.io/guide/install#highlighter-usage
const highlighter = createHighlighterCore({
  themes: [githubDarkDefault],
  langs: [html],
  engine: createJavaScriptRegexEngine()
})

export const codeToHtml = async (code: string, options: CodeToHastOptions): Promise<string> => {
  return (await highlighter).codeToHtml(code, options)
}
