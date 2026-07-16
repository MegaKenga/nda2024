from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from core.media_optimizer_auth import (
    append_optimizer_token,
    get_media_optimizer_actor,
    get_optimizer_token_from_request,
    media_optimizer_required,
)
from core.media_webp_optimizer import MediaOptimizerJobManager, OptimizerOptions

URL_NAMES = {
    'admin': {
        'page': 'admin:core_media_optimizer',
        'start': 'admin:core_media_optimizer_start',
        'stop': 'admin:core_media_optimizer_stop',
        'reset': 'admin:core_media_optimizer_reset',
        'status': 'admin:core_media_optimizer_status',
        'report': 'admin:core_media_optimizer_report',
    },
    'standalone': {
        'page': 'media_optimizer',
        'start': 'media_optimizer_start',
        'stop': 'media_optimizer_stop',
        'reset': 'media_optimizer_reset',
        'status': 'media_optimizer_status',
        'report': 'media_optimizer_report',
    },
}


def _optimizer_urls(namespace: str, token: str = '') -> dict[str, str]:
    names = URL_NAMES[namespace]
    urls = {key: reverse(name) for key, name in names.items()}
    if token:
        for key in urls:
            urls[key] = append_optimizer_token(urls[key], token)
    return urls


def _page_context(request, namespace: str = 'standalone') -> dict:
    token = get_optimizer_token_from_request(request)
    return {
        'state': MediaOptimizerJobManager.read_state(),
        'media_root': settings.MEDIA_ROOT,
        'report_exists': MediaOptimizerJobManager.report_path().exists(),
        'access_token': token,
        'urls': _optimizer_urls(namespace, token),
    }


@ensure_csrf_cookie
@media_optimizer_required
@require_GET
def media_optimizer_page(request):
    return render(request, 'core/media_optimizer.html', _page_context(request))


@media_optimizer_required
@require_GET
@ensure_csrf_cookie
def media_optimizer_admin_page(request):
    return render(request, 'admin/media_optimizer.html', _page_context(request, namespace='admin'))


def _post_int(request, key: str, default: int) -> int:
    raw = request.POST.get(key, default)
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


@media_optimizer_required
@require_POST
def media_optimizer_start(request):
    if MediaOptimizerJobManager.is_running():
        return JsonResponse({'ok': False, 'error': 'Оптимизация уже выполняется.'}, status=409)

    options = OptimizerOptions(
        media_root=request.POST.get('media_root', '').strip(),
        quality=_post_int(request, 'quality', 82),
        max_width=_post_int(request, 'max_width', 2560),
        dry_run=request.POST.get('dry_run') == '1',
        keep_originals=request.POST.get('keep_originals') == '1',
        skip_db=request.POST.get('skip_db') == '1',
        skip_files=request.POST.get('skip_files') == '1',
    )

    try:
        MediaOptimizerJobManager.start(
            options=options,
            started_by=get_media_optimizer_actor(request),
        )
    except RuntimeError as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=409)
    except Exception as exc:
        return JsonResponse({'ok': False, 'error': f'Ошибка запуска: {exc}'}, status=500)

    return JsonResponse({'ok': True, 'status': 'running'})


@media_optimizer_required
@require_POST
def media_optimizer_stop(request):
    stopped = MediaOptimizerJobManager.stop()
    if not stopped:
        MediaOptimizerJobManager.sync_state()
        return JsonResponse({
            'ok': False,
            'error': 'Процесс не выполняется. Нажмите «Сбросить статус», если интерфейс завис.',
        }, status=409)
    return JsonResponse({'ok': True, 'status': 'stopping'})


@media_optimizer_required
@require_POST
def media_optimizer_reset(request):
    MediaOptimizerJobManager.force_reset()
    return JsonResponse({'ok': True, 'status': 'idle'})


@media_optimizer_required
@require_GET
def media_optimizer_status(request):
    MediaOptimizerJobManager.sync_state()
    from_line = int(request.GET.get('from_line', 0))
    entries, total_lines = MediaOptimizerJobManager.read_log(from_line)
    state = MediaOptimizerJobManager.read_state()
    token = get_optimizer_token_from_request(request)

    namespace = 'admin' if request.path.startswith('/admin/') else 'standalone'
    report_url = ''
    if MediaOptimizerJobManager.report_path().exists():
        report_url = _optimizer_urls(namespace, token)['report']

    return JsonResponse({
        'ok': True,
        'status': state.get('status', 'idle'),
        'state': state,
        'entries': entries,
        'total_lines': total_lines,
        'report_url': report_url,
    })


@media_optimizer_required
@require_GET
def media_optimizer_report(request):
    report_path = MediaOptimizerJobManager.report_path()
    if not report_path.exists():
        namespace = 'admin' if request.path.startswith('/admin/') else 'standalone'
        context = _page_context(request, namespace=namespace)
        context['report_missing'] = True
        template = 'admin/media_optimizer.html' if namespace == 'admin' else 'core/media_optimizer.html'
        return render(request, template, context, status=404)

    return HttpResponse(report_path.read_text(encoding='utf-8'), content_type='text/html; charset=utf-8')
