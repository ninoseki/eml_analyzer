export function toCommaSeparatedString(words: string[] | undefined): string {
  if (words == undefined) {
    return "N/A"
  }
  return words.join(", ")
}
