import * as React from "react";

import { Icon } from "./Icon";

const TYPE_MAP = {
  check: {
    icon: "checkmark-circle",
    iconColor: "var(--black)",
  },
  error: {
    icon: "warning",
    iconColor: "#ed5f74",
  },
  note: {
    icon: "information-circle",
    iconColor: "#8792a2",
  },
  warning: {
    icon: "warning",
    iconColor: "#d97917",
  },
};

export function Callout({ title, children, type }) {
  const { icon, iconColor } = TYPE_MAP[type] || TYPE_MAP.note;

  return (
    <div className="callout">
      <div className="flex content">
        <div className="flex icon">
          <Icon icon={icon} color={iconColor} />
        </div>
        <div className="flex column">
          <strong>{title}</strong>
          <span>{children}</span>
        </div>
      </div>
      <style jsx>
        {`
          .callout {
            padding: 0 0 1rem;
          }
          .content {
            color: var(--dark);
            background: var(--code-background);
            border: 1px solid var(--code-border);
            line-height: 20px;
            padding: 12px 20px;
            border-radius: 4px;
          }
          .icon {
            padding-right: 8px;
            align-items: center;
          }
          .callout :global(p:first-of-type) {
            padding: 0;
          }
        `}
      </style>
    </div>
  );
}
