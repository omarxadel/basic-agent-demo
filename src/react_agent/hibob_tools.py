"""Mock HiBob-compatible tools and in-memory data store."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from itertools import count
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


def _utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {value}") from exc


def _normalize_field_path(field_path: str) -> str:
    if field_path.startswith("/"):
        return field_path
    if "." in field_path:
        parts = field_path.split(".")
        return f"/{'/'.join(parts)}"
    return f"/{field_path}"


def _matches_filters(value: Any, values: Iterable[Any]) -> bool:
    return str(value) in {str(v) for v in values}


@dataclass
class HibobMockStore:
    policy_types: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    policy_type_reason_codes: Dict[str, List[Dict[str, Any]]] = field(
        default_factory=dict
    )
    policies: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    policy_type_policies: Dict[str, List[str]] = field(default_factory=dict)
    timeoff_requests: Dict[Tuple[str, int], Dict[str, Any]] = field(
        default_factory=dict
    )
    request_changes: List[Dict[str, Any]] = field(default_factory=list)
    balances: Dict[Tuple[str, str], Dict[str, Any]] = field(default_factory=dict)
    balance_adjustments: List[Dict[str, Any]] = field(default_factory=list)
    attendance_logs: List[Dict[str, Any]] = field(default_factory=list)
    reports: List[Dict[str, Any]] = field(default_factory=list)
    report_runs: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    job_ads: List[Dict[str, Any]] = field(default_factory=list)
    job_profiles: List[Dict[str, Any]] = field(default_factory=list)
    job_roles: List[Dict[str, Any]] = field(default_factory=list)
    job_families: List[Dict[str, Any]] = field(default_factory=list)
    job_family_groups: List[Dict[str, Any]] = field(default_factory=list)
    goals: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    key_results: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    people: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    positions: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    position_openings: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    position_budgets: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    onboarding_wizards: List[Dict[str, Any]] = field(default_factory=list)
    documents: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    company_fields: List[Dict[str, Any]] = field(default_factory=list)
    company_lists: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    custom_tables: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    custom_table_entries: Dict[Tuple[str, str], List[Dict[str, Any]]] = field(
        default_factory=dict
    )
    work_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    employment_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    payroll_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    equity_grants: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    variable_payments: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    training_records: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    bank_accounts: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)

    request_id_seq: count = field(default_factory=lambda: count(1000))
    goal_id_seq: count = field(default_factory=lambda: count(2000))
    key_result_id_seq: count = field(default_factory=lambda: count(3000))
    person_id_seq: count = field(default_factory=lambda: count(100))
    position_id_seq: count = field(default_factory=lambda: count(4000))
    position_opening_id_seq: count = field(default_factory=lambda: count(5000))
    position_budget_id_seq: count = field(default_factory=lambda: count(6000))
    doc_id_seq: count = field(default_factory=lambda: count(7000))
    task_id_seq: count = field(default_factory=lambda: count(1))


STORE = HibobMockStore()


def _seed_store() -> None:
    if STORE.policy_types:
        return

    STORE.policy_types = {
        "Holiday": {
            "name": "Holiday",
            "unit": "days",
            "visibility": "public",
            "description": "Annual holiday allowance",
        },
        "Sick": {
            "name": "Sick",
            "unit": "days",
            "visibility": "private",
            "description": "Paid sick leave",
        },
    }
    STORE.policy_type_reason_codes = {
        "Sick": [
            {"id": 1, "code": "flu", "description": "Flu", "status": "active"},
            {
                "id": 2,
                "code": "mental_health",
                "description": "Mental health day",
                "status": "active",
            },
        ]
    }
    STORE.policies = {
        "Standard Holiday": {
            "name": "Standard Holiday",
            "allowance": 25,
            "maxBalance": 10,
            "minBalance": 0,
            "yosIncrease": [],
            "minTimeOffRequestDuration": "PT1H",
            "bookingWorkDaysOnly": True,
            "approvalRequired": True,
            "description": "Default holiday policy",
            "unit": "days",
        },
        "Sick Leave": {
            "name": "Sick Leave",
            "allowance": 10,
            "maxBalance": 5,
            "minBalance": 0,
            "yosIncrease": [],
            "minTimeOffRequestDuration": "PT1H",
            "bookingWorkDaysOnly": True,
            "approvalRequired": False,
            "description": "Default sick policy",
            "unit": "days",
        },
    }
    STORE.policy_type_policies = {
        "Holiday": ["Standard Holiday"],
        "Sick": ["Sick Leave"],
    }
    STORE.reports = [
        {"id": 1, "name": "Employee Report", "type": "people"},
        {"id": 2, "name": "Time Off Report", "type": "timeoff"},
    ]
    STORE.job_ads = [
        {
            "id": "job-123",
            "applyUrl": "https://example.com/jobs/123",
            "title": "Backend Engineer",
            "departmentId": "eng",
            "department": "Engineering",
            "employmentTypeId": "full-time",
            "employmentType": "Full Time",
            "siteId": "nyc",
            "site": "New York",
            "country": "US",
            "languageCode": "en",
            "description": "Build APIs",
            "requirements": "Python, SQL",
            "responsibilities": "Ship features",
            "benefits": "Health, PTO",
            "postedAt": "2025-01-01",
            "status": "published",
        }
    ]
    STORE.job_profiles = [
        {
            "id": "jp-1",
            "title": "Software Engineer",
            "status": "active",
            "jobRoleId": "jr-1",
            "jobFamilyId": "jf-1",
            "jobFamilyGroupId": "jfg-1",
            "jobLevelRoleId": "jl-1",
        }
    ]
    STORE.job_roles = [{"id": "jr-1", "title": "Engineer"}]
    STORE.job_families = [{"id": "jf-1", "title": "Engineering"}]
    STORE.job_family_groups = [{"id": "jfg-1", "title": "Product & Tech"}]
    STORE.onboarding_wizards = [
        {
            "id": 1,
            "name": "Standard Welcome Wizard",
            "description": "Default onboarding wizard",
            "category": "welcome",
            "isActive": True,
            "isDefault": True,
            "tasks": [{"id": 1, "title": "Complete profile", "type": "form"}],
            "config": {},
            "usageCount": 10,
            "createdBy": "admin",
            "createdAt": "2024-01-15T10:00:00Z",
            "updatedAt": "2024-01-15T10:00:00Z",
        }
    ]
    STORE.company_fields = [
        {
            "id": "work.department",
            "category": "work",
            "categoryId": "work",
            "categoryDisplayName": "Work",
            "name": "Department",
            "description": "Employee department",
            "jsonPath": "work.department",
            "type": "list",
            "typeData": {"listId": "departments"},
            "historical": True,
        }
    ]
    STORE.company_lists = {
        "departments": {
            "name": "Departments",
            "items": [
                {"id": 1, "value": "Engineering", "name": "Engineering", "archived": False, "children": []},
                {"id": 2, "value": "Sales", "name": "Sales", "archived": False, "children": []},
            ],
        },
        "sites": {
            "name": "Sites",
            "items": [
                {"id": 1, "value": "New York", "name": "New York", "archived": False, "children": []},
                {"id": 2, "value": "Remote", "name": "Remote", "archived": False, "children": []},
            ],
        },
    }
    STORE.custom_tables = {
        "1": {
            "id": "1",
            "category": "finance",
            "name": "Expense Allowances",
            "description": "Allowances",
            "columns": [
                {"id": "1", "name": "Type", "mandatory": True, "type": "text", "typeData": None},
                {"id": "2", "name": "Amount", "mandatory": True, "type": "number", "typeData": None},
            ],
        }
    }
    default_people = [
        {
            "firstName": "Nadia",
            "surname": "Kassem",
            "email": "nadia.kassem@duo-marketing.com",
            "title": "Chief Executive Officer",
            "department": "Executive",
        },
        {
            "firstName": "Youssef",
            "surname": "Gad",
            "email": "youssef.gad@duo-marketing.com",
            "title": "Chief Marketing Officer",
            "department": "Marketing",
        },
    ]
    for person in default_people:
        person_id = str(next(STORE.person_id_seq))
        STORE.people[person_id] = {
            "id": person_id,
            "firstName": person["firstName"],
            "surname": person["surname"],
            "displayName": f"{person['firstName']} {person['surname']}",
            "email": person["email"],
            "creationDateTime": _utc_now_iso(),
            "work": {
                "title": person["title"],
                "department": person["department"],
                "site": "New York",
                "startDate": "2025-01-01",
                "isManager": False,
            },
            "about": {"about": "", "superpowers": [], "hobbies": []},
            "root": {"displayName": f"{person['firstName']} {person['surname']}", "avatarUrl": None},
            "lifecycle": {"status": "active"},
            "metadata": {},
        }


_seed_store()


def get_policy_type_names() -> List[str]:
    return list(STORE.policy_types.keys())


def get_policy_type_details(policy_type: str) -> Dict[str, Any]:
    if policy_type not in STORE.policy_types:
        raise ValueError(f"Policy type {policy_type} not found")
    return STORE.policy_types[policy_type]


def get_reason_codes(policy_type: str) -> List[Dict[str, Any]]:
    return STORE.policy_type_reason_codes.get(policy_type, [])


def add_reason_codes(policyType: str, reasonCodes: List[str]) -> Dict[str, Any]:
    if policyType not in STORE.policy_types:
        raise ValueError(f"Policy type {policyType} not found")
    normalized = [code.strip() for code in reasonCodes if code.strip()]
    if len({code.lower() for code in normalized}) != len(normalized):
        raise ValueError("Duplicate reason codes in request")
    existing = STORE.policy_type_reason_codes.setdefault(policyType, [])
    existing_codes = {code["code"].lower() for code in existing}
    new_codes = []
    next_id = max([code["id"] for code in existing], default=0) + 1
    for code in normalized:
        if code.lower() in existing_codes:
            raise ValueError(f"Reason code {code} already exists")
        new_codes.append({"id": next_id, "displayName": code})
        existing.append({"id": next_id, "code": code, "description": code, "status": "active"})
        next_id += 1
    return {"reasonCodes": new_codes}


def get_policies(policyName: str) -> Dict[str, Any]:
    if policyName not in STORE.policies:
        raise ValueError(f"Policy {policyName} not found")
    return STORE.policies[policyName]


def get_policy_names(policy_type: str) -> List[str]:
    if policy_type not in STORE.policy_types:
        raise ValueError(f"Policy type {policy_type} not found")
    return STORE.policy_type_policies.get(policy_type, [])


def submit_timeoff_request(
    id: str,
    requestRangeType: str,
    policyType: str,
    startDate: str,
    endDate: Optional[str] = None,
    startDatePortion: Optional[str] = None,
    endDatePortion: Optional[str] = None,
    hours: Optional[int] = None,
    minutes: Optional[int] = None,
    durations: Optional[List[Dict[str, Any]]] = None,
    dayPortion: Optional[str] = None,
    dailyHours: Optional[int] = None,
    dailyMinutes: Optional[int] = None,
    localStartTime: Optional[str] = None,
    localEndTime: Optional[str] = None,
    skipManagerApproval: bool = False,
    approver: Optional[str] = None,
    description: Optional[str] = None,
    reasonCode: Optional[int] = None,
) -> Dict[str, Any]:
    _parse_date(startDate)
    if requestRangeType != "hours" and endDate is None:
        raise ValueError("endDate is required for this request type")
    if requestRangeType == "days" and (startDatePortion is None or endDatePortion is None):
        raise ValueError("startDatePortion and endDatePortion are required for days")
    if requestRangeType == "hours" and (hours is None or minutes is None or endDate != startDate):
        raise ValueError("hours/minutes required and endDate must equal startDate for hours")
    if requestRangeType in {"differentDayDurations", "differentSpecificHoursDayDurations"} and not durations:
        raise ValueError("durations required for this request type")
    if requestRangeType == "portionOnRange" and dayPortion is None:
        raise ValueError("dayPortion required for portionOnRange")
    if requestRangeType == "hoursOnRange" and (dailyHours is None or dailyMinutes is None):
        raise ValueError("dailyHours/dailyMinutes required for hoursOnRange")
    if requestRangeType == "specificHoursDayDurations" and (localStartTime is None or localEndTime is None):
        raise ValueError("localStartTime/localEndTime required for specificHoursDayDurations")

    request_id = next(STORE.request_id_seq)
    request = {
        "id": id,
        "request_id": request_id,
        "policyType": policyType,
        "requestRangeType": requestRangeType,
        "startDate": startDate,
        "endDate": endDate or startDate,
        "startDatePortion": startDatePortion,
        "endDatePortion": endDatePortion,
        "hours": hours,
        "minutes": minutes,
        "durations": durations,
        "dayPortion": dayPortion,
        "dailyHours": dailyHours,
        "dailyMinutes": dailyMinutes,
        "localStartTime": localStartTime,
        "localEndTime": localEndTime,
        "skipManagerApproval": skipManagerApproval,
        "approver": approver,
        "description": description,
        "reasonCode": reasonCode,
        "status": "Pending",
        "createdAt": _utc_now_iso(),
    }
    STORE.timeoff_requests[(id, request_id)] = request
    STORE.request_changes.append({"type": "Created", "request": request, "changedAt": _utc_now_iso()})
    return {"id": id, "request_id": request_id, "status": "Pending"}


def get_timeoff_request(id: int, request_id: int) -> Dict[str, Any]:
    key = (str(id), request_id)
    if key not in STORE.timeoff_requests:
        raise ValueError("Request not found")
    return STORE.timeoff_requests[key]


def cancel_timeoff_request(id: str, request_id: int) -> Dict[str, Any]:
    key = (id, request_id)
    if key not in STORE.timeoff_requests:
        raise ValueError("Request not found")
    STORE.timeoff_requests[key]["status"] = "Canceled"
    STORE.request_changes.append(
        {"type": "Canceled", "request": STORE.timeoff_requests[key], "changedAt": _utc_now_iso()}
    )
    return {"request_id": request_id}


def get_request_changes(
    since: str,
    to: Optional[str] = None,
    includePending: bool = False,
) -> Dict[str, Any]:
    start = _parse_date(since)
    end = _parse_date(to) if to else date.today()
    changes = [
        change
        for change in STORE.request_changes
        if start <= _parse_date(change["request"]["startDate"]) <= end
    ]
    if includePending:
        return {"changes": changes}
    filtered = [change for change in changes if change["request"]["status"] != "Pending"]
    return {"changes": filtered}


def get_whosout(
    from_: str,
    to: str,
    includeHourly: bool = False,
    includePrivate: bool = False,
    includePending: bool = False,
    includeWorkingRequests: bool = True,
    include_private: Optional[bool] = None,
) -> Dict[str, Any]:
    start = _parse_date(from_)
    end = _parse_date(to)
    outs = []
    for request in STORE.timeoff_requests.values():
        req_start = _parse_date(request["startDate"])
        req_end = _parse_date(request["endDate"])
        if req_end < start or req_start > end:
            continue
        if not includePending and request["status"] == "Pending":
            continue
        outs.append(request)
    return {"outs": outs}


def get_out_today(
    today: Optional[str] = None,
    includeHourly: bool = False,
    includePrivate: bool = False,
    siteId: Optional[int] = None,
) -> Dict[str, Any]:
    target = _parse_date(today) if today else date.today()
    outs = []
    for request in STORE.timeoff_requests.values():
        req_start = _parse_date(request["startDate"])
        req_end = _parse_date(request["endDate"])
        if req_start <= target <= req_end:
            outs.append(request)
    return {"outs": outs}


def get_balance(id: str, policyType: str, date: str) -> Dict[str, Any]:
    key = (id, policyType)
    if key not in STORE.balances:
        STORE.balances[key] = {
            "employeeId": id,
            "totalBalanceAsOfDate": 10,
            "totalRoundedBalanceAsOfDate": 10,
            "pointInTime": date,
            "startingBalance": 10,
            "startingBalanceAsOf": date,
            "totalTaken": 0,
            "totalAdminAdjustments": 0,
            "totalSystemAdjustments": 0,
            "annualAllowance": 10,
            "policy": policyType,
        }
    return STORE.balances[key]


def create_balance_adjustment(
    id: str,
    adjustmentType: str,
    policyType: str,
    effectiveDate: str,
    amount: float,
    reason: str,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.balance_adjustments) + 1,
        "employeeId": id,
        "adjustmentType": adjustmentType,
        "policyType": policyType,
        "effectiveDate": effectiveDate,
        "amount": amount,
        "reason": reason,
    }
    STORE.balance_adjustments.append(entry)
    balance = get_balance(id=id, policyType=policyType, date=effectiveDate)
    balance["totalBalanceAsOfDate"] += amount
    return {"id": entry["id"], "msg": "Success"}


def import_attendance_data(
    importMethod: str,
    idType: str,
    requests: List[Dict[str, Any]],
    dateTimeFormat: Optional[str] = None,
) -> Dict[str, Any]:
    STORE.attendance_logs.extend(requests)
    total = sum(1 for r in requests if r.get("clockIn")) + sum(
        1 for r in requests if r.get("clockOut")
    )
    return {"status": "success", "total": total, "imported": total, "notImported": 0, "errors": []}


def read_company_reports() -> Dict[str, Any]:
    return {"success": True, "reports": STORE.reports}


def download_report_by_id(
    reportId: int,
    format: str = "csv",
    includeInfo: bool = False,
    locale: Optional[str] = None,
    humanReadable: Optional[str] = None,
) -> Dict[str, Any]:
    report = next((r for r in STORE.reports if r["id"] == reportId), None)
    if not report:
        raise ValueError("Report not found")
    return {
        "reportId": reportId,
        "format": format,
        "includeInfo": includeInfo,
        "downloadUrl": f"https://example.com/reports/{reportId}.{format}",
    }


def generate_company_report_async(
    reportId: int,
    format: str = "csv",
    includeInfo: bool = False,
    locale: Optional[str] = None,
    humanReadable: Optional[str] = None,
) -> Dict[str, Any]:
    return {"status": "ready", "downloadUrl": f"https://example.com/reports/{reportId}.{format}"}


def download_report_by_name(reportName: str) -> Dict[str, Any]:
    report = next((r for r in STORE.reports if r["name"] == reportName), None)
    if not report:
        raise ValueError("Report not found")
    return {"success": True, "run": {"reportId": report["id"], "downloadUrl": f"https://example.com/reports/{report['id']}.csv"}}


def read_all_active_job_ads(preferredLanguage: str = "en", fields: Optional[List[str]] = None, filters: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    active_ads = [ad for ad in STORE.job_ads if ad.get("status") == "published"]
    if not fields:
        return {"success": True, "count": len(active_ads), "job_ads": active_ads}
    filtered_ads = []
    for ad in active_ads:
        filtered_ads.append({field.replace("/jobAd/", ""): ad.get(field.replace("/jobAd/", "")) for field in fields})
    return {"success": True, "count": len(filtered_ads), "job_ads": filtered_ads}


def read_job_ads_by_id(id: str, preferredLanguage: str = "en") -> Dict[str, Any]:
    ad = next((ad for ad in STORE.job_ads if ad["id"] == id), None)
    if not ad:
        raise ValueError("Job ad not found")
    return {"success": True, "job_ad": ad}


def read_company_job_profiles(
    fields: List[str],
    filters: List[Dict[str, Any]],
    pagination: Optional[Dict[str, Any]] = None,
    includeHumanReadable: bool = True,
) -> Dict[str, Any]:
    results = []
    for profile in STORE.job_profiles:
        entry = {}
        for field_id in fields:
            key = field_id.replace("/jobProfile/", "")
            entry[field_id] = profile.get(key)
        results.append(entry)
    return {"items": results, "response_metadata": {"cursor": None}}


def get_all_job_roles(
    cursor: Optional[str] = None, limit: int = 100, includeHumanReadable: bool = False
) -> Dict[str, Any]:
    return {"items": STORE.job_roles[:limit], "response_metadata": {"cursor": None}}


def get_all_job_families(
    cursor: Optional[str] = None, limit: int = 100, includeHumanReadable: bool = False
) -> Dict[str, Any]:
    return {"items": STORE.job_families[:limit], "response_metadata": {"cursor": None}}


def get_all_job_family_groups(
    cursor: Optional[str] = None, limit: int = 100, includeHumanReadable: bool = False
) -> Dict[str, Any]:
    return {"items": STORE.job_family_groups[:limit], "response_metadata": {"cursor": None}}


def get_job_profiles_metadata() -> Dict[str, Any]:
    return {"fields": ["/jobProfile/id", "/jobProfile/title", "/jobProfile/status"]}


def get_job_roles_metadata() -> Dict[str, Any]:
    return {"fields": ["/jobRole/id", "/jobRole/title"]}


def get_job_families_metadata() -> Dict[str, Any]:
    return {"fields": ["/jobFamily/id", "/jobFamily/title"]}


def get_job_family_groups_metadata() -> Dict[str, Any]:
    return {"fields": ["/jobFamilyGroup/id", "/jobFamilyGroup/title"]}


def get_goal_type_metadata() -> Dict[str, Any]:
    return {"items": [{"id": 1, "name": "Company Goal"}, {"id": 2, "name": "Team Goal"}]}


def get_goals_metadata() -> Dict[str, Any]:
    return {"metadata": [{"id": "title"}, {"id": "status"}]}


def get_key_results_metadata() -> Dict[str, Any]:
    return {"metadata": [{"id": "title"}, {"id": "measureType"}]}


def search_goal_types(
    fields: List[str],
    filters: Optional[List[Dict[str, Any]]] = None,
    limit: int = 50,
    cursor: str = "0",
) -> Dict[str, Any]:
    items = [
        {"objectType": "goalType", "fields": {field: {"value": "mock"} for field in fields}}
    ]
    return {"items": items, "responseMetadata": {"totalCount": 1, "pageSize": limit}, "nextCursor": None, "errors": {}}


def search_goals(
    fields: List[str],
    filters: Optional[List[Dict[str, Any]]] = None,
    limit: int = 25,
    cursor: str = "0",
) -> Dict[str, Any]:
    items = []
    for goal_id, goal in STORE.goals.items():
        entry = {"objectType": "goal", "fields": {}}
        for field in fields:
            entry["fields"][field] = {"value": goal.get(field)}
        items.append(entry)
    return {"items": items, "responseMetadata": {"totalCount": len(items), "pageSize": limit}, "nextCursor": None, "errors": []}


def search_key_results(
    fields: List[str],
    filters: List[Dict[str, Any]],
    limit: int = 50,
    cursor: Optional[str] = "0",
) -> Dict[str, Any]:
    items = []
    for key_result_id, key_result in STORE.key_results.items():
        entry = {"objectType": "keyResult", "fields": {}}
        for field in fields:
            entry["fields"][field] = {"value": key_result.get(field)}
        items.append(entry)
    return {"items": items, "responseMetadata": {"totalCount": len(items), "pageSize": limit}, "nextCursor": None, "errors": []}


def create_goals(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    goal_ids = []
    for item in items:
        goal_id = next(STORE.goal_id_seq)
        fields = item.get("fields", {})
        STORE.goals[goal_id] = {key: value.get("value") for key, value in fields.items()}
        STORE.goals[goal_id]["id"] = goal_id
        goal_ids.append(goal_id)
    return {"goalIds": goal_ids}


def update_goal_status(goalId: int, status: str, comment: Optional[str] = None) -> Dict[str, Any]:
    if goalId not in STORE.goals:
        raise ValueError("Goal not found")
    STORE.goals[goalId]["status"] = status
    STORE.goals[goalId]["statusComment"] = comment
    return STORE.goals[goalId]


def update_goal(goalId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if goalId not in STORE.goals:
        raise ValueError("Goal not found")
    fields = items[0].get("fields", {})
    for key, value in fields.items():
        STORE.goals[goalId][key] = value.get("value")
    return {"success": True, "goalId": goalId}


def delete_goal(goalId: int) -> Dict[str, Any]:
    STORE.goals.pop(goalId, None)
    return {"detail": "deleted"}


def create_key_results(goalId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if goalId not in STORE.goals:
        raise ValueError("Goal not found")
    for item in items:
        key_result_id = next(STORE.key_result_id_seq)
        fields = item.get("fields", {})
        STORE.key_results[key_result_id] = {key: value.get("value") for key, value in fields.items()}
        STORE.key_results[key_result_id]["id"] = key_result_id
        STORE.key_results[key_result_id]["goalId"] = goalId
    return {"success": True}


def update_key_results_progress(
    goalId: int, keyResults: List[Dict[str, Any]], comment: Optional[str] = None
) -> Dict[str, Any]:
    for entry in keyResults:
        key_result_id = entry["keyResultId"]
        if key_result_id in STORE.key_results:
            STORE.key_results[key_result_id]["currentValue"] = entry["currentValue"]
            STORE.key_results[key_result_id]["comment"] = comment
    return {"success": True}


def update_key_results_details(goalId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    for item in items:
        fields = item.get("fields", {})
        key_result_id = fields.get("keyResultId", {}).get("value")
        if key_result_id and key_result_id in STORE.key_results:
            for key, value in fields.items():
                if key != "keyResultId":
                    STORE.key_results[key_result_id][key] = value.get("value")
    return {"success": True}


def delete_key_result(goalId: int, keyResultId: int) -> Dict[str, Any]:
    STORE.key_results.pop(keyResultId, None)
    return {"detail": "deleted"}


def people_search(
    fields: Optional[List[str]] = None,
    filters: Optional[List[Dict[str, Any]]] = None,
    showInactive: bool = False,
    humanReadable: str = "",
) -> Dict[str, Any]:
    results = []
    for employee in STORE.people.values():
        if filters:
            allowed = True
            for filter_entry in filters:
                field_path = filter_entry.get("fieldPath")
                values = filter_entry.get("values", [])
                if field_path == "root.id" and not _matches_filters(employee["id"], values):
                    allowed = False
                if field_path == "root.email" and not _matches_filters(employee["email"], values):
                    allowed = False
            if not allowed:
                continue
        if not fields:
            results.append(employee)
        else:
            entry: Dict[str, Any] = {}
            for field_path in fields:
                normalized = _normalize_field_path(field_path)
                key = normalized.strip("/")
                parts = key.split("/")
                if parts[0] in employee and len(parts) > 1:
                    entry[normalized] = {"value": employee[parts[0]].get(parts[1])}
                else:
                    entry[normalized] = {"value": employee.get(parts[-1])}
            results.append(entry)
    return {"employees": results}


def read_by_identifier(identifier: str, fields: Optional[List[str]] = None, humanReadable: str = "") -> Dict[str, Any]:
    employee = next(
        (person for person in STORE.people.values() if person["id"] == identifier or person["email"] == identifier),
        None,
    )
    if not employee:
        raise ValueError("Employee not found")
    if not fields:
        return {"employees": [employee]}
    entry: Dict[str, Any] = {}
    for field_path in fields:
        normalized = _normalize_field_path(field_path)
        key = normalized.strip("/")
        parts = key.split("/")
        if parts[0] in employee and len(parts) > 1:
            entry[normalized] = {"value": employee[parts[0]].get(parts[1])}
        else:
            entry[normalized] = {"value": employee.get(parts[-1])}
    entry.update({"id": employee["id"], "fullName": employee["displayName"], "email": employee["email"]})
    return {"employees": [entry]}


def update_by_identifier(
    identifier: Dict[str, str],
    firstName: Optional[str] = None,
    surname: Optional[str] = None,
    displayName: Optional[str] = None,
    email: Optional[str] = None,
    personal: Optional[Dict[str, Any]] = None,
    root: Optional[Dict[str, Any]] = None,
    about: Optional[Dict[str, Any]] = None,
    work: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    person_id = identifier.get("id")
    if not person_id or person_id not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[person_id]
    if firstName:
        employee["firstName"] = firstName
    if surname:
        employee["surname"] = surname
    if displayName:
        employee["displayName"] = displayName
    if email:
        employee["email"] = email
    if personal:
        employee.setdefault("personal", {}).update(personal)
    if root:
        employee.setdefault("root", {}).update(root)
    if about:
        employee.setdefault("about", {}).update(about)
    if work:
        employee.setdefault("work", {}).update(work)
    return {"employees": [employee]}


def get_profiles() -> Dict[str, Any]:
    return {"employees": list(STORE.people.values())}


def create_person(
    email: str,
    firstName: str,
    surname: str,
    work: Dict[str, Any],
    displayName: Optional[str] = None,
    lifecycle: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    root: Optional[Dict[str, Any]] = None,
    about: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if any(person["email"] == email for person in STORE.people.values()):
        raise ValueError("Email already exists")
    person_id = str(next(STORE.person_id_seq))
    employee = {
        "id": person_id,
        "firstName": firstName,
        "surname": surname,
        "displayName": displayName or f"{firstName} {surname}",
        "email": email,
        "creationDateTime": _utc_now_iso(),
        "work": work,
        "about": about or {},
        "root": root or {"displayName": displayName or f"{firstName} {surname}", "avatarUrl": None},
        "lifecycle": lifecycle or {"status": "active"},
        "metadata": metadata or {},
    }
    STORE.people[person_id] = employee
    return employee


def invite_employee(employeeId: int, welcomeWizardId: int) -> Dict[str, Any]:
    person_id = str(employeeId)
    if person_id not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[person_id]
    if employee.get("lifecycle", {}).get("status") == "invited":
        raise ValueError(f"Person with ID {employeeId} is already invited")
    employee.setdefault("lifecycle", {})["status"] = "invited"
    employee["lifecycle"]["invitedAt"] = _utc_now_iso()
    employee["lifecycle"]["welcomeWizardId"] = welcomeWizardId
    employee["lifecycle"]["invitedBy"] = "service_user:1"
    return {"employees": [employee]}


def uninvite_employee(identifier: str, reason: Optional[str] = None) -> Dict[str, Any]:
    if identifier not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[identifier]
    if employee.get("lifecycle", {}).get("status") == "invitation_revoked":
        raise ValueError(f"Person with ID {identifier} is already uninvited")
    employee.setdefault("lifecycle", {})["status"] = "invitation_revoked"
    employee["lifecycle"]["uninvitedAt"] = _utc_now_iso()
    employee["lifecycle"]["uninviteReason"] = reason
    employee["lifecycle"]["uninvitedBy"] = "service_user:1"
    return {"employees": [employee]}


def terminate_employee(
    identifier: str,
    terminationDate: str,
    noticePeriod: Optional[Dict[str, Any]] = None,
    lastDayOfWork: Optional[str] = None,
    terminationReason: Optional[str] = None,
    reasonType: Optional[str] = None,
) -> Dict[str, Any]:
    if identifier not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[identifier]
    if employee.get("lifecycle", {}).get("status") == "terminated":
        raise ValueError(f"Person with ID {identifier} is already terminated")
    term_date = _parse_date(terminationDate)
    if term_date <= date.today():
        raise ValueError("terminationDate must be in the future")
    if lastDayOfWork and lastDayOfWork != terminationDate:
        raise ValueError("lastDayOfWork must be equal to terminationDate")
    lifecycle = employee.setdefault("lifecycle", {})
    lifecycle.update(
        {
            "status": "terminated",
            "terminationDate": terminationDate,
            "terminatedAt": _utc_now_iso(),
            "terminationReason": terminationReason,
            "reasonType": reasonType,
            "terminatedBy": "service_user:1",
        }
    )
    if noticePeriod:
        lifecycle["noticePeriod"] = noticePeriod
    if lastDayOfWork:
        lifecycle["lastDayOfWork"] = lastDayOfWork
    return {"employees": [employee]}


def set_start_date(employeeId: int, startDate: str, reason: Optional[str] = None) -> Dict[str, Any]:
    person_id = str(employeeId)
    if person_id not in STORE.people:
        raise ValueError("Employee not found")
    start_date = _parse_date(startDate)
    if start_date < date.today():
        raise ValueError("startDate must be today or future")
    employee = STORE.people[person_id]
    employee.setdefault("work", {})["startDate"] = startDate
    employee["work"].setdefault("originalStartDate", startDate)
    employee["work"]["activeEffectiveDate"] = startDate
    if reason:
        employee["work"]["startDateReason"] = reason
    return {"employees": [employee]}


def get_avatar_by_email(email: str) -> Dict[str, Any]:
    employee = next((person for person in STORE.people.values() if person["email"] == email), None)
    if not employee:
        raise ValueError("Employee not found")
    return {"email": email, "avatarUrl": employee.get("root", {}).get("avatarUrl"), "employeeId": employee["id"]}


def get_avatar_by_id(employeeId: int) -> Dict[str, Any]:
    person_id = str(employeeId)
    if person_id not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[person_id]
    return {"employeeId": employee["id"], "email": employee["email"], "avatarUrl": employee.get("root", {}).get("avatarUrl")}


def upload_avatar_by_url(employeeId: int, url: str) -> Dict[str, Any]:
    person_id = str(employeeId)
    if person_id not in STORE.people:
        raise ValueError("Employee not found")
    employee = STORE.people[person_id]
    employee.setdefault("root", {})["avatarUrl"] = url
    return {"employees": [employee]}


def update_employee_email(id: int, email: str) -> Dict[str, Any]:
    person_id = str(id)
    if person_id not in STORE.people:
        raise ValueError("Employee not found")
    if any(person["email"] == email for person in STORE.people.values()):
        raise ValueError("Email already in use")
    employee = STORE.people[person_id]
    employee["email"] = email
    return {"employees": [employee]}


def get_all_positions_fields() -> Dict[str, Any]:
    return {"success": True, "count": 3, "fields": [{"id": "position.id", "name": "Position ID", "type": "number", "required": True, "description": "Position identifier"}]}


def get_all_position_openings_fields() -> Dict[str, Any]:
    return {"fields": [{"id": "position_opening.id", "name": "Position Opening ID", "type": "number", "description": "Opening identifier"}]}


def get_all_position_budget_fields() -> Dict[str, Any]:
    return {"fields": [{"id": "position_budget.id", "name": "Position Budget ID", "type": "number", "description": "Budget identifier"}]}


def read_company_positions(
    fields: List[str],
    filters: Optional[List[Dict[str, Any]]] = None,
    includeHumanReadable: bool = False,
) -> Dict[str, Any]:
    results = []
    for position in STORE.positions.values():
        entry = {}
        for field_id in fields:
            key = field_id.replace("/position/", "")
            entry[field_id] = {"value": position.get(key)}
        results.append(entry)
    return {"positions": results}


def read_position_openings(
    fields: List[str],
    filters: Optional[List[Dict[str, Any]]] = None,
    includeHumanReadable: bool = False,
    pagination: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    results = []
    for opening in STORE.position_openings.values():
        entry = {}
        for field_id in fields:
            key = field_id.replace("/positionOpening/", "")
            entry[field_id] = {"value": opening.get(key)}
        results.append(entry)
    return {"positionOpenings": results, "next_cursor": None}


def read_position_budgets(
    fields: List[str],
    filters: Optional[List[Dict[str, Any]]] = None,
    includeHumanReadable: bool = False,
    pagination: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    results = []
    for budget in STORE.position_budgets.values():
        entry = {}
        for field_id in fields:
            key = field_id.replace("/positionBudget/", "")
            entry[field_id] = {"value": budget.get(key)}
        results.append(entry)
    return {"positionBudgets": results, "next_cursor": None}


def create_positions(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    created = []
    for item in items:
        position_id = next(STORE.position_id_seq)
        fields = item.get("fields", {})
        position = {"id": position_id}
        for key, value in fields.items():
            if key.startswith("/position/"):
                position[key.replace("/position/", "")] = value.get("value")
        STORE.positions[position_id] = position
        created.append(position_id)
    return {"positionIds": created}


def create_position_openings(positionId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if positionId not in STORE.positions:
        raise ValueError("Position not found")
    created = []
    for item in items:
        opening_id = next(STORE.position_opening_id_seq)
        fields = item.get("fields", {})
        opening = {"id": opening_id, "positionId": positionId}
        for key, value in fields.items():
            opening[key.replace("/positionOpening/", "")] = value.get("value")
        STORE.position_openings[opening_id] = opening
        created.append(opening_id)
    return {"positionOpeningIds": created}


def update_position(positionId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if positionId not in STORE.positions:
        raise ValueError("Position not found")
    fields = items[0].get("fields", {})
    for key, value in fields.items():
        STORE.positions[positionId][key.replace("/position/", "")] = value.get("value")
    return {"positionId": positionId}


def update_position_opening(
    positionId: int, positionOpeningId: int, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    if positionOpeningId not in STORE.position_openings:
        raise ValueError("Position opening not found")
    fields = items[0].get("fields", {})
    for key, value in fields.items():
        STORE.position_openings[positionOpeningId][key.replace("/positionOpening/", "")] = value.get("value")
    return {"positionOpeningId": positionOpeningId}


def delete_position_opening(positionId: int, positionOpeningId: int) -> Dict[str, Any]:
    STORE.position_openings.pop(positionOpeningId, None)
    return {"positionOpeningId": positionOpeningId}


def create_position_budget(positionId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if positionId not in STORE.positions:
        raise ValueError("Position not found")
    budget_id = next(STORE.position_budget_id_seq)
    fields = items[0].get("fields", {})
    budget = {"id": budget_id, "positionId": positionId}
    for key, value in fields.items():
        budget[key.replace("/positionBudget/", "")] = value.get("value")
    STORE.position_budgets[budget_id] = budget
    return {"positionBudgetId": budget_id}


def update_position_budget(positionId: int, positionBudgetId: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if positionBudgetId not in STORE.position_budgets:
        raise ValueError("Budget not found")
    fields = items[0].get("fields", {})
    for key, value in fields.items():
        STORE.position_budgets[positionBudgetId][key.replace("/positionBudget/", "")] = value.get("value")
    return {"positionBudgetId": positionBudgetId}


def cancel_position(positionId: int) -> Dict[str, Any]:
    if positionId not in STORE.positions:
        raise ValueError("Position not found")
    STORE.positions[positionId]["status"] = "cancelled"
    return {"positionId": positionId}


def get_onboarding_wizards(active_only: bool = False) -> Dict[str, Any]:
    if active_only:
        return {"wizards": [w for w in STORE.onboarding_wizards if w.get("isActive")], "total": len(STORE.onboarding_wizards)}
    return {"wizards": STORE.onboarding_wizards, "total": len(STORE.onboarding_wizards)}


def get_bulk_people_work(limit: int = 50, cursor: Optional[str] = None, employeeIds: Optional[str] = None) -> Dict[str, Any]:
    ids = employeeIds.split(",") if employeeIds else list(STORE.people.keys())
    results = []
    for person_id in ids[:limit]:
        for entry in STORE.work_history.get(person_id, []):
            results.append(entry)
    return {"results": results, "response_metadata": {"cursor": None}, "errors": []}


def get_bulk_lifecycle_history(limit: int = 50, cursor: Optional[str] = None, employeeIds: Optional[str] = None) -> Dict[str, Any]:
    ids = employeeIds.split(",") if employeeIds else list(STORE.people.keys())
    results = []
    for person_id in ids[:limit]:
        employee = STORE.people.get(person_id)
        if employee:
            results.append({"employeeId": person_id, "values": employee.get("lifecycle", {})})
    return {"results": results, "response_metadata": {"cursor": None}, "errors": []}


def get_bulk_employment_history(limit: int = 50, cursor: Optional[str] = None, employeeIds: Optional[str] = None) -> Dict[str, Any]:
    ids = employeeIds.split(",") if employeeIds else list(STORE.people.keys())
    results = []
    for person_id in ids[:limit]:
        results.extend(STORE.employment_history.get(person_id, []))
    return {"results": results, "response_metadata": {"cursor": None}, "errors": []}


def get_bulk_payroll_history(limit: int = 50, cursor: Optional[str] = None, employeeIds: Optional[str] = None) -> Dict[str, Any]:
    ids = employeeIds.split(",") if employeeIds else list(STORE.people.keys())
    results = []
    for person_id in ids[:limit]:
        results.extend(STORE.payroll_history.get(person_id, []))
    return {"results": results, "response_metadata": {"cursor": None}, "errors": []}


def search_actual_payments(filters: List[Dict[str, Any]], pagination: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {"results": [], "response_metadata": {"cursor": None}}


def get_employee_work_history(id: str) -> Dict[str, Any]:
    return {"values": STORE.work_history.get(id, [])}


def create_employee_work_entry(
    id: str,
    effectiveDate: str,
    site: Optional[str] = None,
    siteId: Optional[int] = None,
    title: Optional[str] = None,
    department: Optional[str] = None,
    reason: Optional[str] = None,
    reportsTo: Optional[Dict[str, Any]] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.work_history.get(id, [])) + 1,
        "effectiveDate": effectiveDate,
        "site": site,
        "siteId": siteId,
        "title": title,
        "department": department,
        "reason": reason,
        "reportsTo": reportsTo,
        "customColumns": customColumns or {},
    }
    STORE.work_history.setdefault(id, []).append(entry)
    return {"values": [entry]}


def update_employee_work_entry(
    id: str,
    entry_id: int,
    effectiveDate: str,
    title: Optional[str] = None,
    department: Optional[str] = None,
    site: Optional[str] = None,
    siteId: Optional[int] = None,
    workChangeType: Optional[str] = None,
    reason: Optional[str] = None,
    reportsTo: Optional[Dict[str, Any]] = None,
    customColumns: Optional[Dict[str, Any]] = None,
    patchUpdate: bool = False,
) -> Dict[str, Any]:
    entries = STORE.work_history.get(id, [])
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        raise ValueError("Entry not found")
    if patchUpdate:
        updates = {
            "effectiveDate": effectiveDate,
            "title": title,
            "department": department,
            "site": site,
            "siteId": siteId,
            "workChangeType": workChangeType,
            "reason": reason,
            "reportsTo": reportsTo,
            "customColumns": customColumns,
        }
        for key, value in updates.items():
            if value is not None:
                entry[key] = value
    else:
        entry.update(
            {
                "effectiveDate": effectiveDate,
                "title": title,
                "department": department,
                "site": site,
                "siteId": siteId,
                "workChangeType": workChangeType,
                "reason": reason,
                "reportsTo": reportsTo,
                "customColumns": customColumns or {},
            }
        )
    return {"values": [entry]}


def delete_employee_work_entry(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.work_history.get(id, [])
    STORE.work_history[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted entry {entry_id} for employee {id}"}


def get_employee_employment_history(id: str) -> Dict[str, Any]:
    return {"values": STORE.employment_history.get(id, [])}


def create_employee_employment_entry(
    id: str,
    effectiveDate: str,
    reason: Optional[str] = None,
    personalWorkingPatternType: Optional[str] = None,
    contract: Optional[str] = None,
    type: Optional[str] = None,
    salaryPayType: Optional[str] = None,
    flsaCode: Optional[str] = None,
    weeklyHours: Optional[float] = None,
    fte: Optional[float] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.employment_history.get(id, [])) + 1,
        "effectiveDate": effectiveDate,
        "reason": reason,
        "personalWorkingPatternType": personalWorkingPatternType,
        "contract": contract,
        "type": type,
        "salaryPayType": salaryPayType,
        "flsaCode": flsaCode,
        "weeklyHours": weeklyHours,
        "fte": fte,
        "customColumns": customColumns or {},
    }
    STORE.employment_history.setdefault(id, []).append(entry)
    return {"values": [entry]}


def update_employee_employment_entry(
    id: str,
    entry_id: int,
    effectiveDate: str,
    reason: Optional[str] = None,
    personalWorkingPatternType: Optional[str] = None,
    actualWorkingPattern: Optional[Dict[str, Any]] = None,
    contract: Optional[str] = None,
    type: Optional[str] = None,
    salaryPayType: Optional[str] = None,
    flsaCode: Optional[str] = None,
    weeklyHours: Optional[float] = None,
    fte: Optional[float] = None,
    calendarName: Optional[str] = None,
    calendarId: Optional[int] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entries = STORE.employment_history.get(id, [])
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        raise ValueError("Entry not found")
    entry.update(
        {
            "effectiveDate": effectiveDate,
            "reason": reason,
            "personalWorkingPatternType": personalWorkingPatternType,
            "actualWorkingPattern": actualWorkingPattern,
            "contract": contract,
            "type": type,
            "salaryPayType": salaryPayType,
            "flsaCode": flsaCode,
            "weeklyHours": weeklyHours,
            "fte": fte,
            "calendarName": calendarName,
            "calendarId": calendarId,
            "customColumns": customColumns or {},
        }
    )
    return {"values": [entry]}


def delete_employee_employment_entry(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.employment_history.get(id, [])
    STORE.employment_history[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted entry {entry_id} for employee {id}"}


def get_employee_lifecycle_history(id: str) -> Dict[str, Any]:
    employee = STORE.people.get(id, {})
    return {"values": [employee.get("lifecycle", {})]}


def get_employee_payroll_history(id: str) -> Dict[str, Any]:
    return {"values": STORE.payroll_history.get(id, [])}


def create_employee_salary_entry(
    id: str,
    base: Dict[str, Any],
    payPeriod: str,
    effectiveDate: Optional[str] = None,
    payFrequency: Optional[str] = None,
    workChangeType: Optional[str] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.payroll_history.get(id, [])) + 1,
        "base": base,
        "payPeriod": payPeriod,
        "effectiveDate": effectiveDate or _utc_now_iso(),
        "payFrequency": payFrequency,
        "workChangeType": workChangeType,
        "customColumns": customColumns or {},
    }
    STORE.payroll_history.setdefault(id, []).append(entry)
    return {"values": [entry]}


def delete_employee_salary_entry(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.payroll_history.get(id, [])
    STORE.payroll_history[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted salary entry {entry_id} for employee {id}"}


def get_payroll_history(department: Optional[str] = None, showInactive: bool = False) -> Dict[str, Any]:
    return {"employees": list(STORE.people.values())}


def get_employee_equity_grants(id: str) -> Dict[str, Any]:
    return {"values": STORE.equity_grants.get(id, [])}


def create_employee_equity_grant(
    id: str,
    effectiveDate: str,
    quantity: float,
    equityType: str,
    grantType: Optional[str] = None,
    grantNumber: Optional[str] = None,
    grantDate: Optional[str] = None,
    grantStatus: Optional[str] = None,
    exercisePrice: Optional[Dict[str, Any]] = None,
    vestingCommencementDate: Optional[str] = None,
    vestingTerm: Optional[str] = None,
    vestingSchedule: Optional[int] = None,
    optionExpiration: Optional[str] = None,
    reason: Optional[str] = None,
    consentNumber: Optional[str] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.equity_grants.get(id, [])) + 1,
        "effectiveDate": effectiveDate,
        "quantity": quantity,
        "equityType": equityType,
        "grantType": grantType,
        "grantNumber": grantNumber,
        "grantDate": grantDate,
        "grantStatus": grantStatus,
        "exercisePrice": exercisePrice,
        "vestingCommencementDate": vestingCommencementDate,
        "vestingTerm": vestingTerm,
        "vestingSchedule": vestingSchedule,
        "optionExpiration": optionExpiration,
        "reason": reason,
        "consentNumber": consentNumber,
        "customColumns": customColumns or {},
    }
    STORE.equity_grants.setdefault(id, []).append(entry)
    return {"values": [entry]}


def update_employee_equity_grant(
    id: str,
    entry_id: int,
    effectiveDate: str,
    equityType: str,
    quantity: float,
    grantType: Optional[str] = None,
    grantNumber: Optional[int] = None,
    grantDate: Optional[str] = None,
    grantStatus: Optional[str] = None,
    exercisePrice: Optional[Dict[str, Any]] = None,
    vestingCommencementDate: Optional[str] = None,
    vestingTerm: Optional[str] = None,
    vestingSchedule: Optional[int] = None,
    vestedQuantity: Optional[float] = None,
    optionExpiration: Optional[str] = None,
    reason: Optional[str] = None,
    consentNumber: Optional[str] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entries = STORE.equity_grants.get(id, [])
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        raise ValueError("Equity grant entry not found")
    entry.update(
        {
            "effectiveDate": effectiveDate,
            "equityType": equityType,
            "quantity": quantity,
            "grantType": grantType,
            "grantNumber": grantNumber,
            "grantDate": grantDate,
            "grantStatus": grantStatus,
            "exercisePrice": exercisePrice,
            "vestingCommencementDate": vestingCommencementDate,
            "vestingTerm": vestingTerm,
            "vestingSchedule": vestingSchedule,
            "vestedQuantity": vestedQuantity,
            "optionExpiration": optionExpiration,
            "reason": reason,
            "consentNumber": consentNumber,
            "customColumns": customColumns or {},
        }
    )
    return {"values": [entry]}


def delete_employee_equity_grant(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.equity_grants.get(id, [])
    STORE.equity_grants[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted equity entry {entry_id} for employee {id}"}


def get_employee_variable_payments(id: str) -> Dict[str, Any]:
    return {"values": STORE.variable_payments.get(id, [])}


def create_employee_variable_payment(
    id: str,
    effectiveDate: str,
    amount: Dict[str, Any],
    variableType: str,
    paymentPeriod: str,
    companyPercent: Optional[float] = None,
    departmentPercent: Optional[float] = None,
    individualPercent: Optional[float] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.variable_payments.get(id, [])) + 1,
        "effectiveDate": effectiveDate,
        "amount": amount,
        "variableType": variableType,
        "paymentPeriod": paymentPeriod,
        "companyPercent": companyPercent,
        "departmentPercent": departmentPercent,
        "individualPercent": individualPercent,
        "reason": reason,
    }
    STORE.variable_payments.setdefault(id, []).append(entry)
    return {"values": [entry]}


def delete_employee_variable_payment(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.variable_payments.get(id, [])
    STORE.variable_payments[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted variable payment {entry_id} for employee {id}"}


def get_employee_training_records(id: str) -> Dict[str, Any]:
    return {"values": STORE.training_records.get(id, [])}


def create_employee_training_record(
    id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    cost: Optional[Dict[str, Any]] = None,
    status: Optional[str] = None,
    frequency: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    documentId: Optional[int] = None,
    customColumns: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.training_records.get(id, [])) + 1,
        "name": name,
        "description": description,
        "cost": cost,
        "status": status,
        "frequency": frequency,
        "startDate": startDate,
        "endDate": endDate,
        "documentId": documentId,
        "customColumns": customColumns or {},
    }
    STORE.training_records.setdefault(id, []).append(entry)
    return {"values": [entry]}


def delete_employee_training_record(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.training_records.get(id, [])
    STORE.training_records[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted training record {entry_id} for employee {id}"}


def get_employee_bank_accounts(id: str) -> Dict[str, Any]:
    return {"values": STORE.bank_accounts.get(id, [])}


def create_employee_bank_account(
    id: str,
    bankAccountType: str,
    accountNumber: str,
    bankName: str,
    branchAddress: str,
    routingNumber: Optional[str] = None,
    accountNickname: Optional[str] = None,
    bicOrSwift: Optional[str] = None,
    iban: Optional[str] = None,
    allocation: Optional[str] = None,
    amount: Optional[float] = None,
    useForBonus: Optional[bool] = None,
) -> Dict[str, Any]:
    entry = {
        "id": len(STORE.bank_accounts.get(id, [])) + 1,
        "bankAccountType": bankAccountType,
        "accountNumber": accountNumber,
        "bankName": bankName,
        "branchAddress": branchAddress,
        "routingNumber": routingNumber,
        "accountNickname": accountNickname,
        "bicOrSwift": bicOrSwift,
        "iban": iban,
        "allocation": allocation,
        "amount": amount,
        "useForBonus": useForBonus,
    }
    STORE.bank_accounts.setdefault(id, []).append(entry)
    return {"values": [entry]}


def update_employee_bank_account(
    id: str,
    entry_id: int,
    bankAccountType: Optional[str] = None,
    routingNumber: Optional[str] = None,
    accountNickname: Optional[str] = None,
    accountNumber: Optional[str] = None,
    bankName: Optional[str] = None,
    branchAddress: Optional[str] = None,
    bicOrSwift: Optional[str] = None,
    iban: Optional[str] = None,
    allocation: Optional[str] = None,
    amount: Optional[float] = None,
    useForBonus: Optional[bool] = None,
) -> Dict[str, Any]:
    entries = STORE.bank_accounts.get(id, [])
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        raise ValueError("Bank account entry not found")
    updates = {
        "bankAccountType": bankAccountType,
        "routingNumber": routingNumber,
        "accountNickname": accountNickname,
        "accountNumber": accountNumber,
        "bankName": bankName,
        "branchAddress": branchAddress,
        "bicOrSwift": bicOrSwift,
        "iban": iban,
        "allocation": allocation,
        "amount": amount,
        "useForBonus": useForBonus,
    }
    for key, value in updates.items():
        if value is not None:
            entry[key] = value
    return {"values": [entry]}


def delete_employee_bank_account(id: str, entry_id: int) -> Dict[str, Any]:
    entries = STORE.bank_accounts.get(id, [])
    STORE.bank_accounts[id] = [entry for entry in entries if entry["id"] != entry_id]
    return {"detail": f"Deleted bank account {entry_id} for employee {id}"}


def get_docs_folders_metadata() -> List[Dict[str, Any]]:
    return [
        {"id": {"value": "shared"}, "name": {"value": "Shared"}, "folderType": {"value": "shared"}},
        {"id": {"value": "confidential"}, "name": {"value": "Confidential"}, "folderType": {"value": "confidential"}},
        {"id": {"value": "custom-1"}, "name": {"value": "Custom Folder"}, "folderType": {"value": "custom"}},
    ]


def get_docs_for_employee(id: str) -> Dict[str, Any]:
    return {"documents": STORE.documents.get(id, [])}


def upload_shared_document(
    id: str, documentName: str, documentUrl: str, tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    doc_id = str(next(STORE.doc_id_seq))
    entry = {
        "id": doc_id,
        "documentName": {"value": documentName},
        "downloadLink": {"value": documentUrl},
        "tags": tags or [],
        "folderId": "shared",
    }
    STORE.documents.setdefault(id, []).append(entry)
    return {"documentName": {"value": documentName}, "downloadLink": {"value": documentUrl}}


def upload_confidential_document(
    id: str, documentName: str, documentUrl: str, tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    doc_id = str(next(STORE.doc_id_seq))
    entry = {
        "id": doc_id,
        "employeeId": id,
        "uploadedById": "service_user:1",
        "name": documentName,
        "creationDate": _utc_now_iso(),
        "status": "active",
        "tags": tags or [],
        "folderId": "confidential",
        "mimeType": "application/pdf",
        "fileId": doc_id,
        "documentName": documentName,
        "owner": {"id": id},
        "actionRequestDate": _utc_now_iso(),
        "actionCompleteDate": _utc_now_iso(),
    }
    STORE.documents.setdefault(id, []).append(entry)
    return entry


def upload_custom_document(
    id: str,
    folderId: str,
    documentName: str,
    documentUrl: str,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    doc_id = str(next(STORE.doc_id_seq))
    entry = {
        "id": doc_id,
        "employeeId": id,
        "uploadedById": "service_user:1",
        "name": documentName,
        "creationDate": _utc_now_iso(),
        "status": "active",
        "tags": tags or [],
        "folderId": folderId,
        "mimeType": "application/pdf",
        "fileId": doc_id,
        "documentName": documentName,
        "owner": {"id": id},
        "actionRequestDate": _utc_now_iso(),
        "actionCompleteDate": _utc_now_iso(),
    }
    STORE.documents.setdefault(id, []).append(entry)
    return entry


def delete_shared_document(id: str, docId: str) -> Dict[str, Any]:
    STORE.documents[id] = [doc for doc in STORE.documents.get(id, []) if doc.get("id") != docId]
    return {"detail": "deleted"}


def delete_confidential_document(id: str, docId: str) -> Dict[str, Any]:
    return delete_shared_document(id=id, docId=docId)


def delete_custom_document(id: str, folderId: str, docId: str) -> Dict[str, Any]:
    return delete_shared_document(id=id, docId=docId)


def get_all_company_fields() -> List[Dict[str, Any]]:
    return STORE.company_fields


def create_new_field(
    name: str, category: str, type: str, description: Optional[str] = None, historical: bool = False
) -> Dict[str, Any]:
    field_id = f"{category}.{name[:1].lower()}{name[1:].replace(' ', '')}"
    STORE.company_fields.append(
        {
            "id": field_id,
            "category": category,
            "categoryId": category,
            "categoryDisplayName": category.title(),
            "name": name,
            "description": description or "",
            "jsonPath": field_id,
            "type": type,
            "typeData": None,
            "historical": historical,
        }
    )
    return {"id": field_id}


def update_existing_field(fieldId: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    field_entry = next((field for field in STORE.company_fields if field["id"] == fieldId), None)
    if not field_entry:
        raise ValueError("Field not found")
    if name:
        field_entry["name"] = name
    if description:
        field_entry["description"] = description
    return {}


def delete_existing_field(fieldId: str) -> Dict[str, Any]:
    STORE.company_fields = [field for field in STORE.company_fields if field["id"] != fieldId]
    return {}


def get_all_company_lists(includeArchived: bool = False) -> List[Dict[str, Any]]:
    return list(STORE.company_lists.values())


def get_company_list_by_name(listName: str, includeArchived: bool = False) -> Dict[str, Any]:
    if listName not in STORE.company_lists:
        raise ValueError("List not found")
    return STORE.company_lists[listName]


def add_item_to_list(listName: str, name: str, parentId: Optional[int] = None) -> Dict[str, Any]:
    if listName not in STORE.company_lists:
        raise ValueError("List not found")
    list_entry = STORE.company_lists[listName]
    new_id = max([item["id"] for item in list_entry["items"]], default=0) + 1
    list_entry["items"].append({"id": new_id, "value": name, "name": name, "archived": False, "children": []})
    return {"id": str(new_id)}


def update_list_item(listName: str, itemId: str, name: Optional[str] = None, parentId: Optional[int] = None) -> Dict[str, Any]:
    list_entry = STORE.company_lists.get(listName)
    if not list_entry:
        raise ValueError("List not found")
    item = next((entry for entry in list_entry["items"] if str(entry["id"]) == itemId), None)
    if not item:
        raise ValueError("Item not found")
    if name:
        item["name"] = name
        item["value"] = name
    return {}


def delete_list_item(listName: str, itemId: str) -> Dict[str, Any]:
    list_entry = STORE.company_lists.get(listName)
    if not list_entry:
        raise ValueError("List not found")
    list_entry["items"] = [item for item in list_entry["items"] if str(item["id"]) != itemId]
    return {}


def read_all_open_tasks() -> Dict[str, Any]:
    tasks = [task for task in STORE.tasks if task.get("status") == "open"]
    return {"tasks": tasks}


def read_tasks_for_employee(id: str, task_status: Optional[str] = None) -> Dict[str, Any]:
    tasks = [task for task in STORE.tasks if task.get("employeeId") == id]
    if task_status:
        tasks = [task for task in tasks if task.get("status") == task_status]
    return {"tasks": tasks}


def complete_task(taskId: str) -> Dict[str, Any]:
    updated = 0
    for task in STORE.tasks:
        if str(task.get("id")) == taskId and task.get("status") == "open":
            task["status"] = "closed"
            updated = 1
            break
    return {"toDosUpdated": updated}


def get_custom_tables_metadata() -> Dict[str, Any]:
    return {"tables": list(STORE.custom_tables.values())}


def get_custom_table_metadata(custom_table_id: str) -> Dict[str, Any]:
    if custom_table_id not in STORE.custom_tables:
        raise ValueError("Table not found")
    return STORE.custom_tables[custom_table_id]


def get_employee_custom_table_entries(
    employee_id: str, custom_table_id: str, includeHumanReadable: bool = False
) -> Dict[str, Any]:
    entries = STORE.custom_table_entries.get((employee_id, custom_table_id), [])
    return {"values": entries}


def create_custom_table_entry(
    employee_id: str, custom_table_id: str, column_data: Dict[str, Any]
) -> Dict[str, Any]:
    entry = {"id": str(len(STORE.custom_table_entries.get((employee_id, custom_table_id), [])) + 1)}
    entry.update(column_data)
    STORE.custom_table_entries.setdefault((employee_id, custom_table_id), []).append(entry)
    return entry


def update_custom_table_entry(
    employee_id: str, custom_table_id: str, entry_id: str, column_data: Dict[str, Any]
) -> Dict[str, Any]:
    entries = STORE.custom_table_entries.get((employee_id, custom_table_id), [])
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        raise ValueError("Entry not found")
    entry.update(column_data)
    return entry


def delete_custom_table_entry(employee_id: str, custom_table_id: str, entry_id: str) -> Dict[str, Any]:
    entries = STORE.custom_table_entries.get((employee_id, custom_table_id), [])
    STORE.custom_table_entries[(employee_id, custom_table_id)] = [
        entry for entry in entries if entry["id"] != entry_id
    ]
    return {"detail": "deleted"}


HIBOB_TOOLS: List[Callable[..., Any]] = [
    get_policy_type_names,
    get_policy_type_details,
    get_reason_codes,
    add_reason_codes,
    get_policies,
    get_policy_names,
    submit_timeoff_request,
    get_timeoff_request,
    cancel_timeoff_request,
    get_request_changes,
    get_whosout,
    get_out_today,
    get_balance,
    create_balance_adjustment,
    import_attendance_data,
    read_company_reports,
    download_report_by_id,
    generate_company_report_async,
    download_report_by_name,
    read_all_active_job_ads,
    read_job_ads_by_id,
    read_company_job_profiles,
    get_all_job_roles,
    get_all_job_families,
    get_all_job_family_groups,
    get_job_profiles_metadata,
    get_job_roles_metadata,
    get_job_families_metadata,
    get_job_family_groups_metadata,
    get_goal_type_metadata,
    get_goals_metadata,
    get_key_results_metadata,
    search_goal_types,
    search_goals,
    search_key_results,
    create_goals,
    update_goal_status,
    update_goal,
    delete_goal,
    create_key_results,
    update_key_results_progress,
    update_key_results_details,
    delete_key_result,
    people_search,
    read_by_identifier,
    update_by_identifier,
    get_profiles,
    create_person,
    invite_employee,
    uninvite_employee,
    terminate_employee,
    set_start_date,
    get_avatar_by_email,
    get_avatar_by_id,
    upload_avatar_by_url,
    update_employee_email,
    get_all_positions_fields,
    get_all_position_openings_fields,
    get_all_position_budget_fields,
    read_company_positions,
    read_position_openings,
    read_position_budgets,
    create_positions,
    create_position_openings,
    update_position,
    update_position_opening,
    delete_position_opening,
    create_position_budget,
    update_position_budget,
    cancel_position,
    get_onboarding_wizards,
    get_bulk_people_work,
    get_bulk_lifecycle_history,
    get_bulk_employment_history,
    get_bulk_payroll_history,
    search_actual_payments,
    get_employee_work_history,
    create_employee_work_entry,
    update_employee_work_entry,
    delete_employee_work_entry,
    get_employee_employment_history,
    create_employee_employment_entry,
    update_employee_employment_entry,
    delete_employee_employment_entry,
    get_employee_lifecycle_history,
    get_employee_payroll_history,
    create_employee_salary_entry,
    delete_employee_salary_entry,
    get_payroll_history,
    get_employee_equity_grants,
    create_employee_equity_grant,
    update_employee_equity_grant,
    delete_employee_equity_grant,
    get_employee_variable_payments,
    create_employee_variable_payment,
    delete_employee_variable_payment,
    get_employee_training_records,
    create_employee_training_record,
    delete_employee_training_record,
    get_employee_bank_accounts,
    create_employee_bank_account,
    update_employee_bank_account,
    delete_employee_bank_account,
    get_docs_folders_metadata,
    get_docs_for_employee,
    upload_shared_document,
    upload_confidential_document,
    upload_custom_document,
    delete_shared_document,
    delete_confidential_document,
    delete_custom_document,
    get_all_company_fields,
    create_new_field,
    update_existing_field,
    delete_existing_field,
    get_all_company_lists,
    get_company_list_by_name,
    add_item_to_list,
    update_list_item,
    delete_list_item,
    read_all_open_tasks,
    read_tasks_for_employee,
    complete_task,
    get_custom_tables_metadata,
    get_custom_table_metadata,
    get_employee_custom_table_entries,
    create_custom_table_entry,
    update_custom_table_entry,
    delete_custom_table_entry,
]
