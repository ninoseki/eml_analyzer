import { Submitter } from "@/types";

import { InQuest } from "./inquest";
import { VirusTotal } from "./virustotal";

export const Submitters: Submitter[] = [new InQuest(), new VirusTotal()];
