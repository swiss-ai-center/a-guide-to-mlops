import React from "react";
import Link from "next/link";

export function AppLink(props) {
  const target =
    props.target || (props.href.startsWith("http") ? "_blank" : undefined);

  return (
    <Link
      {...props}
      passHref
      target={target}
      rel={target === "_blank" ? "noreferrer" : undefined}
      className={props.className}
      legacyBehavior
    >
      {props.children}
    </Link>
  );
}
