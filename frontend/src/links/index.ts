import { Link } from "@/types";

import { AnyRun } from "./anyrun";
import { Browserling } from "./browserling";
import { Crtsh } from "./crtsh";
import { EmailRep } from "./emailrep";
import { HybridAnalysis } from "./hybridanalysis";
import { InQuest } from "./inquest";
import { SecurityTrails } from "./securitytrails";
import { Shodan } from "./shodan";
import { UrlscanForDomain, UrlscanForIP, UrlscanForURL } from "./urlscan";
import {
  VirusTotalForDomain,
  VirusTotalForIP,
  VirusTotalForSHA256,
  VirusTotalForURL,
} from "./virustotal";

export const Links: Link[] = [
  new AnyRun(),
  new Browserling(),
  new Crtsh(),
  new EmailRep(),
  new HybridAnalysis(),
  new InQuest(),
  new SecurityTrails(),
  new Shodan(),
  new UrlscanForDomain(),
  new UrlscanForIP(),
  new UrlscanForURL(),
  new VirusTotalForDomain(),
  new VirusTotalForIP(),
  new VirusTotalForSHA256(),
  new VirusTotalForURL(),
];
