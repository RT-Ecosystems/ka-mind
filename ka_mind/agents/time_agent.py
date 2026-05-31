# KA-Mind Time Agent — Date, time, calendar
from datetime import datetime, timedelta
import re


class TimeAgent:
    def answer(self, query: str) -> str:
        q = query.lower()
        now = datetime.now()
        if any(w in q for w in ['time','समय','बजे','clock']):
            return f'Current time: {now.strftime("%I:%M %p")} ({now.strftime("%H:%M")})'
        if any(w in q for w in ['date','तारीख','today','आज']):
            return f'Today: {now.strftime("%A, %d %B %Y")}'
        if any(w in q for w in ['year','वर्ष','साल']):
            return f'Current year: {now.year}'
        if 'tomorrow' in q or 'कल' in q:
            tom = now + timedelta(days=1)
            return f'Tomorrow: {tom.strftime("%A, %d %B %Y")}'
        if 'yesterday' in q:
            yes = now - timedelta(days=1)
            return f'Yesterday: {yes.strftime("%A, %d %B %Y")}'
        return f'Current date & time: {now.strftime("%A, %d %B %Y — %I:%M %p")}'
