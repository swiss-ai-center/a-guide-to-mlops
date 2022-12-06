import { Callout } from "../../components";

export const callout = {
  render: Callout,
  children: ["paragraph", "tag", "list"],
  attributes: {
    title: {
      type: String,
    },
    type: {
      type: String,
      default: "note",
      matches: ["caution", "check", "note", "warning"],
      errorLevel: "critical",
    },
  },
};
