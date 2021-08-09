import { Base64 } from "js-base64";

type BlobPart = ArrayBuffer | ArrayBufferView | Blob | string;

export function b64toBlob(
  b64data: string,
  contentType = "",
  sliceSize = 512
): Blob {
  const byteCharacters = Base64.atob(b64data);
  const byteArrays: BlobPart[] = [];

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize);

    const byteNumbers = new Array(slice.length);
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    const byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }

  const blob = new Blob(byteArrays, { type: contentType });
  return blob;
}
