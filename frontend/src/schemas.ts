import { z } from 'zod'

// ref. https://github.com/colinhacks/zod/issues/4143#issuecomment-2845134912
const functionSchema = <T extends z.core.$ZodFunction>(schema: T) =>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  z.custom<Parameters<T['implement']>[0]>((fn) => schema.implement(fn as any))

const asyncFunctionSchema = <T extends z.core.$ZodFunction>(schema: T) =>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  z.custom<Parameters<T['implementAsync']>[0]>((fn) => schema.implementAsync(fn as any))

export const StatusSchema = z.object({
  cache: z.boolean().optional(),
  vt: z.boolean().optional(),
  emailRep: z.boolean().optional(),
  inquest: z.boolean().optional(),
  urlscan: z.boolean().optional()
})

export type StatusType = z.infer<typeof StatusSchema>

export const HashSchema = z.object({
  md5: z.string(),
  sha1: z.string(),
  sha256: z.string(),
  sha512: z.string()
})

export const HeaderItemSchema = z.object({
  key: z.string(),
  values: z.array(z.union([z.string(), z.number()]))
})

export type HeaderItemType = z.infer<typeof HeaderItemSchema>

const DictionarySchema = z.record(z.string(), z.array(z.union([z.string(), z.number()])))

export const AttachmentSchema = z.object({
  raw: z.string(),
  filename: z.string(),
  size: z.number(),
  extension: z.string().nullish(),
  hash: HashSchema,
  mimeType: z.string(),
  mimeTypeShort: z.string(),
  contentHeader: DictionarySchema
})

export type AttachmentType = z.infer<typeof AttachmentSchema>

export const BodySchema = z.object({
  contentType: z.string().nullish(),
  hash: z.string(),
  contentHeader: DictionarySchema,
  content: z.string(),
  urls: z.array(z.string()),
  emails: z.array(z.string()),
  domains: z.array(z.string()),
  ipAddresses: z.array(z.string())
})

export type BodyType = z.infer<typeof BodySchema>

export const ReceivedSchema = z.object({
  by: z.array(z.string()).nullish(),
  date: z.string(),
  for: z.array(z.string()).nullish(),
  from: z.array(z.string()).nullish(),
  src: z.string(),
  with: z.string().nullish(),
  delay: z.number().nullish()
})

export type ReceivedType = z.infer<typeof ReceivedSchema>

export const HeaderSchema = z.object({
  messageId: z.string().nullish(),
  subject: z.string(),
  defect: z.array(z.string()).nullish(),
  from: z.string().nullish(),
  to: z.array(z.string()),
  cc: z.array(z.string()).nullish(),
  date: z.string(),
  receivedEmail: z.array(z.string()).nullish(),
  receivedForemail: z.array(z.string()).nullish(),
  receivedDomain: z.array(z.string()).nullish(),
  receivedIp: z.array(z.string()).nullish(),
  receivedSrc: z.array(z.string()).nullish(),
  received: z.array(ReceivedSchema).nullish(),
  header: DictionarySchema
})

export type HeaderType = z.infer<typeof HeaderSchema>

export const EmlSchema = z.object({
  attachments: z.array(AttachmentSchema),
  bodies: z.array(BodySchema),
  header: HeaderSchema
})

export type EmlType = z.infer<typeof EmlSchema>

export const DetailSchema = z.object({
  key: z.string(),
  score: z.number().nullish(),
  description: z.string(),
  referenceLink: z.string().nullish()
})

export type DetailType = z.infer<typeof DetailSchema>

export const VerdictSchema = z.object({
  name: z.string(),
  malicious: z.boolean(),
  score: z.number().nullish(),
  details: z.array(DetailSchema)
})

export type VerdictType = z.infer<typeof VerdictSchema>

export const ResponseSchema = z.object({
  id: z.string(),
  eml: EmlSchema,
  verdicts: z.array(VerdictSchema)
})

export type ResponseType = z.infer<typeof ResponseSchema>

export const SubmissionResultSchema = z.object({
  referenceUrl: z.string(),
  status: z.string().nullish()
})

export type SubmissionResultType = z.infer<typeof SubmissionResultSchema>

export const ValidationErrorSchema = z.object({
  loc: z.array(z.string()),
  msg: z.string(),
  type: z.string()
})

export const ErrorDataSchema = z.object({
  detail: z.union([z.string(), z.array(ValidationErrorSchema)])
})

export type ErrorDataType = z.infer<typeof ErrorDataSchema>

export const LinkTypeSchema = z.union([
  z.literal('url'),
  z.literal('email'),
  z.literal('ip'),
  z.literal('domain'),
  z.literal('sha256')
])

export const IndicatorTypeSchema = z.union([
  z.literal('url'),
  z.literal('email'),
  z.literal('ip'),
  z.literal('domain'),
  z.literal('sha256')
])

export type IndicatorType = z.infer<typeof IndicatorTypeSchema>

export const LinkSchema = z.object({
  name: z.string(),
  type: z.string(),
  baseURL: z.string(),
  favicon: z.string(),
  href: functionSchema(z.function({ input: [z.string()], output: z.string() }))
})

export type LinkType = z.infer<typeof LinkSchema>

export const SubmitTypeSchema = z.literal('sha256')

export type SubmitType = z.infer<typeof SubmitTypeSchema>

export const SubmitterSchema = z.object({
  name: z.string(),
  type: SubmitTypeSchema,
  favicon: z.string(),
  submit: asyncFunctionSchema(
    z.function({ input: [AttachmentSchema], output: z.promise(SubmissionResultSchema) })
  )
})

export type SubmitterType = z.infer<typeof SubmitterSchema>
