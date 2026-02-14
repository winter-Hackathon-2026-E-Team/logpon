from django.db import transaction
from django.db.models import F, Max

from apps.programs.models import ProgramTimer


def add_timer_to_program(*, program, timer) -> ProgramTimer:
    max_idx = (
        ProgramTimer.objects.filter(program=program).aggregate(m=Max("order_index"))["m"]
        or 0
    )
    return ProgramTimer.objects.create(program=program, timer=timer, order_index=max_idx + 1)


def delete_program_timer(*, program_timer: ProgramTimer) -> None:
    program = program_timer.program
    deleted_order = program_timer.order_index

    with transaction.atomic():
        program_timer.delete()
        # 後ろを詰める（1,2,3…を維持）
        ProgramTimer.objects.filter(program=program, order_index__gt=deleted_order).update(
            order_index=F("order_index") - 1
        )


def reorder_program_timers(*, program, ordered_ids: list[int]) -> None:
    existing_ids = list(
        ProgramTimer.objects.filter(program=program).values_list("id", flat=True)
    )

    if set(ordered_ids) != set(existing_ids) or len(ordered_ids) != len(existing_ids):
        raise ValueError("reorder target mismatch")

    with transaction.atomic():
        # UNIQUE(program, order_index) 回避のため一旦+1000
        ProgramTimer.objects.filter(program=program).update(order_index=F("order_index") + 1000)
        for idx, pt_id in enumerate(ordered_ids, start=1):
            ProgramTimer.objects.filter(id=pt_id, program=program).update(order_index=idx)
