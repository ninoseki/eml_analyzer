import Vue from "vue";
import { Mixin } from "vue-mixin-decorator";

import { ErrorData } from "@/types";

@Mixin
export class ErrorDialogMixin extends Vue {
  buildMessage(error: ErrorData): string {
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

  alertError(error: ErrorData) {
    // if something goes wrong, the app returns a string (e.g Internal Server Error).
    if (typeof error === "string") {
      error = { detail: error };
    }
    const message = this.buildMessage(error);

    this.$buefy.dialog.alert({
      title: "Error",
      message: message,
      type: "is-danger",
      ariaRole: "alertdialog",
      ariaModal: true,
    });
  }
}
