from datetime import date, timedelta
from typing import Tuple


def get_required_dates() -> Tuple[date, date]:
    """This processing will always be done for the month that just finished. This function returns the start and end date of the previous month.
    Will be used to remove rows from the input CSVs that contain transactions not in this date range

    Returns:
        Tuple[date, date]: (start date, end date) of the range we want to include transactions for.
        Transactions outside this range will not be included in the budgeting calculations
    """
    today = date.today()
    last_day_of_prev_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_prev_month = today.replace(day=1) - timedelta(
        days=last_day_of_prev_month.day
    )

    return (first_day_of_prev_month, last_day_of_prev_month)
