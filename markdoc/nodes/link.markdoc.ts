// @ts-ignore
import { link as linktag } from "@markdoc/next.js/tags";

import { AppLink } from "../../components";

export const link = {
  ...linktag,
  render: AppLink,
};
