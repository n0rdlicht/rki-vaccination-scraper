module.exports = {
  dest: 'public',
  locales: {
    '/': {
      lang: 'en-US',
      title: 'Historized COVID-19 Vaccination Data API',
      description: 'A JSON-API serving COVID-19 vaccination monitoring data published by the RKI.',
    },
  },
  themeConfig: {
    repo: 'n0rdlicht/rki-vaccination-scraper',
    editLinks: true,
    locales: {
      '/': {
        search: true,
        label: 'English',
        selectText: 'Languages',
        ariaLabel: 'Select language',
        editLinkText: 'Edit this page on GitHub',
        lastUpdated: 'Last Updated',
        nav: [{
            text: 'Guide',
            link: '/'
          },
        ],
        sidebar: 'auto',
      }
    }
  }
}