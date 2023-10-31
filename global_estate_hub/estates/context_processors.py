def breadcrumbs_urls(request):
    return {
        'breadcrumb_urls': request.path.split('/')[1:],
    }
