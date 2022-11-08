import React from "react";
import { useRouter } from "next/router";
import Link from "next/link";

const items = [
  {
    title: "Get started",
    links: [
      { href: "/", children: "What is MLOps?" },
      { href: "/", children: "What problems is MLOps trying to solve?" },
      { href: "/", children: "Why would MLOps be useful for me?" },
      { href: "/", children: "The tools used in this guide" },
    ],
  },
  {
    title: "The guide",
    links: [
      { href: "/", children: "Prerequesties" },
      { href: "/", children: "Step 1: Run a simple ML experiment" },
      { href: "/", children: "Step 2: Share your ML experiment code with Git" },
      {
        href: "/",
        children:
          "Step 3: Share your ML experiment data with DVC",
      },
      {
        href: "/",
        children: "Step 4: Save the commands to run the experiment in DVC",
      },
      {
        href: "/",
        children: "Step 5: Track the changes made to a model with DVC",
      },
      {
        href: "/",
        children: "Step 6: Orchestrate the workflow with A CI/CD pipeline",
      },
      { href: "/", children: "Step 7: Visualize model evolutions with CML" },
      { href: "/", children: "Step 8: Share and deploy model with MLEM" },
    ],
  },
  {
    title: "Labelization",
    links: [
      { href: "/", children: "Label Studio presentation" },
      { href: "/", children: "Create a Label Studio project" },
      {
        href: "/",
        children: "Convert and import existing data to Label Studio",
      },
      { href: "/", children: "Annotate new data with Label Studio" },
      { href: "/", children: "Export data from Label Studio" },
      { href: "/", children: "Link your ML model with Label Studio" },
    ],
  },
  {
    title: "Advanced concepts",
    links: [
      {
        href: "/",
        children: "Train the model on a Kubernetes cluster with CML",
      },
      {
        href: "/",
        children: "Deploy MinIO",
      },
      {
        href: "/",
        children: "Deploy Label Studio",
      },
    ],
  },
];

export function SideNav() {
  const router = useRouter();

  return (
    <nav className="sidenav">
      {items.map((item) => (
        <div key={item.title}>
          <span>{item.title}</span>
          <ul className="flex column">
            {item.links.map((link) => {
              const active = router.pathname === link.href;
              return (
                <li key={link.href} className={active ? "active" : ""}>
                  <Link {...link} />
                </li>
              );
            })}
          </ul>
        </div>
      ))}
      <style jsx>
        {`
          nav {
            position: sticky;
            top: var(--top-nav-height);
            height: calc(100vh - var(--top-nav-height));
            flex: 0 0 auto;
            overflow-y: auto;
            padding: 2.5rem 2rem 2rem;
            border-right: 1px solid var(--border-color);
          }
          span {
            font-size: larger;
            font-weight: 500;
            padding: 0.5rem 0 0.5rem;
          }
          ul {
            padding: 0;
          }
          li {
            list-style: none;
            margin: 0;
          }
          li :global(a) {
            text-decoration: none;
          }
          li :global(a:hover),
          li.active :global(a) {
            text-decoration: underline;
          }
        `}
      </style>
    </nav>
  );
}
