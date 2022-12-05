import * as React from 'react';
import { useRouter } from 'next/router';

export function Heading({id = '', level = 1, children, className}) {
  const link = React.createElement(
    `h${level}`,
    {
      id,
      className: ['heading', className].filter(Boolean).join(' '),
    },
    children,
    <style jsx>
        {`
          a {
            text-decoration: none;
          }
          a:hover {
            opacity: 1;
          }
          div {
            position: absolute;
            top: calc(-1 * (var(--nav-height) + 44px));
          }
        `}
      </style>
  );

  return level !== 1 ? (
    <a href={`#${id}`}>
      {link}
      <style jsx>
        {`
          a {
            text-decoration: none;
          }
          a:hover {
            opacity: 1;
          }
          a :global(.heading::after) {
            opacity: 0;
            color: var(--toc-border);
            content: '  #';
            transition: opacity 250ms ease;
          }
          a :global(.heading:hover::after) {
            opacity: 1;
          }
        `}
      </style>
    </a>
  ) : (
    link
  );
}
