from django.db.models import QuerySet

from apps.timers.models import Timer


def get_timer_list_qs(*, include_inactive: bool = False) -> QuerySet[Timer]:
    """
    タイマー一覧取得を1か所に集約する。
    - 並び順
    - is_activeの扱い
    - select_related などの最適化
    """
    qs = Timer.objects.select_related("sound").order_by("-id")

    # is_active運用するなら「一覧は有効のみ」をここで統一
    if not include_inactive:
        qs = qs.filter(is_active=True)

    return qs
