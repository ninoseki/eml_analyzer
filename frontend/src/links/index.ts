import { Link } from "@/types";

import { AnyRun } from "./anyrun";
import { Crtsh } from "./crtsh";
import { EmailRep } from "./emailrep";
import { HybridAnalysis } from "./hybridanalysis";
import { SecurityTrails } from "./securitytrails";
import { Shodan } from "./shodan";
import { UrlscanForDomain, UrlscanForIP } from "./urlscan";
import {
  VirusTotalForDomain,
  VirusTotalForIP,
  VirusTotalForSHA256,
  VirusTotalForURL,
} from "./virustotal";

export const Links: Link[] = [
  new AnyRun(),
  new Crtsh(),
  new EmailRep(),
  new HybridAnalysis(),
  new SecurityTrails(),
  new Shodan(),
  new UrlscanForDomain(),
  new UrlscanForIP(),
  new VirusTotalForDomain(),
  new VirusTotalForIP(),
  new VirusTotalForSHA256(),
  new VirusTotalForURL(),
];
