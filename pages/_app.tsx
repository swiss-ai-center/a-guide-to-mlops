import React from "react";
import Head from "next/head";
import "prismjs";
// Import other Prism themes here
import "prismjs/components/prism-bash.min";
import "prismjs/components/prism-json.min";
import "prismjs/components/prism-yaml.min";
import "prismjs/themes/prism.css";
import "../public/globals.css";
import {
  AppLink as Link,
  Footer,
  SideNav,
  TableOfContents,
  TopNav,
} from "../components";

import type { AppProps } from "next/app";
import type { MarkdocNextJsPageProps } from "@markdoc/next.js";

const TITLE = "A guide to MLOps";
const DESCRIPTION =
  "A simple yet complete guide to MLOps tools and practices - from a conventional way to a modern approach of working with ML projects.";

function collectHeadings(node, sections = []) {
  if (node) {
    if (node.name === "Heading") {
      const title = node.children[0];

      if (typeof title === "string") {
        sections.push({
          ...node.attributes,
          title,
        });
      }
    }

    if (node.children) {
      for (const child of node.children) {
        collectHeadings(child, sections);
      }
    }
  }

  return sections;
}

export type MyAppProps = MarkdocNextJsPageProps;

export default function MyApp({ Component, pageProps }: AppProps<MyAppProps>) {
  const { markdoc } = pageProps;

  let title = TITLE;
  let description = DESCRIPTION;
  if (markdoc) {
    if (markdoc.frontmatter.title) {
      title = markdoc.frontmatter.title;
    }
    if (markdoc.frontmatter.description) {
      description = markdoc.frontmatter.description;
    }
  }

  const toc = pageProps.markdoc?.content
    ? collectHeadings(pageProps.markdoc.content)
    : [];

  return (
    <>
      <Head>
        <title>{`${title} | ${TITLE}`}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="referrer" content="strict-origin" />
        <meta name="title" content={title} />
        <meta name="description" content={description} />
        <link rel="shortcut icon" href="/favicon.ico" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* https://webaim.org/techniques/skipnav/ */}
      <a href="#skip-nav" className="skip-nav">
        Skip to content
      </a>
      <TopNav>
        <Link href="https://github.com/csia-pme/a-guide-to-mlops">GitHub</Link>
      </TopNav>
      <div className="page">
        <SideNav />
        <main className="flex column">
          <Component {...pageProps} />
        </main>
        <TableOfContents toc={toc} />
      </div>
      <div className="footer-bar">
        <Footer />
      </div>
      <style jsx global>
        {`
          .page {
            display: flex;
            flex-grow: 1;
            padding-top: var(--nav-height);
            min-height: 100vh;
            max-width: 100vw;
          }
          .dark .page {
            border-bottom-color: var(--black-light);
          }
          .skip-nav {
            border: 0;
            clip: rect(0 0 0 0);
            height: 1px;
            width: 1px;
            margin: -1px;
            padding: 0;
            overflow: hidden;
            position: absolute;
            text-decoration: none;
          }
          .skip-nav:focus {
            padding: 1rem;
            position: fixed;
            top: 10px;
            left: 10px;
            background: var(--light);
            z-index: 1000;
            width: auto;
            height: auto;
            clip: auto;
          }
          main {
            flex-grow: 1;
            max-width: 100%;
            /* https://stackoverflow.com/questions/36230944/prevent-flex-items-from-overflowing-a-container */
            min-width: 0;
          }
          main article {
            padding: 2rem 1.5rem 3rem;
          }
          .footer-bar {
            flex: 1;
            padding: 0;
            border-top: 1px solid var(--gray-medium);
          }
          .footer-bar footer {
            margin: 0 auto;
            max-width: calc(100% - 4rem);
          }
        `}
      </style>
    </>
  );
}
