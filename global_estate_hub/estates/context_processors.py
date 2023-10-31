def breadcrumbs_urls(request):
    slugs = [slug.replace('-', ' ').title for slug in request.path.split('/')[1:]]

    return {
        'breadcrumb_urls': slugs,
    }
