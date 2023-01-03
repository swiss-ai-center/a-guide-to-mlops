import React from "react";
import { useRouter } from "next/router";
import Link from "next/link";

const items = [
  {
    title: "Get started",
    links: [
      { href: "/get-started/what-is-mlops", children: "What is MLOps?" },
      {
        href: "/get-started/what-problems-is-mlops-trying-to-solve",
        children: "What problems is MLOps trying to solve?",
      },
      {
        href: "/get-started/why-would-mlops-be-useful-for-me",
        children: "Why would MLOps be useful for me?",
      },
      {
        href: "/get-started/the-tools-used-in-this-guide",
        children: "The tools used in this guide",
      },
      {
        href: "/get-started/known-limitations",
        children: "Known limitations",
      },
    ],
  },
  {
    title: "The guide",
    links: [
      { href: "/the-guide/introduction", children: "Introduction" },
      {
        href: "/the-guide/step-1-run-a-simple-ml-experiment",
        children: "Step 1: Run a simple ML experiment",
      },
      {
        href: "/the-guide/step-2-share-your-ml-experiment-code-with-git",
        children: "Step 2: Share your ML experiment code with Git",
      },
      {
        href: "/the-guide/step-3-share-your-ml-experiment-data-with-dvc",
        children: "Step 3: Share your ML experiment data with DVC",
      },
      {
        href: "/the-guide/step-4-reproduce-the-experiment-with-dvc",
        children: "Step 4: Reproduce the experiment with DVC",
      },
      {
        href: "/the-guide/step-5-track-model-evolutions-with-dvc",
        children: "Step 5: Track model evolutions with DVC",
      },
      {
        href: "/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline",
        children: "Step 6: Orchestrate the workflow with a CI/CD pipeline",
      },
      {
        href: "/the-guide/step-7-track-model-evolutions-in-the-cicd-pipeline-with-cml",
        children: "Step 7: Track model evolutions in the CI/CD pipeline with CML",
      },
      {
        href: "/the-guide/step-8-share-and-deploy-model-with-mlem",
        children: "Step 8: Share and deploy model with MLEM",
      },
      {
        href: "/the-guide/conclusion",
        children: "Conclusion",
      },
    ],
  },
  {
    title: "Labelization",
    links: [
      { href: "/label-studio/introduction", children: "Introduction" },
      {
        href: "/label-studio/create-a-label-studio-project",
        children: "Create a Label Studio project",
      },
      {
        href: "/label-studio/convert-and-import-existing-data-to-label-studio",
        children: "Convert and import existing data to Label Studio",
      },
      {
        href: "/label-studio/annotate-new-data-with-label-studio",
        children: "Annotate new data with Label Studio",
      },
      {
        href: "/label-studio/export-data-from-label-studio",
        children: "Export data from Label Studio",
      },
    ],
  },
  {
    title: "Advanced concepts",
    links: [
      {
        href: "/advanced-concepts/deploy-minio",
        children: "Deploy MinIO",
      },
      {
        href: "/advanced-concepts/deploy-label-studio",
        children: "Deploy Label Studio",
      },
      {
        href: "/advanced-concepts/link-your-ml-model-with-label-studio",
        children: "Link your ML model with Label Studio",
      },
      {
        href: "/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml",
        children: "Train the model on a Kubernetes cluster with CML",
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
          <h3>{item.title}</h3>
          <ul className="flex column">
            {item.links.map((link) => {
              const active = router.pathname === link.href;
              return (
                <li key={link.href} className={active ? "active" : ""}>
                  <Link {...link} legacyBehavior>
                    <a href={link.href}>{link.children}</a>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
      <style jsx>
        {`
          nav {
            /* https://stackoverflow.com/questions/66898327/how-to-keep-footer-from-pushing-up-sticky-sidebar */
            position: sticky;
            top: var(--nav-height);
            height: calc(100vh - var(--nav-height));
            flex: 0 0 240px;
            overflow-y: auto;
            padding: 2rem 0 2rem 2rem;
          }
          h3 {
            font-weight: 500;
            margin: 0.5rem 0 0;
            padding-bottom: 0.5rem;
          }
          ul {
            margin: 0;
            padding: 0;
          }
          li {
            list-style-type: none;
            margin: 0 0 0.7rem 0.7rem;
            font-size: 14px;
            font-weight: 400;
          }
          li a {
            text-decoration: none;
          }
          li a:hover,
          li.active > a {
            text-decoration: underline;
          }
          @media screen and (max-width: 600px) {
            nav {
              display: none;
            }
          }
        `}
      </style>
    </nav>
  );
}
