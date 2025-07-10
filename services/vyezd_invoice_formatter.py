import re

def format_vyezd_invoice_block(client_name, records):
    """
    Возвращает (block, total) для клиента по выездным тренировкам.
    block — текст блока без заголовка и реквизитов.
    total — сумма по всем All $.
    """
    lines = ["Тренировки:"]
    total = 0
    for row in records:
        date = row.get('Date', '—')
        desc = row.get('Description', 'Выездная тренировка')
        all_sum = row.get('All $', '0')
        digits = re.sub(r'[^\d]', '', str(all_sum))
        all_sum_int = int(digits) if digits else 0
        total += all_sum_int
        parts = []
        for label, col in [
            ("Тренировка", 'Tren $'),
            ("Перевозка", 'Trans $'),
            ("Бензин", 'Gas $'),
            ("Трек", 'Track $'),
            ("Перекус", 'Food $'),
            ("Прочее", 'Other'),
        ]:
            val = row.get(col, '').replace(' ', '').replace('₽', '')
            if val and val != '0':
                parts.append(f"{label}: {val}₽")
        parts_str = f" ({' / '.join(parts)})" if parts else ""
        lines.append(f"- {date} — {desc} = {all_sum}₽{parts_str}")
    block = "\n".join(lines)
    return block, total 