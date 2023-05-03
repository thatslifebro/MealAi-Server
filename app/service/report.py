from app.dao.report import get_report_week


def service_get_report_week(week: int):
    return get_report_week(week)
