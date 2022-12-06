const withMarkdoc = require('@markdoc/next.js');

// https://www.viget.com/articles/host-build-and-deploy-next-js-projects-on-github-pages/
const isGithubActions = process.env.GITHUB_ACTIONS || false

let basePath = ''

if (isGithubActions) {
  // trim off `<owner>/`
  const repo = process.env.GITHUB_REPOSITORY.replace(/.*?\//, '')

  basePath = `/${repo}`
}

module.exports =
  withMarkdoc(/* config: https://markdoc.io/docs/nextjs#options */)({
    reactStrictMode: true,
    pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdoc'],
    basePath,
    images: {
      unoptimized: true,
    },
  });
