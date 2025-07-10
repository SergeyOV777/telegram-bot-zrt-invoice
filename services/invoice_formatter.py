import re
from typing import Sequence, Tuple, Optional

def parse_money(val: str) -> int:
    """Убирает все, кроме цифр, и возвращает сумму в целых рублях."""
    try:
        digits = re.sub(r'[^\d]', '', val or '')
        return int(digits) if digits else 0
    except Exception:
        return 0

def format_invoice_block(client_name: str, records):
    """
    Возвращает (block, total) для обслуживания мотоцикла.
    block — текст блока без заголовка и реквизитов.
    total — сумма обслуживания.
    """
    lines = ["Обслуживание мотоцикла:"]
    total = 0
    for row in records:
        date = row.get('Дата', '—')
        work = row.get('Работа', '—')
        work_sum = row.get('Сумма работа', '0')
        part_sum = row.get('Сумма запчасть', '0')
        try:
            work_sum_int = int(str(work_sum).replace(' ', '').replace('₽', '')) if work_sum else 0
        except Exception:
            work_sum_int = 0
        try:
            part_sum_int = int(str(part_sum).replace(' ', '').replace('₽', '')) if part_sum else 0
        except Exception:
            part_sum_int = 0
        amount = work_sum_int + part_sum_int
        total += amount
        parts = []
        if work_sum_int:
            parts.append(f"работа {work_sum_int}₽")
        if part_sum_int:
            parts.append(f"запчасть {part_sum_int}₽")
        parts_str = f" ({', '.join(parts)})" if parts else ""
        lines.append(f"- {date} — {work} = {amount}₽{parts_str}")
    block = "\n".join(lines)
    return block, total
