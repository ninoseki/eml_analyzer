import { SetupContext } from "@vue/composition-api";

import { ErrorData } from "@/types";

function buildMessage(error: ErrorData): string {
  if (typeof error.detail === "string") {
    return error.detail;
  }

  const messages: string[] = [];
  for (const detail of error.detail) {
    const attr = detail.loc[detail.loc.length - 1];
    messages.push(`Validation error in ${attr} - ${detail.msg}`);
  }
  return messages.join("<br />");
}

export function alertError(error: ErrorData, context: SetupContext): void {
  // if something goes wrong, the app returns a string (e.g Internal Server Error).
  if (typeof error === "string") {
    error = { detail: error };
  }
  const message = buildMessage(error);

  context.root.$buefy.dialog.alert({
    title: "Error",
    message: message,
    type: "is-danger",
    ariaRole: "alertdialog",
    ariaModal: true,
  });
}
