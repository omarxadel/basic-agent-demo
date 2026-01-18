# Main Requirements (Summary)

1. Update the agent to have mocks for these tools and support HiBob operations:

```json
[
  {
    "name": "get_policy_type_names",
    "description": "Get all policy type names.\n        \n        Returns a list of all available policy type names in the system.\n        \n        Response: Array of policy type name strings.\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_policy_type_details",
    "description": "Get details of a specific policy type.\n        \n        Returns complete information about a policy type including its configuration,\n        unit (days/hours), visibility settings, and related metadata.\n        \n        Parameters:\n        - policy_type: Policy type name (required)\n        \n        Response: Complete policy type object with all configuration details.\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "policy_type": {
          "type": "string",
          "description": "Policy type name"
        }
      },
      "required": [
        "policy_type"
      ]
    }
  },
  {
    "name": "get_reason_codes",
    "description": "Get reason codes for a policy type.\n        \n        Reason codes define specific reasons for taking leave (e.g., Headache, Mental health day).\n        Typically used for Sick leave policy types.\n        \n        Parameters:\n        - policy_type: Policy type name (required)\n        \n        Response: Array of reason code objects with code, description, and status.\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "policy_type": {
          "type": "string",
          "description": "Policy type name to get reason codes for"
        }
      },
      "required": [
        "policy_type"
      ]
    }
  },
  {
    "name": "add_reason_codes",
    "description": "Add reason codes to a policy type.\n        \n        Allows bulk creation of reason codes for a specific policy type.\n        Validates that the policy type exists and checks for duplicate codes.\n        \n        Parameters:\n        - policyType: Policy type name (required, must exist in database)\n        - reasonCodes: Array of reason code strings (required)\n          - Each code will be used as both the code and description\n          - Codes must be unique (no duplicates in request or existing codes)\n          - Case-insensitive duplicate checking\n        \n        Response: {reasonCodes: [{id, displayName}]}\n        \n        **Validation:**\n        - policyType must exist in database\n        - No duplicate codes in request\n        - Codes must not already exist for this policy type\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "policyType": {
          "type": "string",
          "description": "Policy type name (must exist in database)"
        },
        "reasonCodes": {
          "type": "array",
          "description": "Array of reason code strings (each used as code and description)",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "policyType",
        "reasonCodes"
      ]
    }
  },
  {
    "name": "get_policies",
    "description": "Get details about a given policy.\n        \n        **Endpoint**: GET /timeoff/policies?policyName={name}\n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        A policy defines the rules, values, and validations that govern leave regulations.\n        Each policy is linked to a policy type.\n        \n        Parameters:\n        - policyName: Policy name (required)\n        \n        Response fields:\n        - name (string): Policy name\n        - allowance (number): Base annual allowance\n        - maxBalance (number): Maximum balance at end of cycle\n        - minBalance (number): Minimum balance cap\n        - yosIncrease (array): Years of service increments\n        - minTimeOffRequestDuration (string): Shortest time employees can request\n        - bookingWorkDaysOnly (boolean): Whether non-working days are deducted\n        - approvalRequired (boolean): Requests require approval\n        - description (string): Policy description\n        - unit (string): \"days\" or \"hours\"\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "policyName": {
          "type": "string",
          "description": "Policy name (required)"
        }
      },
      "required": [
        "policyName"
      ]
    }
  },
  {
    "name": "get_policy_names",
    "description": "Get list of policy names for a given policy type.\n        \n        Returns names of all active policies under a specific policy type.\n        \n        Parameters:\n        - policy_type: Policy type name (required)\n        \n        Response: Array of policy name strings.\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "policy_type": {
          "type": "string",
          "description": "Policy type name to get policies for"
        }
      },
      "required": [
        "policy_type"
      ]
    }
  },
  {
    "name": "submit_timeoff_request",
    "description": "Submit a new time off request following HiBob API specification.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Supports 7 different request types:\n        1. days - Time off request in days (with start/end date portions)\n        2. hours - Time off request in hours for a specific date\n        3. differentDayDurations - Different hours per day across a date range\n        4. portionOnRange - Same portion (morning/afternoon) per day for a date range\n        5. hoursOnRange - Same hours per day for a date range\n        6. specificHoursDayDurations - Specific hours (time range) per day\n        7. differentSpecificHoursDayDurations - Different specific hours per day\n        \n        Common Parameters (all types):\n        - id: Employee ID (required) - path parameter\n        - policyType: Policy type name like \"Holiday\", \"Sick\" (required)\n        - requestRangeType: One of the 7 types above (required)\n        - startDate: Start date in YYYY-MM-DD format (required)\n        - endDate: End date in YYYY-MM-DD format (required for most types)\n        - skipManagerApproval: Skip approval (admin only, default: false)\n        - approver: Employee ID of approver (if skipManagerApproval is true)\n        - description: Request reason\n        - reasonCode: Reason code ID from policy type\n        \n        Required Fields by Request Type:\n        \n        1. days (REQUIRED: startDate, endDate, startDatePortion, endDatePortion, policyType):\n           - startDatePortion: 'all_day' or 'afternoon'\n           - endDatePortion: 'all_day' or 'morning'\n        \n        2. hours (REQUIRED: startDate, endDate, hours, minutes, policyType):\n           - hours: integer (0+)\n           - minutes: integer (0+)\n           - endDate must equal startDate\n        \n        3. differentDayDurations (REQUIRED: startDate, endDate, durations, policyType):\n           - durations: array of {date, hours, minutes}\n        \n        4. portionOnRange (REQUIRED: startDate, endDate, dayPortion, policyType):\n           - dayPortion: 'morning' or 'afternoon'\n        \n        5. hoursOnRange (REQUIRED: startDate, endDate, dailyHours, dailyMinutes, policyType):\n           - dailyHours: integer (0+)\n           - dailyMinutes: integer (0+)\n        \n        6. specificHoursDayDurations (REQUIRED: startDate, endDate, localStartTime, localEndTime, policyType):\n           - localStartTime: time in HH:MM:SS format\n           - localEndTime: time in HH:MM:SS format\n        \n        7. differentSpecificHoursDayDurations (REQUIRED: startDate, endDate, durations, policyType):\n           - durations: array with complex dayDuration structure\n        \n        Response: Created time off request with id, request_id, status.\n        \n        **Required Permissions:**\n        - Features > Time off > Settings > Manage company's time off settings\n        - People's Data > Time off > Requests > Create, edit, and cancel people's requests that haven't been approved yet\n        \n        **Note:** skipManagerApproval requires admin permissions\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (path parameter)"
        },
        "requestRangeType": {
          "type": "string",
          "enum": [
            "days",
            "hours",
            "differentDayDurations",
            "portionOnRange",
            "hoursOnRange",
            "specificHoursDayDurations",
            "differentSpecificHoursDayDurations"
          ],
          "description": "Type of time off request"
        },
        "policyType": {
          "type": "string",
          "description": "Policy type name (e.g., Holiday, Sick)"
        },
        "startDate": {
          "type": "string",
          "description": "Start date (YYYY-MM-DD format)"
        },
        "endDate": {
          "type": "string",
          "description": "End date (YYYY-MM-DD format)"
        },
        "startDatePortion": {
          "type": "string",
          "enum": [
            "all_day",
            "afternoon"
          ],
          "description": "For 'days' type: portion of first day"
        },
        "endDatePortion": {
          "type": "string",
          "enum": [
            "all_day",
            "morning"
          ],
          "description": "For 'days' type: portion of last day"
        },
        "hours": {
          "type": "integer",
          "description": "For 'hours' type: number of hours"
        },
        "minutes": {
          "type": "integer",
          "description": "For 'hours' type: number of minutes"
        },
        "durations": {
          "type": "array",
          "description": "For differentDayDurations or differentSpecificHoursDayDurations types",
          "items": {
            "type": "object",
            "description": "Duration entry for a specific date",
            "properties": {
              "date": {
                "type": "string",
                "format": "date",
                "description": "Date of the duration entry"
              },
              "hours": {
                "type": "integer",
                "description": "Hours for this date (for differentDayDurations)"
              },
              "minutes": {
                "type": "integer",
                "description": "Minutes for this date (for differentDayDurations)"
              },
              "dayDuration": {
                "type": "object",
                "description": "Day duration structure (for differentSpecificHoursDayDurations)",
                "properties": {
                  "dayDurationType": {
                    "type": "string",
                    "enum": [
                      "specificHoursDayDuration",
                      "portionDayDuration"
                    ],
                    "description": "Type of day duration"
                  },
                  "localStartTime": {
                    "type": "string",
                    "format": "time",
                    "description": "Start time (for specificHoursDayDuration type)"
                  },
                  "localEndTime": {
                    "type": "string",
                    "format": "time",
                    "description": "End time (for specificHoursDayDuration type)"
                  },
                  "portion": {
                    "type": "string",
                    "enum": [
                      "all_day",
                      "vacant"
                    ],
                    "description": "Portion of day (for portionDayDuration type)"
                  }
                }
              }
            }
          }
        },
        "dayPortion": {
          "type": "string",
          "enum": [
            "morning",
            "afternoon"
          ],
          "description": "For 'portionOnRange' type"
        },
        "dailyHours": {
          "type": "integer",
          "description": "For 'hoursOnRange' type: hours per day"
        },
        "dailyMinutes": {
          "type": "integer",
          "description": "For 'hoursOnRange' type: minutes per day"
        },
        "localStartTime": {
          "type": "string",
          "description": "For 'specificHoursDayDurations' type: start time (HH:MM:SS)"
        },
        "localEndTime": {
          "type": "string",
          "description": "For 'specificHoursDayDurations' type: end time (HH:MM:SS)"
        },
        "skipManagerApproval": {
          "type": "boolean",
          "description": "Skip approval (admin only)"
        },
        "approver": {
          "type": "string",
          "description": "Employee ID of approver (if skipManagerApproval is true)"
        },
        "description": {
          "type": "string",
          "description": "Request reason"
        },
        "reasonCode": {
          "type": "integer",
          "description": "Reason code ID"
        }
      },
      "required": [
        "id",
        "requestRangeType",
        "policyType",
        "startDate"
      ]
    }
  },
  {
    "name": "get_timeoff_request",
    "description": "Get details of an existing time off request.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Returns complete information about a specific time off request including\n        status, dates, approval details, and associated person information.\n        \n        Parameters:\n        - id: Person ID (required) - path parameter\n        - request_id: Request ID (required)\n        \n        Response: Complete time off request object.\n        \n        **Required Permissions:**\n        - People's Data > Time off > Requests > Create, edit, and cancel people's requests that haven't been approved yet\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "Person ID (path parameter)"
        },
        "request_id": {
          "type": "integer",
          "description": "Request ID (integer)"
        }
      },
      "required": [
        "id",
        "request_id"
      ]
    }
  },
  {
    "name": "cancel_timeoff_request",
    "description": "Cancel an existing time off request.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token (used to identify who is cancelling)\n        - X-Database-Id: Database identifier\n        \n        Marks the request as cancelled. This action cannot be undone.\n        The authenticated service user is automatically recorded as the person who cancelled the request.\n        \n        Parameters:\n        - id: Person ID (required) - path parameter\n        - request_id: Request ID (required)\n        \n        Response: Success confirmation with request_id.\n        \n        **Required Permissions:**\n        - People's Data > Time off > Requests > Create, edit, and cancel people's requests that haven't been approved yet\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Person ID (path parameter, must be string)"
        },
        "request_id": {
          "type": "integer",
          "description": "Request ID to cancel (integer)"
        }
      },
      "required": [
        "id",
        "request_id"
      ]
    }
  },
  {
    "name": "get_request_changes",
    "description": "Get all time off request changes in HiBob format.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Returns array of changes (Created, Canceled, Deleted, Pending) with complete request details.\n        Response format varies by request type with type-specific fields.\n        \n        **Date Range Validation:**\n        - since: Must be within last 6 months\n        - to: Optional, must be within 6 months of since\n        - If to is omitted, range extends from since to present\n        \n        Parameters:\n        - since: Starting date (ISO 8601 format, required, max 6 months in past)\n        - to: End date (ISO 8601 format, optional, max 6 months from since)\n        - includePending: Include pending requests (optional, default false)\n        \n        Response: {changes: [array of change objects with full request details]}\n        \n        **Required Permissions:**\n        - People's Data > Time off > See who's out today > See who's out\n        - (Optional) includePending may require additional permission\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "since": {
          "type": "string",
          "description": "Starting date (ISO 8601 format, required)"
        },
        "to": {
          "type": "string",
          "description": "End date (ISO 8601 format, optional)"
        },
        "includePending": {
          "type": "boolean",
          "description": "Include pending requests (default: false)"
        }
      },
      "required": [
        "since"
      ]
    }
  },
  {
    "name": "get_whosout",
    "description": "Read a list of who's out of the office in HiBob format.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Returns time off information for given date range. Only active users included.\n        Response format varies by request type with type-specific fields.\n        \n        Parameters:\n        - from: Start period date (required, YYYY-MM-DD)\n        - to: End period date (required, YYYY-MM-DD)\n        - includeHourly: Include hourly requests (default: false)\n        - includePrivate: Include private requests (default: false)\n        - includePending: Include pending requests (default: false)\n        - includeWorkingRequests: Include working types like WFH (default: true)\n        \n        Response: {\"outs\": [array of request objects]}\n        \n        **Required Permissions:**\n        - People's Data > Time off > See who's out today > See who's out\n        - (Optional) People's Data > Time off > See who's out today > See who's out because of private policy (if include_private=true)\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "from": {
          "type": "string",
          "description": "Start period date (YYYY-MM-DD)"
        },
        "to": {
          "type": "string",
          "description": "End period date (YYYY-MM-DD)"
        },
        "includeHourly": {
          "type": "boolean",
          "description": "Include hourly requests"
        },
        "includePrivate": {
          "type": "boolean",
          "description": "Include private requests"
        },
        "includePending": {
          "type": "boolean",
          "description": "Include pending requests"
        },
        "includeWorkingRequests": {
          "type": "boolean",
          "description": "Include working policy types"
        },
        "include_private": {
          "type": "boolean",
          "description": "Include private time off requests"
        }
      },
      "required": [
        "from",
        "to"
      ]
    }
  },
  {
    "name": "get_out_today",
    "description": "Read a list of who's out today or on specified date in HiBob format.\n        \n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Returns list of people with time off requests on specified date.\n        \n        Parameters:\n        - today: Date to report (optional, defaults to UTC current date, YYYY-MM-DD)\n        - includeHourly: Include hourly requests (optional, default: false)\n        - includePrivate: Include private requests (optional, default: false)\n        - siteId: Filter by employee's site ID (optional)\n        \n        Response: {\"outs\": [array]} with requestRangeType discriminator\n        - hours: uses \"hours\" and \"minutes\" fields\n        - days: includes startDatePortion/endDatePortion\n        - openEnded: includes startDatePortion/endDatePortion (may be null)\n        \n        **Required Permissions:**\n        - People's Data > Time off > See who's out today > See who's out\n        - (Optional) includePrivate requires additional permission\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "today": {
          "type": "string",
          "description": "Date to report (YYYY-MM-DD, defaults to UTC current date)"
        },
        "includeHourly": {
          "type": "boolean",
          "description": "Include hourly requests"
        },
        "includePrivate": {
          "type": "boolean",
          "description": "Include private requests"
        },
        "siteId": {
          "type": "integer",
          "description": "Filter by employee's site ID"
        }
      },
      "required": []
    }
  },
  {
    "name": "get_balance",
    "description": "Get the balance for a given employee in HiBob format.\n        \n        **Endpoint**: GET /timeoff/employees/{id}/balance?policyType={name}&date={date}\n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Retrieve the balance for a given employee, for a given policy type, as of a given date.\n        \n        Parameters (all required):\n        - id: Employee ID (path parameter, string)\n        - policyType: Policy type name (query parameter, string)\n        - date: Point in time (query parameter, date format YYYY-MM-DD)\n        \n        Response fields:\n        - employeeId (string): Employee ID\n        - totalBalanceAsOfDate (number): The retrieved balance as of this date\n        - totalRoundedBalanceAsOfDate (number): The retrieved rounded balance as of this date\n        - pointInTime (string, date): The balance date\n        - startingBalance (number): The balance as of the cycle start date\n        - startingBalanceAsOf (string, date): The cycle start date\n        - totalTaken (number): Total number of days/hours taken\n        - totalAdminAdjustments (number): Total number of days/hours manually adjusted\n        - totalSystemAdjustments (number): Total number of days/hours adjusted\n        - annualAllowance (number): Annual allowance\n        - policy (string): Policy name\n        \n        **Required Permissions:**\n        - See selected people's time off and sick leave balances\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (path parameter)"
        },
        "policyType": {
          "type": "string",
          "description": "Policy type name (query parameter, required)"
        },
        "date": {
          "type": "string",
          "format": "date",
          "description": "Point in time (query parameter, date format YYYY-MM-DD, required)"
        }
      },
      "required": [
        "id",
        "policyType",
        "date"
      ]
    }
  },
  {
    "name": "create_balance_adjustment",
    "description": "Create a balance adjustment for a given employee for a given effective date.\n        \n        **Endpoint**: POST /timeoff/employees/{id}/adjustments\n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        Allows manual adjustment of time off balances. Supports two adjustment types:\n        - balance: Adjusts the available balance directly\n        - daysUsed: Adjusts the days/hours already used\n        \n        Common use case: Adding time off in lieu for working on weekends.\n        \n        Parameters:\n        - id: Employee ID (required) - path parameter (string)\n        - adjustmentType: Type of adjustment - \"balance\" or \"daysUsed\" (required)\n        - policyType: Policy type name (required)\n        - effectiveDate: The date this adjustment becomes effective (YYYY-MM-DD format, required)\n        - amount: The amount of days/hours to add/subtract (required, number)\n        - reason: A reason for this adjustment (required)\n        \n        Response: 200 Success\n        - id: Adjustment ID (integer)\n        - msg: Success message (string)\n        \n        **Required Permissions:**\n        - Adjust selected peoples' time off balances and bank their overtime\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (path parameter)"
        },
        "adjustmentType": {
          "type": "string",
          "enum": [
            "balance",
            "daysUsed"
          ],
          "description": "Adjustment type - balance or time used"
        },
        "policyType": {
          "type": "string",
          "description": "Policy type name"
        },
        "effectiveDate": {
          "type": "string",
          "format": "date",
          "description": "The date this adjustment becomes effective (YYYY-MM-DD)"
        },
        "amount": {
          "type": "number",
          "description": "The amount of days/hours to add/subtract"
        },
        "reason": {
          "type": "string",
          "description": "A reason for this adjustment"
        }
      },
      "required": [
        "id",
        "adjustmentType",
        "policyType",
        "effectiveDate",
        "amount",
        "reason"
      ]
    }
  },
  {
    "name": "import_attendance_data",
    "description": "Import attendance punches (entries) for employees.\n        \n        **Endpoint**: POST /attendance/import/{importMethod}\n        **Headers Required:**\n        - X-Hibob-User-Token: Service user token\n        - X-Database-Id: Database identifier\n        \n        **Before using this endpoint:**\n        - Explore HiBob documentation for detailed information about this endpoint\n        - It's important to fully understand how to use this endpoint correctly to avoid errors in the import process\n        \n        **Import Methods:**\n        - aggregate: Adds the logs to a temporary location, and an aggregation job will process the data asynchronously\n        - immediate: Will insert the records as-is\n        \n        **ID Types:**\n        The ID type used to identify the employee. Can be one of:\n        - \"bobId\": Employee ID from database\n        - \"email\": Employee email address\n        - \"idInCompany\": Employee ID in company\n        - Custom field: Use forward slash separator format\n          Example: \"/identification/custom/Payroll Integration ID_1RNhI\"\n        \n        **Request Body Parameters:**\n        - importMethod: \"aggregate\" or \"immediate\" (required, path parameter)\n        - idType: ID type to identify employees (required)\n        - requests: Array of attendance events (required)\n          Each event contains:\n          - id: Employee identifier value (required, string)\n          - clockIn: Clock-in timestamp in local time (optional, format: \"2022-06-12T08:00\")\n          - clockOut: Clock-out timestamp in local time (optional, format: \"2022-06-12T17:00\")\n          - entryType: \"work\" or \"break\" (optional, default: \"work\")\n            **Important**: Break entries are supported only with 'immediate' import method\n        - dateTimeFormat: Custom date format for date-time values (optional, e.g., \"yyyy-MM-dd hh:mm a\")\n        \n        **Response:**\n        - status: \"success\", \"failed\", or \"partial_success\"\n        - total: Total number of clock-in and clock-out events received (number)\n        - imported: Number of clock-in/clock-out events imported (number)\n        - notImported: Number of clock-in/clock-out events not imported (number)\n        - errors: Array of error messages (array of strings)\n        \n        **Example Request:**\n        ```json\n        {\n          \"importMethod\": \"immediate\",\n          \"idType\": \"bobId\",\n          \"requests\": [\n            {\n              \"id\": \"123\",\n              \"clockIn\": \"2022-06-12T08:00\",\n              \"clockOut\": \"2022-06-12T17:00\",\n              \"entryType\": \"work\"\n            }\n          ]\n        }\n        ```\n        \n        **Example Response:**\n        ```json\n        {\n          \"status\": \"success\",\n          \"total\": 2,\n          \"imported\": 2,\n          \"notImported\": 0,\n          \"errors\": []\n        }\n        ```\n        \n        **Required Permissions:**\n        - Attendance management permissions\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "importMethod": {
          "type": "string",
          "enum": [
            "aggregate",
            "immediate"
          ],
          "description": "Import method: aggregate (async processing) or immediate (insert as-is)"
        },
        "idType": {
          "type": "string",
          "description": "ID type: 'bobId', 'email', 'idInCompany', or custom field path starting with '/'"
        },
        "requests": {
          "type": "array",
          "description": "List of attendance events",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "description": "Employee identifier value"
              },
              "clockIn": {
                "type": "string",
                "description": "Clock-in timestamp in local time (e.g., '2022-06-12T08:00')"
              },
              "clockOut": {
                "type": "string",
                "description": "Clock-out timestamp in local time (e.g., '2022-06-12T17:00')"
              },
              "entryType": {
                "type": "string",
                "enum": [
                  "work",
                  "break"
                ],
                "description": "Entry type (default: 'work'). Break only supported with 'immediate' method"
              }
            },
            "required": [
              "id"
            ]
          }
        },
        "dateTimeFormat": {
          "type": "string",
          "description": "Custom date format for date-time values (e.g., 'yyyy-MM-dd hh:mm a')"
        }
      },
      "required": [
        "importMethod",
        "idType",
        "requests"
      ]
    }
  },
  {
    "name": "read_company_reports",
    "description": "Fetch all reports available for the company.\n\nFollows the structure of Company Reports API `/reports/company`.\n\nResponse Structure:\n  - success: Boolean indicating operation success\n  - reports: Array of report objects",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "download_report_by_id",
    "description": "Returns or generates a downloadable report data file for a given report ID. Supports Service-type users only.\n\nPermissions required: The authenticated service user must have valid report download permissions.\n\nPath Params:\n  - reportId: The numeric ID of the report to download (required).\n\nQuery Params:\n  - format: File format (csv, xlsx, or json). Default: csv.\n  - includeInfo: Whether to include report info in the output (default: true).\n  - locale: Requested language for report columns (e.g., fr-FR).\n  - humanReadable: Optional, applies only for JSON format. Values: APPEND | REPLACE.\n\nResponses:\n  - 200: Returns completed report metadata with a download URL.\n  - 403: If user is not Service-type or lacks report permission.\n  - 404: If report or file not found.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "reportId": {
          "type": "number",
          "description": "The numeric ID of the report to download (e.g., 123).",
          "minimum": 1
        },
        "format": {
          "type": "string",
          "enum": [
            "csv",
            "xlsx",
            "json"
          ],
          "default": "csv",
          "description": "Desired output format. Defaults to csv."
        },
        "includeInfo": {
          "type": "boolean",
          "default": false,
          "description": "Include report info in the output file."
        },
        "locale": {
          "type": "string",
          "description": "Requested language for the report columns (e.g., 'fr-FR')."
        },
        "humanReadable": {
          "type": "string",
          "enum": [
            "APPEND",
            "REPLACE"
          ],
          "description": "Optional. Applies only for JSON format."
        }
      },
      "required": [
        "reportId"
      ]
    }
  },
  {
    "name": "generate_company_report_async",
    "description": "Asynchronously generate and download a company report using the HiBob-compatible endpoint.\n\nEndpoint: `POST /reports/{report_id}/download-async`\n\nThis endpoint triggers asynchronous report generation in the specified format and returns a polling URL in the `Location` header for checking report readiness or obtaining the download link.\n\n**Permissions Required:**\n- Only Service users with 'Reports permissions' can generate report downloads.\n\n**Query Parameters:**\n- `format` (string, enum: csv, xlsx): File format of the generated report.\n- `includeInfo` (boolean): Whether to include additional info metadata (default: false).\n- `locale` (string): Optional language locale for report columns (e.g., fr-FR). If not provided, the user preference locale is used.\n- `humanReadable` (string, enum: APPEND, REPLACE): Only applies for JSON format. Ignored for other formats.\n\n**Response:**\n- `200 OK`: Report already generated; returns the download URL.\n- `202 Accepted`: Report generation started; polling URL is provided in the `Location` header.\n- `403 Forbidden`: User lacks permission.\n- `404 Not Found`: Invalid or inaccessible report ID.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "reportId": {
          "type": "number",
          "description": "The numeric ID of the report to generate (e.g., 123)."
        },
        "format": {
          "type": "string",
          "enum": [
            "csv",
            "xlsx"
          ],
          "default": "csv",
          "description": "Output file format for the report."
        },
        "includeInfo": {
          "type": "boolean",
          "description": "Include report metadata and additional info.",
          "default": false
        },
        "locale": {
          "type": "string",
          "description": "Optional language locale for report columns (e.g., fr-FR).",
          "minLength": 2
        },
        "humanReadable": {
          "type": "string",
          "enum": [
            "APPEND",
            "REPLACE"
          ],
          "description": "For JSON format only — APPEND adds human-readable data, REPLACE replaces machine-readable values."
        }
      },
      "required": [
        "reportId"
      ]
    }
  },
  {
    "name": "download_report_by_name",
    "description": "Download the latest completed report run for a given report name.\n\n        Request Body Requirements:\n          - name: Required. The report name (e.g., 'Employee Report')\n\n        Response Structure:\n          - success: Boolean indicating operation success\n          - run: Latest completed report run object\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "reportName": {
          "type": "string",
          "description": "The  reportName (e.g., 'report_name.formate')",
          "minLength": 1
        }
      },
      "required": [
        "reportName"
      ]
    }
  },
  {
    "name": "read_all_active_job_ads",
    "description": "Fetch all active (published) job ads from the career page.\n\nQuery Parameters:\n  - preferred_language: Optional. Return job ads in the preferred language if available. Defaults to 'en'.\n\nRequest Body Parameters:\n  - fields: Array of jobAd fields to include in the response. Must include at least one field.\n  - filters: Array of filter objects to narrow search results. To fetch all active job ads, use an empty array [].\n\nResponse Structure:\n  - success: Boolean indicating operation success.\n  - count: Total number of active job ads.\n  - job_ads: Array of job ad objects with requested fields, e.g.:\n      - id\n      - applyUrl\n      - title\n      - departmentId\n      - department\n      - employmentTypeId\n      - employmentType\n      - siteId\n      - site\n      - country\n      - languageCode\n      - description\n      - requirements\n      - responsibilities\n      - benefits\n      - postedAt",
    "inputSchema": {
      "type": "object",
      "properties": {
        "preferredLanguage": {
          "type": "string",
          "description": "Optional query parameter for preferred language (e.g., en, fr). Defaults to 'en'."
        },
        "fields": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "string"
          },
          "description": "Array of /jobAd fields to include in the response. Must include at least one field (e.g., /jobAd/id, /jobAd/title)."
        },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "description": "Field ID to filter by (e.g., /jobAd/departmentId)."
              },
              "operator": {
                "type": "string",
                "description": "Filter operator (e.g., equals, notEquals, in, notIn)."
              },
              "values": {
                "type": "array",
                "minItems": 1,
                "items": {
                  "type": "string"
                },
                "description": "Values to filter by. Must include at least one value."
              }
            },
            "required": [
              "fieldId",
              "operator",
              "values"
            ]
          },
          "description": "Array of filter objects to narrow down the results. To fetch all active job ads, use an empty array []."
        }
      },
      "required": [
        "fields"
      ]
    },
    "queryParams": [
      "preferredLanguage"
    ]
  },
  {
    "name": "read_job_ads_by_id",
    "description": "Fetch detailed information for a single job ad by its ID.\n\n        Request Body Requirements:\n          - job_ad_id: Required. The job ad ID (e.g., job-123)\n\n        Response Structure:\n          - success: Boolean indicating operation success\n          - job_ad: Job ad object with details including:\n            - job_ad_id\n            - title\n            - status (draft, published, archived)\n            - department, job role, job profile\n            - location\n            - description\n            - apply_url\n            - posted_at\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid",
          "description": "The job ad ID (e.g., job-123)",
          "minLength": 1
        },
        "preferredLanguage": {
          "type": "string",
          "description": "Optional query parameter for preferred language (e.g., en, fr). Defaults to 'en'."
        }
      },
      "required": [
        "id"
      ]
    },
    "pathParams": [
      "id"
    ],
    "queryParams": [
      "preferredLanguage"
    ]
  },
  {
    "name": "read_company_job_profiles",
    "description": "Search and filter company job profiles with customizable field selection. Returns job profile entries matching the specified criteria.\n        \n        Requires fields array (path-style field IDs, max 50) and filters array to narrow results. Supports cursor-based pagination\n        for handling large datasets (limit 1-100, default 10). You can optionally include human-readable values via includeHumanReadable flag.\n        \n        Response includes job profile entries array and response_metadata with cursor for pagination.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "/jobProfile/assignedEmployees",
              "/jobProfile/code",
              "/jobProfile/description",
              "/jobProfile/id",
              "/jobProfile/jobFamilyGroupId",
              "/jobProfile/jobFamilyId",
              "/jobProfile/jobLevelRoleId",
              "/jobProfile/jobRoleId",
              "/jobProfile/status",
              "/jobProfile/title"
            ]
          },
          "minItems": 1,
          "maxItems": 50,
          "description": "List of field IDs to return (path-style)",
          "example": [
            "/jobProfile/id",
            "/jobProfile/title",
            "/jobProfile/status",
            "/jobProfile/jobRoleId"
          ]
        },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "example": "/jobProfile/status"
              },
              "operator": {
                "type": "string",
                "example": "equals"
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "example": [
                  "active"
                ]
              }
            },
            "required": [
              "fieldId",
              "operator",
              "values"
            ]
          },
          "description": "Filtering instructions"
        },
        "pagination": {
          "type": "object",
          "properties": {
            "limit": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100,
              "default": 10
            },
            "cursor": {
              "type": [
                "string",
                "null"
              ],
              "default": null
            }
          }
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": true
        }
      },
      "required": [
        "fields",
        "filters"
      ]
    }
  },
  {
    "name": "get_all_job_roles",
    "description": "List all job roles defined in the organization's job catalog. Returns role definitions used to categorize positions.\n        \n        Supports cursor-based pagination for handling large datasets (limit 1-100, default 100). You can optionally include\n        human-readable values via includeHumanReadable flag (default false).\n        \n        Response includes job roles array and response_metadata with cursor for pagination.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null
        },
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "default": 100
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false
        }
      },
      "required": []
    }
  },
  {
    "name": "get_all_job_families",
    "description": "List all job families defined in the organization's job catalog. Returns family groupings that organize related job roles.\n        \n        Supports cursor-based pagination for handling large datasets (limit 1-100, default 100). You can optionally include\n        human-readable values via includeHumanReadable flag (default false).\n        \n        Response includes job families array and response_metadata with cursor for pagination.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null
        },
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "default": 100
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false
        }
      },
      "required": []
    }
  },
  {
    "name": "get_all_job_family_groups",
    "description": "List all job family groups defined in the organization's job catalog. Returns higher-level groupings that contain multiple job families.\n        \n        Supports cursor-based pagination for handling large datasets (limit 1-100, default 100). You can optionally include\n        human-readable values via includeHumanReadable flag (default false).\n        \n        Response includes job family groups array and response_metadata with cursor for pagination.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null
        },
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "default": 100
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false
        }
      },
      "required": []
    }
  },
  {
    "name": "get_job_profiles_metadata",
    "description": "Return field metadata describing the structure and available fields for job profiles. Includes field definitions, data types, and validation rules.\n        \n        Use this to understand which fields are available when searching job profiles and what values they accept. No input parameters required.\n        \n        Response includes field definitions array with schema information for each available job profile field.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_job_roles_metadata",
    "description": "Return field metadata describing the structure and available fields for job roles. Includes field definitions, data types, and validation rules.\n        \n        Use this to understand the schema and available properties for job roles. No input parameters required.\n        \n        Response includes field definitions array with schema information for each available job role field.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_job_families_metadata",
    "description": "Return field metadata describing the structure and available fields for job families. Includes field definitions, data types, and validation rules.\n        \n        Use this to understand the schema and available properties for job families. No input parameters required.\n        \n        Response includes field definitions array with schema information for each available job family field.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_job_family_groups_metadata",
    "description": "Return field metadata describing the structure and available fields for job family groups. Includes field definitions, data types, and validation rules.\n        \n        Use this to understand the schema and available properties for job family groups. No input parameters required.\n        \n        Response includes field definitions array with schema information for each available job family group field.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_goal_type_metadata",
    "description": "Fetch all available goal types.\n\nResponse:\n  - items: List of goal type objects with fields id and name",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_goals_metadata",
    "description": "Fetch metadata for all goals.\n\nResponse:\n  - metadata: Array of goal metadata objects",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_key_results_metadata",
    "description": "Fetch metadata for all key results.\n\nResponse:\n  - metadata: Array of key result metadata objects",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "search_goal_types",
    "description": "Search Goal Types using filters and DB-driven pagination.\n\nBehavior:\n- Supports filtering by field values.\n- Pagination is performed using `limit` and `cursor`.\n- Returned items follow HiBob-compatible structure where field values are wrapped as { value: ... }.\n\nResponse:\n  - items: Array of objects with `objectType` and `fields`\n  - responseMetadata: { totalCount, pageSize }\n  - nextCursor: Cursor for the next page or null\n  - errors: Object containing error details (if any)",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "description": "List of field IDs to include in the response. Required.",
          "items": {
            "type": "string"
          }
        },
        "filters": {
          "type": "array",
          "description": "Optional filters to apply. Each filter applies field IN values.",
          "items": {
            "type": "object",
            "properties": {
              "field": {
                "type": "string",
                "description": "Field name in goalTypes to filter on."
              },
              "values": {
                "type": "array",
                "description": "List of accepted values for the field.",
                "items": {
                  "type": [
                    "string",
                    "number",
                    "boolean"
                  ]
                }
              }
            },
            "required": [
              "field",
              "values"
            ]
          }
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of results to return.",
          "default": 50,
          "minimum": 1
        },
        "cursor": {
          "type": "string",
          "description": "Cursor for pagination. Usually the last returned item ID.",
          "default": "0"
        }
      },
      "required": [
        "fields"
      ]
    }
  },
  {
    "name": "search_goals",
    "description": "Search goals using selected fields, optional filters, and cursor-based pagination.\n\nResponse:\n  - items: List of goals with requested fields.\n  - responseMetadata: Contains totalCount and pageSize.\n  - nextCursor: Cursor value to retrieve the next page.\n  - errors: List of errors, if any.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of goal field IDs to return. Use the metadata API to retrieve available field IDs."
        },
        "filters": {
          "type": "array",
          "description": "Filters to apply (AND logic).",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "description": "Goal field to filter on. Supported: status, isPrivate, typeId."
              },
              "operator": {
                "type": "string",
                "description": "Comparison operator. Currently only `equals` is supported.",
                "default": "equals"
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Values to match for the given fieldId."
              }
            },
            "required": [
              "fieldId",
              "values"
            ]
          }
        },
        "limit": {
          "type": "integer",
          "description": "Max number of records to return per page.",
          "default": 25,
          "minimum": 1
        },
        "cursor": {
          "type": "string",
          "description": "Pagination cursor. Pass null or '0' to start from beginning.",
          "default": "0"
        }
      },
      "required": [
        "fields"
      ]
    }
  },
  {
    "name": "search_key_results",
    "description": "Search and list Key Results using dynamic fields, mandatory goalId filter, and cursor-based pagination. Mirrors HiBob `POST /goals/key-results/search` behavior.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "description": "Array of field IDs to return for each key result. At least one is required (e.g., \"id\", \"title\").",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "filters": {
          "type": "array",
          "description": "List of filter conditions (combined with AND). The filter `fieldId = goalId` is mandatory.",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "description": "Field identifier to filter on (e.g., \"goalId\", \"status\")."
              },
              "operator": {
                "type": "string",
                "description": "Comparison operator. Currently only `equals` is supported.",
                "default": "equals"
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "List of values to match for this field. At least one required."
              }
            },
            "required": [
              "fieldId",
              "values"
            ]
          }
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of key results to return in this page. Must be a positive integer.",
          "default": 50,
          "minimum": 1
        },
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "description": "Pagination cursor from previous response. Use \"0\" or null to fetch the first page.",
          "default": "0"
        }
      },
      "required": [
        "fields",
        "filters"
      ]
    }
  },
  {
    "name": "create_goals",
    "description": "Create multiple goals at once using HiBob bulk goal creation format.\n\nResponse:\n  - goalIds: Array of created goal IDs",
    "inputSchema": {
      "type": "object",
      "properties": {
        "items": {
          "type": "array",
          "description": "List of goals to create",
          "items": {
            "type": "object",
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "goal"
                ],
                "description": "Must always be 'goal'"
              },
              "fields": {
                "type": "object",
                "properties": {
                  "title": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "description": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "startDate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "format": "date"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "dueDate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "format": "date"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "typeId": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "owner": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "isPrivate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "boolean"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "alignedGoal": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    }
                  },
                  "typeListItem": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  }
                },
                "required": [
                  "title",
                  "startDate",
                  "dueDate",
                  "typeId",
                  "owner",
                  "isPrivate"
                ]
              }
            },
            "required": [
              "objectType",
              "fields"
            ]
          }
        }
      },
      "required": [
        "items"
      ]
    }
  },
  {
    "name": "update_goal_status",
    "description": "Update the status of a goal by ID.\n\nResponse:\n  - Goal object with updated status",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer"
        },
        "status": {
          "type": "string"
        },
        "comment": {
          "type": "string"
        }
      },
      "required": [
        "goalId",
        "status"
      ]
    }
  },
  {
    "name": "update_goal",
    "description": "Partially update a goal by ID. Matches HiBob PATCH /goals/goals/{goalId}. Note: This endpoint does NOT update status. Use the Update Goal Status endpoint for status changes.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer",
          "description": "ID of the goal to update (path parameter)"
        },
        "items": {
          "type": "array",
          "description": "Array of update objects. Must contain exactly one item.",
          "items": {
            "type": "object",
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "goal"
                ],
                "description": "Must be set to 'goal'",
                "default": "goal"
              },
              "fields": {
                "type": "object",
                "properties": {
                  "title": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "description": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "owner": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    }
                  },
                  "startDate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "format": "date"
                      }
                    }
                  },
                  "dueDate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "format": "date"
                      }
                    }
                  },
                  "isPrivate": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "boolean"
                      }
                    }
                  },
                  "isActive": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "boolean"
                      }
                    }
                  },
                  "typeId": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    }
                  },
                  "alignedGoal": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer",
                        "nullable": true
                      }
                    }
                  }
                }
              }
            },
            "required": [
              "objectType",
              "fields"
            ]
          }
        }
      },
      "required": [
        "goalId",
        "items"
      ]
    },
    "responseSchema": {
      "type": "object",
      "properties": {
        "success": {
          "type": "boolean"
        },
        "goalId": {
          "type": "integer"
        }
      }
    }
  },
  {
    "name": "delete_goal",
    "description": "Delete a goal by ID.\n\nResponse:\n  - detail: Message indicating success",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer"
        }
      },
      "required": [
        "goalId"
      ]
    }
  },
  {
    "name": "create_key_results",
    "description": "Create multiple key results for a given goal. The goalId is provided in the request path. Supports creating up to 25 key results at once.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer",
          "description": "The ID of the goal to attach key results to."
        },
        "items": {
          "type": "array",
          "maxItems": 25,
          "items": {
            "type": "object",
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "keyResult"
                ],
                "default": "keyResult"
              },
              "fields": {
                "type": "object",
                "properties": {
                  "title": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "description": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "measureType": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "enum": [
                          "number",
                          "percentage",
                          "currency",
                          "boolean"
                        ]
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "target": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "number"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "currentValue": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "number"
                      }
                    }
                  },
                  "currency": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    },
                    "description": "Required if measureType = currency"
                  },
                  "currencySymbol": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    },
                    "description": "Required if measureType = currency"
                  }
                },
                "required": [
                  "title",
                  "measureType",
                  "target"
                ]
              }
            },
            "required": [
              "objectType",
              "fields"
            ]
          }
        }
      },
      "required": [
        "goalId",
        "items"
      ]
    }
  },
  {
    "name": "update_key_results_progress",
    "description": "Bulk update the progress values of key results belonging to a specific goal.\nThis call updates progress only — it does NOT change the goal’s status.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer",
          "description": "ID of the goal whose key results are being updated (from path parameter)"
        },
        "keyResults": {
          "type": "array",
          "description": "List of key results and their updated values",
          "items": {
            "type": "object",
            "properties": {
              "keyResultId": {
                "type": "integer",
                "description": "ID of the key result to update"
              },
              "currentValue": {
                "type": "string",
                "enum": [
                  "number",
                  "boolean",
                  "string"
                ],
                "description": "New progress value for the key result"
              }
            },
            "required": [
              "keyResultId",
              "currentValue"
            ]
          }
        },
        "comment": {
          "type": "string",
          "description": "Optional comment describing the update",
          "nullable": true
        }
      },
      "required": [
        "goalId",
        "keyResults"
      ]
    }
  },
  {
    "name": "update_key_results_details",
    "description": "Bulk update the details of multiple key results for a specific goal. Supports updating title, description, measureType, target, and currency fields. Maximum 25 items per request.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer",
          "description": "The ID of the goal that the key results belong to."
        },
        "items": {
          "type": "array",
          "maxItems": 25,
          "items": {
            "type": "object",
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "keyResult"
                ],
                "default": "keyResult"
              },
              "fields": {
                "type": "object",
                "properties": {
                  "keyResultId": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "value"
                    ]
                  },
                  "title": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "measureType": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string",
                        "enum": [
                          "number",
                          "percentage",
                          "currency",
                          "boolean"
                        ]
                      }
                    }
                  },
                  "target": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "number"
                      }
                    }
                  },
                  "currency": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  },
                  "currencySymbol": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "string"
                      }
                    }
                  }
                },
                "required": [
                  "keyResultId"
                ]
              }
            },
            "required": [
              "objectType",
              "fields"
            ]
          }
        }
      },
      "required": [
        "goalId",
        "items"
      ]
    }
  },
  {
    "name": "delete_key_result",
    "description": "Delete a key result by ID for a specific goal.\n\nResponse:\n  - 204 No Content on success",
    "inputSchema": {
      "type": "object",
      "properties": {
        "goalId": {
          "type": "integer",
          "description": "ID of the goal that contains the key result"
        },
        "keyResultId": {
          "type": "integer",
          "description": "ID of the key result to delete"
        }
      },
      "required": [
        "goalId",
        "keyResultId"
      ]
    }
  },
  {
    "name": "people_search",
    "description": "Search for employees based on specified criteria.\n        \n        **Endpoint**: POST /v1/people/search\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Request Body:**\n        - fields: Optional array of strings - list of field paths to return\n          * When not specified, returns default set of fields and categories:\n            - Basic employee fields: name, id, avatar URL, creation date, etc.\n            - Basic categories: About, Employment, Work\n          * When specified, returns only the requested fields\n          * Examples: [\"root.id\", \"root.firstName\", \"work.title\"]\n        - filters: Optional filters (ONLY root.id and root.email supported)\n        - showInactive: Optional boolean to include inactive employees (default: false)\n        - humanReadable: Optional formatting mode ('', 'APPEND', or 'REPLACE')\n        \n        **Filter Restrictions (validated by Pydantic):**\n        - fieldPath: MUST be 'root.id' or 'root.email' ONLY\n        - operator: MUST be 'equals' ONLY\n        - values: Cannot be empty list\n        - Any other fieldPath will return 400 error\n        - Any other operator will return 400 error\n        \n        **Field Paths:**\n        - root.id: Employee ID\n        - root.email: Email address\n        - root.firstName: First name\n        - root.displayName: Display name\n        - work.title: Job title\n        - work.department: Department\n        - work.site: Site location\n        - work.isManager: Manager flag\n        - about.about: About text\n        - about.superpowers: Superpowers list\n        \n        **Default Response (when fields not specified):**\n        Returns employees with comprehensive information including:\n        - Root fields: id, displayName, companyId, fullName, firstName, surname, creationDateTime\n        - Work category: title, manager, employeeIdInCompany, tenureDuration, site, department, isManager, etc.\n        - About category: about, superpowers, hobbies, foodPreferences, avatar\n        \n        **Example (valid filter):**\n        ```json\n        {\n          \"filters\": [\n            {\"fieldPath\": \"root.email\", \"operator\": \"equals\", \"values\": [\"john@example.com\"]}\n          ],\n          \"fields\": [\"root.id\", \"root.displayName\", \"work.title\"],\n          \"humanReadable\": \"\"\n        }\n        ```\n        \n        **Example (invalid filter - will return 400):**\n        ```json\n        {\n          \"filters\": [\n            {\"fieldPath\": \"work.title\", \"operator\": \"equals\", \"values\": [\"Engineer\"]}\n          ]\n        }\n        ```\n        This will fail with: \"fieldPath must be 'root.id' or 'root.email'\"\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "description": "List of field paths to return. Use dot notation (root.id) or slash notation (/root/id). Omit for default fields.",
          "items": {
            "type": "string"
          },
          "default": null
        },
        "filters": {
          "type": "array",
          "description": "Array of filter conditions. Each filter has fieldPath, operator, and values.",
          "items": {
            "type": "object",
            "properties": {
              "fieldPath": {
                "type": "string",
                "description": "Field to filter on. ONLY 'root.id' or 'root.email' allowed",
                "enum": [
                  "root.id",
                  "root.email"
                ]
              },
              "operator": {
                "type": "string",
                "description": "Comparison operator. ONLY 'equals' allowed",
                "enum": [
                  "equals"
                ],
                "default": "equals"
              },
              "values": {
                "type": "array",
                "description": "List of values to match",
                "items": {
                  "type": "string"
                },
                "minItems": 1
              }
            },
            "required": [
              "fieldPath",
              "values"
            ]
          },
          "default": []
        },
        "showInactive": {
          "type": "boolean",
          "description": "Include terminated/inactive employees in results",
          "default": false
        },
        "humanReadable": {
          "type": "string",
          "description": "Human-readable formatting: '' (none), 'APPEND' (add HR field), 'REPLACE' (replace with HR)",
          "enum": [
            "",
            "APPEND",
            "REPLACE"
          ],
          "default": ""
        }
      },
      "required": []
    }
  },
  {
    "name": "read_by_identifier",
    "description": "Read company employee fields by employee ID.\n\n**Endpoint**: POST /v1/people/{identifier}\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nThis endpoint allows you to retrieve employee data based on specified criteria.\n\n**Path Parameter:**\n- identifier: The backend-id of the Employee (numeric) OR employee's email address - REQUIRED\n\n**Request Body:**\n- fields: Optional list of field paths to return (if not provided, default fields are returned)\n- humanReadable: Optional formatting mode ('', 'APPEND', or 'REPLACE')\n\n**Permission Requirements:**\n- Service user must have access to the person (scope)\n- Service user must have 'view' permission for requested field categories\n- Fields are filtered based on category permissions (root, work, about)\n\n**Response Format:**\nReturns complete employee information in HiBob format with:\n- Top-level fields: fullName, displayName, id, firstName, surname, email, creationDateTime\n- Nested objects: employee, work, about\n- Field paths with values: /root/*, /work/*, /about/*\n- Work details: title, department, site, startDate, tenure information, reports structure\n- About details: superpowers, hobbies, foodPreferences, avatar\n\n**Example Request:**\n{\n  \"identifier\": {\"id\": \"101\"},\n  \"fields\": [\"root.id\", \"root.firstName\", \"work.title\"],\n  \"humanReadable\": \"\"\n}\n\n**Example Response:**\n{\n  \"employees\": [{\n    \"fullName\": \"John Doe\",\n    \"displayName\": \"John Doe\",\n    \"id\": \"101\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"creationDateTime\": \"2025-01-15T10:00:00.000Z\",\n    \"employee\": {\"payrollManager\": null, \"hrbp\": null, \"itAdmin\": null, \"buddy\": null},\n    \"/root/id\": {\"value\": \"101\"},\n    \"/root/firstName\": {\"value\": \"John\"},\n    \"/root/fullName\": {\"value\": \"John Doe\"},\n    \"/root/email\": {\"value\": \"john.doe@company.com\"},\n    \"/work/title\": {\"value\": \"Software Engineer\"},\n    \"/work/department\": {\"value\": \"Engineering\"},\n    \"/work/startDate\": {\"value\": \"2024-01-01\"},\n    \"work\": {\n      \"title\": \"Software Engineer\",\n      \"department\": \"Engineering\",\n      \"startDate\": \"2024-01-01\",\n      \"tenureDuration\": {\"periodISO\": \"P1Y0M15D\", \"sortFactor\": 380, \"humanize\": \"1 year and 15 days\"}\n    },\n    \"/about/about\": {\"value\": \"Passionate developer\"},\n    \"/about/superpowers\": {\"value\": [\"Python\", \"FastAPI\"]},\n    \"about\": {\n      \"about\": \"Passionate developer\",\n      \"superpowers\": [\"Python\", \"FastAPI\"],\n      \"hobbies\": [\"Coding\", \"Reading\"]\n    },\n    \"metadata\": {\n      \"extra-information\": {\n        \"LinkedIn\": \"https://www.linkedin.com/in/john-doe\",\n        \"Github\": \"https://github.com/johndoe\"\n      },\n      \"custom-fields\": {\n        \"Employee Level\": \"Senior\"\n      }\n    }\n  }]\n}\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "identifier": {
          "type": "string",
          "description": "Employee identifier - numeric ID or email address"
        },
        "fields": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Optional list of field paths to include (e.g., 'root.id', 'work.title')"
        },
        "humanReadable": {
          "type": "string",
          "enum": [
            "",
            "APPEND",
            "REPLACE"
          ],
          "default": "",
          "description": "Human-readable formatting mode"
        }
      },
      "required": [
        "identifier"
      ]
    }
  },
  {
    "name": "update_by_identifier",
    "description": "Update company employee by identifier.\n\n**Endpoint**: PUT /v1/people/identifier\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nPartial update: provide only fields you want to update.\n\n**Permission Requirements:**\n- root.edit required for firstName, surname, displayName, email, or root category changes\n- about.edit required to change about category\n- work.edit required to change work category\n\n**Request Body:**\n- identifier: Object with 'id' field (string or numeric) - REQUIRED\n- firstName: Optional first name (if provided, cannot be null or empty; max 50 chars, only letters and ^`-:,.\\/'\" allowed)\n- surname: Optional surname (if provided, cannot be null or empty; max 50 chars, only letters and ^`-:,.\\/'\" allowed)\n- displayName: Optional display name\n- email: Optional email address (if provided, cannot be null or empty; must be valid email format)\n- personal: Optional personal data object\n  - honorific: Optional honorific (e.g., \"Mr\", \"Ms\", \"Dr\")\n  - shortBirthDate: Optional short birth date (MM-DD format)\n  - nationality: Optional array of nationalities\n  - pronouns: Optional pronouns (e.g., \"he/him\", \"she/her\")\n- root: Optional root category updates (displayName, avatarUrl)\n- about: Optional about category updates (about, superpowers, hobbies, foodPreferences)\n- work: Optional work category updates (title, department, startDate, isManager (boolean: true/false), site)\n\n**Validation Rules:**\n- If firstName is provided, it cannot be null or empty string\n- If surname is provided, it cannot be null or empty string\n- If email is provided, it cannot be null or empty string and must be valid email format\n- firstName and surname: max 50 characters, only letters and ^`-:,.\\/'\" allowed\n- If work.site is provided, it cannot be null or empty string\n- If work.startDate is provided, it cannot be null or empty string and must be in YYYY-MM-DD format\n\n**Behavior:**\n- Updates are partial - only provided fields will be modified\n- Respects category-level permissions\n- Returns updated employee information\n\n**Example Request:**\n```json\n{\n  \"identifier\": {\"id\": \"101\"},\n  \"firstName\": \"Bob\",\n  \"personal\": {\n    \"honorific\": \"Mr\",\n    \"shortBirthDate\": \"01-15\",\n    \"nationality\": [\"US\"],\n    \"pronouns\": \"he/him\"\n  },\n  \"about\": {\n    \"hobbies\": [\"music\", \"travel\", \"sport\"]\n  }\n}\n```\n\n**Example Response:**\n```json\n{\n  \"employees\": [{\n    \"id\": \"101\",\n    \"firstName\": \"Bob\",\n    \"surname\": \"Smith\",\n    \"email\": \"bob.smith@company.com\",\n    \"displayName\": \"Bob Smith\",\n    \"personal\": {\n      \"honorific\": \"Mr\",\n      \"shortBirthDate\": \"01-15\",\n      \"nationality\": [\"US\"],\n      \"pronouns\": \"he/him\"\n    },\n    \"about\": {\n      \"hobbies\": [\"music\", \"travel\", \"sport\"]\n    },\n    \"metadata\": {\n      \"extra-information\": {\n        \"LinkedIn\": \"https://www.linkedin.com/in/bob-smith\"\n      }\n    }\n  }]\n}\n```\n\n**Metadata Fields:**\nThe response may include a `metadata` object containing custom metadata fields grouped by category, if the employee has any registered custom fields.\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "identifier": {
          "type": "object",
          "description": "Employee identifier object",
          "properties": {
            "id": {
              "type": "string",
              "description": "Employee id (string or integer)"
            }
          },
          "required": [
            "id"
          ]
        },
        "firstName": {
          "type": "string",
          "description": "First name"
        },
        "surname": {
          "type": "string",
          "description": "Surname/last name"
        },
        "displayName": {
          "type": "string",
          "description": "Display name"
        },
        "email": {
          "type": "string",
          "description": "Email address"
        },
        "personal": {
          "type": "object",
          "description": "Personal data (e.g., birthDate)",
          "additionalProperties": true
        },
        "root": {
          "type": "object",
          "description": "Root category updates",
          "properties": {
            "displayName": {
              "type": "string"
            },
            "avatarUrl": {
              "type": "string"
            }
          },
          "additionalProperties": true
        },
        "about": {
          "type": "object",
          "description": "About category updates",
          "properties": {
            "about": {
              "type": "string"
            },
            "superpowers": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "hobbies": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "foodPreferences": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          "additionalProperties": true
        },
        "work": {
          "type": "object",
          "description": "Work category updates",
          "properties": {
            "title": {
              "type": "string"
            },
            "department": {
              "type": "string"
            },
            "site": {
              "type": "string",
              "description": "Employee site (cannot be empty if provided)"
            },
            "startDate": {
              "type": "string",
              "description": "Start date in YYYY-MM-DD format (cannot be empty if provided)"
            },
            "isManager": {
              "type": "boolean",
              "description": "Manager flag (true/false). Response will return boolean value."
            },
            "data": {
              "type": "object",
              "additionalProperties": true
            }
          },
          "additionalProperties": true
        }
      },
      "required": [
        "identifier"
      ]
    }
  },
  {
    "name": "get_profiles",
    "description": "Read the public profile section of all active employees.\n\n**Endpoint**: GET /v1/people/profiles\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nReturns public profile information for all active employees in the company.\n\n**Behavior:**\n- Only returns active employees (lifecycle.status == 'active')\n- Respects service user's access scope\n- Returns only fields the service user has permission to view\n\n**Permission Requirements:**\n- Service user must have access to employees (scope)\n- work.view required to see work information\n- about.view required to see about information\n\n**Response Format:**\nReturns array of employee profile objects with:\n- Basic fields: id, firstName, surname, email, displayName\n- personal: Object with honorific, shortBirthDate, nationality, pronouns (if available)\n- about: Object with avatar, hobbies, foodPreferences, socialData, superpowers (if permitted)\n- work: Object with detailed work information including tenure, reports, etc. (if permitted)\n\n**Example Response:**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"displayName\": \"John Doe\",\n    \"personal\": {\n      \"honorific\": \"Mr\",\n      \"shortBirthDate\": \"01-15\",\n      \"nationality\": [\"US\"],\n      \"pronouns\": \"he/him\"\n    },\n    \"about\": {\n      \"avatar\": \"https://example.com/avatar.jpg\",\n      \"hobbies\": [\"Reading\", \"Coding\"],\n      \"foodPreferences\": [\"Vegetarian\"],\n      \"socialData\": {\n        \"linkedin\": \"john-doe\",\n        \"twitter\": \"@johndoe\",\n        \"facebook\": \"john.doe\"\n      },\n      \"superpowers\": [\"Python\", \"Leadership\"]\n    },\n    \"work\": {\n      \"shortStartDate\": \"01-15\",\n      \"startDate\": \"2024-01-15\",\n      \"manager\": \"67890\",\n      \"tenureDuration\": {\n        \"periodISO\": \"P1Y9M\",\n        \"sortFactor\": 640,\n        \"humanize\": \"1 year, 9 months\"\n      },\n      \"durationOfEmployment\": {\n        \"periodISO\": \"P1Y9M\",\n        \"sortFactor\": 640,\n        \"humanize\": \"1 year, 9 months\"\n      },\n      \"employeeIdInCompany\": 12345,\n      \"reportsToIdInCompany\": 67890,\n      \"reportsTo\": {\n        \"displayName\": \"Jane Smith\",\n        \"email\": \"jane.smith@company.com\",\n        \"surname\": \"Smith\",\n        \"firstName\": \"Jane\",\n        \"id\": \"67890\"\n      },\n      \"indirectReports\": 5,\n      \"siteID\": 1,\n      \"tenureDurationYears\": 1,\n      \"department\": \"Engineering\",\n      \"tenureYears\": 1,\n      \"isManager\": \"true\",\n      \"title\": \"Software Engineer\",\n      \"site\": \"New York\",\n      \"directReports\": 2,\n      \"yearsOfService\": 1\n    },\n    \"metadata\": {\n      \"extra-information\": {\n        \"LinkedIn\": \"https://www.linkedin.com/in/john-doe\",\n        \"Github\": \"https://github.com/johndoe\"\n      }\n    }\n  }]\n}\n```\n\n**Metadata Fields:**\nIf the employee has custom metadata fields registered, they will be returned in the `metadata` object, grouped by category.\n",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "create_person",
    "description": "Create company employee following HiBob API specification.\n\n**Endpoint**: POST /v1/people\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\n**Required Fields (per HiBob API):**\n- email: Valid email address, must be unique within the company\n- firstName: Max length 50, can only contain letters and ^`-:,.\\/'\"\n- surname: Max length 50, can only contain letters and ^`-:,.\\/'\"\n- work: Object with 'site' and 'startDate' (both required)\n  - site: Site name (display value) - will be looked up in sites table to get site_id\n  - startDate: Format YYYY-MM-DD, must be >= current date and < current date + 4 months (120 days)\n\n**Recommended Fields:**\n- work.title: Job title (STRONGLY RECOMMENDED - must be valid list-item from 'title' list)\n- work.department: Department (STRONGLY RECOMMENDED - must be valid list-item from 'department' list)\n\n**Optional Fields:**\n- displayName: Display name for the employee\n- root: Root category data (displayName, avatarUrl, etc.)\n- about: About category data (about text, superpowers, etc.)\n- work.manager: Manager ID\n- work.isManager: Boolean flag indicating if employee is a manager\n- work.siteId: Site ID reference to sites table (if not provided, will be looked up from site name)\n\n**Site Handling & Validation:**\n- If work.siteId is provided, it MUST exist in the sites table (validated) - will fetch site name automatically\n- If only work.site (name) is provided, it MUST exist in the sites table (validated) - will fetch site_id automatically\n- If both are provided, siteId takes precedence and site name will be fetched from the sites table\n- The site name and site_id are both stored in the work record for complete data integrity\n- **Validation Error**: If site/siteId doesn't exist in sites table, returns 400 error asking to register the site first\n\n**Permission Requirements:**\n- root.edit required to create person\n- work.edit required (work is mandatory)\n- about.edit required if about payload present\n\n**Response Format:**\nReturns a comprehensive HiBob-formatted object with all employee fields including:\n- Top-level fields: fullName, displayName, id, firstName, surname, email, creationDateTime\n- Nested objects: employee, work, about\n- Field paths with values: /root/*, /work/*, /about/*\n- Work details: title, department, site, startDate, tenure information, reports structure\n- About details: superpowers, hobbies, foodPreferences, avatar\n\n**Example 1: Minimal request (only required fields):**\n```json\n{\n  \"email\": \"joe.doe@examplecompany.com\",\n  \"firstName\": \"Joe\",\n  \"surname\": \"Doe\",\n  \"work\": {\n    \"site\": \"New York\",\n    \"startDate\": \"2025-11-15\"\n  }\n}\n```\nNote: The site \"New York\" must exist in the sites table, otherwise you'll get a 400 error.\n\n**Example 2: Recommended - with title, department, and manager:**\n```json\n{\n  \"email\": \"jane.smith@company.com\",\n  \"firstName\": \"Jane\",\n  \"surname\": \"Smith\",\n  \"work\": {\n    \"site\": \"New York\",\n    \"startDate\": \"2025-11-15\",\n    \"title\": \"Chief Engineer\",\n    \"department\": \"Engineering\",\n    \"manager\": \"102\"\n  }\n}\n```\nNote: Person with ID 102 must exist AND have is_manager=true, otherwise you'll get a 400 error.\n\n**Example 3: Using siteId instead of site name:**\n```json\n{\n  \"email\": \"john.engineer@company.com\",\n  \"firstName\": \"John\",\n  \"surname\": \"Engineer\",\n  \"work\": {\n    \"siteId\": 1,\n    \"startDate\": \"2025-12-01\",\n    \"title\": \"Software Engineer\",\n    \"department\": \"Engineering\"\n  }\n}\n```\nNote: Site with ID 1 must exist in sites table. The site name will be auto-fetched.\n\n**Example 4: Creating a manager (is_manager=true):**\n```json\n{\n  \"email\": \"sarah.manager@company.com\",\n  \"firstName\": \"Sarah\",\n  \"surname\": \"Manager\",\n  \"work\": {\n    \"site\": \"San Francisco\",\n    \"startDate\": \"2025-11-20\",\n    \"title\": \"Engineering Manager\",\n    \"department\": \"Engineering\",\n    \"isManager\": true\n  }\n}\n```\nNote: Set isManager to true if this person will manage other employees.\n\n**Full example with all optional fields and metadata:**\n```json\n{\n  \"email\": \"sarah.engineer@company.com\",\n  \"firstName\": \"Sarah\",\n  \"surname\": \"Engineer\",\n  \"displayName\": \"Sarah E.\",\n  \"work\": {\n    \"site\": \"San Francisco\",\n    \"siteId\": 2510069,\n    \"startDate\": \"2025-11-15\",\n    \"title\": \"Senior Engineer\",\n    \"department\": \"Engineering\",\n    \"manager\": \"102\",\n    \"isManager\": false,\n    \"employeeIdInCompany\": 250,\n    \"workPhone\": \"+1-555-0250\",\n    \"workMobile\": \"+1-555-0251\"\n  },\n  \"about\": {\n    \"about\": \"Experienced developer with passion for clean code\",\n    \"avatar\": \"https://example.com/avatar.jpg\",\n    \"superpowers\": [\"python\", \"react\", \"kubernetes\"],\n    \"hobbies\": [\"coding\", \"reading\", \"hiking\"],\n    \"foodPreferences\": {\"dietary\": \"vegan\"},\n    \"socialData\": {\n      \"linkedin\": \"https://www.linkedin.com/in/sarah-engineer\",\n      \"twitter\": \"@saraheng\",\n      \"facebook\": \"\"\n    }\n  },\n  \"metadata\": {\n    \"extra-information\": {\n      \"linkedin\": \"https://www.linkedin.com/in/sarah-engineer\",\n      \"github\": \"https://github.com/saraheng\",\n      \"twitter\": \"https://twitter.com/saraheng\"\n    },\n    \"custom-fields\": {\n      \"employee-level\": \"Senior\",\n      \"certification\": \"AWS Certified Solutions Architect\",\n      \"project-assignment\": \"Cloud Migration Project\"\n    }\n  }\n}\n```\n\n**Note on Twitter in socialData:**\n- Twitter can be a handle starting with @ (e.g., \"@saraheng\")\n- Or a full URL (e.g., \"https://twitter.com/saraheng\")\n- Empty strings are allowed for any social media field\n\n**Metadata Structure:**\nMetadata allows you to store custom fields organized by category:\n```json\n{\n  \"metadata\": {\n    \"category-name\": {\n      \"field-name\": \"field-value\",\n      \"another-field\": \"another-value\"\n    }\n  }\n}\n```\n\n**IMPORTANT - Field Registration Required:**\nBefore using metadata fields, they MUST be registered in the FieldMetadata table.\nThe API will validate that all metadata fields exist before creating the employee.\n\nTo register a new field, insert into the field_metadata table:\n```sql\nINSERT INTO field_metadata (field_id, category, category_id, category_display_name, name, json_path, type, type_data, historical)\nVALUES ('extra-information.linkedin', 'extra-information', 'extra-information', 'Extra Information', 'LinkedIn', 'extra-information.linkedin', 'string', '{}', 1);\n```\n\n**Validation Rules:**\n- **startDate**: Must be >= current date AND < current date + 4 months (120 days)\n  - Cannot set start dates in the past\n  - Cannot set start dates more than 4 months in the future\n- **work.isManager**: Must be a boolean value (true or false) - STRICT VALIDATION\n  - Only accepts boolean literals: true or false\n  - String values like \"yes\", \"no\", \"true\", \"false\" are REJECTED\n  - Returns 400 error if non-boolean value is provided\n  - Error message: \"isManager must be a boolean value (true or false), not a string. Use true or false without quotes.\"\n  - Response returns boolean: true or false (never \"Yes\"/\"No\" strings)\n- **work.manager**: If provided, the manager MUST have is_manager=true\n  - The manager ID must exist in the database\n  - The manager's work.is_manager flag must be set to true\n  - Returns 400 error if manager's is_manager flag is false\n  - Error message: \"Person with ID 'X' cannot be assigned as a manager because their is_manager flag is set to false\"\n- **workPhone / workMobile**:\n  - Must start with digit or + sign\n  - Must contain 7-15 digits total\n  - Can include spaces, hyphens, parentheses for formatting\n  - Examples: \"+1-555-0250\", \"+44 20 1234 5678\", \"555-0123\"\n- **Metadata**:\n  - All categories MUST exist in categories table\n  - All fields MUST exist in field_metadata table\n  - Category names: only letters, numbers, and hyphens allowed\n  - Field names: only letters, numbers, and hyphens allowed\n  - Invalid categories/fields return 400 error\n- **Social Media**:\n  - Twitter can be @handle or full URL\n  - LinkedIn/Facebook must be full URL (http:// or https://)\n\n**Example metadata fields (assuming they're registered):**\n```json\n{\n  \"metadata\": {\n    \"extra-information\": {\n      \"linkedin\": \"https://www.linkedin.com/in/sarah-engineer\",\n      \"github\": \"https://github.com/sarah-eng\"\n    }\n  }\n}\n```\n\n**Error Response (if fields not registered):**\n```json\n{\n  \"detail\": \"Invalid metadata fields. The following fields do not exist in FieldMetadata: extra-information.github. Please register these fields first by adding them to the field_metadata table.\"\n}\n```\n\n**Example response structure:**\n```json\n{\n  \"fullName\": \"Joe Doe\",\n  \"displayName\": \"Joe Doe\",\n  \"id\": \"1001\",\n  \"firstName\": \"Joe\",\n  \"surname\": \"Doe\",\n  \"email\": \"joe.doe@examplecompany.com\",\n  \"creationDateTime\": \"2025-10-27T11:00:00.000Z\",\n  \"employee\": {\n    \"payrollManager\": null,\n    \"hrbp\": null,\n    \"itAdmin\": null,\n    \"buddy\": null\n  },\n  \"/root/id\": {\"value\": \"1001\"},\n  \"/root/firstName\": {\"value\": \"Joe\"},\n  \"/root/fullName\": {\"value\": \"Joe Doe\"},\n  \"/work/title\": {\"value\": \"Chief Engineer\"},\n  \"/work/department\": {\"value\": \"Accounting\"},\n  \"/work/site\": {\"value\": \"New York\"},\n  \"/work/startDate\": {\"value\": \"2024-01-01\"},\n  \"work\": {\n    \"title\": \"Chief Engineer\",\n    \"department\": \"Accounting\",\n    \"site\": \"New York\",\n    \"startDate\": \"2024-01-01\",\n    \"manager\": \"110\",\n    \"reportsTo\": {\n      \"displayName\": \"Manager Name\",\n      \"email\": \"manager@company.com\",\n      \"firstName\": \"Manager\",\n      \"surname\": \"Name\",\n      \"id\": \"110\"\n    },\n    \"tenureDuration\": {\n      \"periodISO\": \"P1Y9M5D\",\n      \"sortFactor\": 640,\n      \"humanize\": \"1 years, 9 months and 5 days\"\n    }\n  },\n  \"about\": {\n    \"about\": \"New hire\",\n    \"superpowers\": [\"fast-learning\"],\n    \"hobbies\": [\"coding\"]\n  },\n  \"metadata\": {\n    \"extra-information\": {\n      \"LinkedIn\": \"https://www.linkedin.com/in/joe-doe\",\n      \"Github\": \"https://github.com/joedoe\"\n    }\n  }\n}\n```\n\n**Response includes metadata:**\nWhen metadata is provided in the request, the response includes a `metadata` object with all custom metadata fields grouped by category.\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Employee's email address (required). Must be valid and unique.",
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "firstName": {
          "type": "string",
          "description": "Employee's first name (required). Max length: 50, letters and ^`-:,.\\/'\" only.",
          "maxLength": 50,
          "pattern": "^[a-zA-Z\\^`\\-:,.\\\\/'\\ ]+$"
        },
        "surname": {
          "type": "string",
          "description": "Employee's surname (required). Max length: 50, letters and ^`-:,.\\/'\" only.",
          "maxLength": 50,
          "pattern": "^[a-zA-Z\\^`\\-:,.\\\\/'\\ ]+$"
        },
        "work": {
          "type": "object",
          "description": "Work object (required) with site and startDate",
          "properties": {
            "site": {
              "type": "string",
              "description": "Employee's site (required). Must be valid list-item from 'site' list."
            },
            "startDate": {
              "type": "string",
              "description": "Employment start date (required). Format: YYYY-MM-DD",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
            },
            "title": {
              "type": "string",
              "description": "Job title (RECOMMENDED). Must be valid list-item from 'title' list."
            },
            "department": {
              "type": "string",
              "description": "Department (RECOMMENDED). Must be valid list-item from 'department' list."
            },
            "manager": {
              "type": "string",
              "description": "Manager's ID (must be valid employee ID in database). The reportsTo object will be auto-populated from this ID."
            },
            "isManager": {
              "type": "boolean",
              "description": "Whether employee is a manager. MUST be boolean true/false, NOT string 'yes'/'no'. Response returns boolean."
            },
            "siteId": {
              "type": "integer",
              "description": "Site ID (backend identifier)"
            },
            "employeeIdInCompany": {
              "type": "integer",
              "description": "Employee ID within company"
            },
            "reportsToIdInCompany": {
              "type": "integer",
              "description": "ID of person employee reports to"
            },
            "secondLevelManager": {
              "type": "string",
              "description": "Second level manager ID"
            },
            "workPhone": {
              "type": "string",
              "description": "Work phone number. Validation: must start with digit or +, contain 7-15 digits, can include spaces/hyphens/parentheses. Examples: '+1-555-0250', '555-0123'",
              "pattern": "^[\\d\\+][\\d\\s\\-\\+\\(\\)]+$"
            },
            "workMobile": {
              "type": "string",
              "description": "Work mobile number. Validation: must start with digit or +, contain 7-15 digits, can include spaces/hyphens/parentheses. Examples: '+1-555-0251', '+44 20 1234 5678'",
              "pattern": "^[\\d\\+][\\d\\s\\-\\+\\(\\)]+$"
            },
            "directReports": {
              "type": "integer",
              "description": "Number of direct reports"
            },
            "indirectReports": {
              "type": "integer",
              "description": "Number of indirect reports"
            },
            "daysOfPreviousService": {
              "type": "integer",
              "description": "Days of previous service"
            },
            "tenureDuration": {
              "type": "object",
              "description": "Tenure duration object (auto-calculated if not provided)",
              "additionalProperties": true
            }
          },
          "required": [
            "site",
            "startDate"
          ],
          "additionalProperties": true
        },
        "displayName": {
          "type": "string",
          "description": "Display name (optional). Auto-generated from firstName and surname if not provided."
        },
        "lifecycle": {
          "type": "object",
          "additionalProperties": true
        },
        "metadata": {
          "type": "object",
          "description": "Custom metadata fields organized by category. Structure: {category: {field: value}}",
          "additionalProperties": {
            "type": "object",
            "additionalProperties": true
          },
          "example": {
            "extra-information": {
              "linkedin": "https://www.linkedin.com/in/user",
              "github": "https://github.com/user"
            }
          }
        },
        "root": {
          "type": "object",
          "properties": {
            "displayName": {
              "type": "string"
            },
            "avatarUrl": {
              "type": "string"
            },
            "data": {
              "type": "object",
              "additionalProperties": true
            }
          },
          "additionalProperties": true
        },
        "about": {
          "type": "object",
          "properties": {
            "about": {
              "type": "string",
              "description": "About/bio text"
            },
            "avatar": {
              "type": "string",
              "description": "Avatar image URL"
            },
            "superpowers": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Array of superpowers/skills"
            },
            "hobbies": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Array of hobbies"
            },
            "foodPreferences": {
              "type": "object",
              "description": "Food preferences object",
              "additionalProperties": true
            },
            "socialData": {
              "type": "object",
              "description": "Social media links",
              "properties": {
                "linkedin": {
                  "type": "string"
                },
                "twitter": {
                  "type": "string"
                },
                "facebook": {
                  "type": "string"
                }
              }
            }
          },
          "additionalProperties": true
        }
      },
      "required": [
        "email",
        "firstName",
        "surname",
        "work"
      ]
    }
  },
  {
    "name": "invite_employee",
    "description": "Invite an employee to Bob with a welcome wizard.\n\n**Endpoint**: POST /v1/people/{employeeId}/invitations\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nInvites an employee to Bob with a welcome wizard. The employee will receive an invitation to access the system.\n\n**Path Parameter:**\n- employeeId: Employee ID (must be an integer)\n\n**Request Body (required):**\n- welcomeWizardId: Welcome wizard configuration ID (required, must be an integer)\n\n**Permission Requirements:**\n- root.edit required\n- Service user must be in scope for the employee\n\n**Validation Rules:**\n- Employee must exist in the database\n- Employee must NOT already be invited (lifecycle.status != 'invited')\n- If employee is already invited, returns 400 error: \"Person with ID {id} is already invited\"\n- welcomeWizardId must exist in the onboarding_wizards table\n- Welcome wizard must be active (is_active = true)\n\n**Behavior:**\n- Validates welcomeWizardId exists in onboarding_wizards table\n- Validates wizard is active before allowing invitation\n- Sets lifecycle.status to 'invited'\n- Records invitedAt timestamp\n- Stores welcome wizard ID in lifecycle.welcomeWizardId\n- Tracks who performed the action in lifecycle.invitedBy\n- Updates metadata with invitation tracking information\n\n**Example Request:**\n```json\n{\n  \"employeeId\": 12345,\n  \"welcomeWizardId\": 123\n}\n```\n\n**Example Response (Success):**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"lifecycle\": {\n      \"status\": \"invited\",\n      \"invitedAt\": \"2025-10-28T10:00:00.000Z\",\n      \"welcomeWizardId\": 123,\n      \"invitedBy\": \"service_user:1\"\n    }\n  }]\n}\n```\n\n**Example Response (Already Invited - 400 Error):**\n```json\n{\n  \"detail\": \"Person with ID 12345 is already invited\"\n}\n```\n\n**Example Response (Invalid Wizard - 400 Error):**\n```json\n{\n  \"detail\": \"Welcome wizard with ID 999 does not exist in the onboarding_wizards table. Please provide a valid wizard ID.\"\n}\n```\n\n**Example Response (Inactive Wizard - 400 Error):**\n```json\n{\n  \"detail\": \"Welcome wizard with ID 123 is not active and cannot be used for invitations.\"\n}\n```\n\n**Error Responses:**\n- 400: Employee already invited, invalid wizard ID, or inactive wizard\n- 403: Missing permissions or not in scope\n- 404: Employee not found\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employeeId": {
          "type": "integer",
          "description": "Employee ID (required path parameter - must be an integer)"
        },
        "welcomeWizardId": {
          "type": "integer",
          "description": "Welcome wizard configuration ID (required - must be a positive integer)"
        }
      },
      "required": [
        "employeeId",
        "welcomeWizardId"
      ]
    }
  },
  {
    "name": "uninvite_employee",
    "description": "Revoke access (uninvite) for an employee.\n\n**Endpoint**: POST /v1/people/{identifier}/uninvite\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nRevokes an employee's access to Bob by setting their lifecycle status to 'invitation_revoked'.\n\n**Path Parameter:**\n- identifier: Employee ID (numeric)\n\n**Request Body:**\n- reason: Optional reason for uninviting the employee (for audit logging)\n\n**Permission Requirements:**\n- root.edit required\n- Service user must be in scope for the employee\n\n**Validation Rules:**\n- Employee must exist in the database\n- Employee must NOT already be uninvited (lifecycle.status != 'invitation_revoked')\n- If employee is already uninvited, returns 400 error: \"Person with ID {id} is already uninvited\"\n\n**Behavior:**\n- Sets lifecycle.status to 'invitation_revoked'\n- Records uninvitedAt timestamp\n- Stores reason if provided in lifecycle.uninviteReason\n- Tracks who performed the action in lifecycle.uninvitedBy\n\n**Example Request:**\n```json\n{\n  \"identifier\": \"12345\",\n  \"reason\": \"Access no longer required\"\n}\n```\n\n**Example Response (Success):**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"lifecycle\": {\n      \"status\": \"invitation_revoked\",\n      \"uninvitedAt\": \"2025-11-21T10:00:00.000Z\",\n      \"uninviteReason\": \"Access no longer required\",\n      \"uninvitedBy\": \"service_user:1\"\n    }\n  }]\n}\n```\n\n**Example Response (Already Uninvited - 400 Error):**\n```json\n{\n  \"detail\": \"Person with ID 12345 is already uninvited\"\n}\n```\n\n**Error Responses:**\n- 400: Employee already uninvited or invalid identifier\n- 403: Missing permissions or not in scope\n- 404: Employee not found\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "identifier": {
          "type": "string",
          "description": "Employee identifier (path param)"
        },
        "reason": {
          "type": "string",
          "description": "Optional reason for audit logging"
        }
      },
      "required": [
        "identifier"
      ]
    }
  },
  {
    "name": "terminate_employee",
    "description": "Terminate an employee following HiBob API specification.\n\n**Endpoint**: POST /v1/people/{identifier}/terminate\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nTerminates an employee by setting their status to terminated with the specified termination date.\n\n**Path Parameter:**\n- identifier: Employee ID (numeric)\n\n**Request Body:**\n- terminationDate: Termination date in ISO 8601 format (required, e.g., \"2025-12-31\")\n  **IMPORTANT: terminationDate MUST be greater than the current date (future date)**\n- noticePeriod: Notice period details (optional)\n  - unit: Time unit - \"days\", \"weeks\", or \"months\"\n  - length: Length of notice period (integer)\n- lastDayOfWork: Last day of work in ISO 8601 format (optional, e.g., \"2025-12-31\")\n  **IMPORTANT: lastDayOfWork MUST be equal to terminationDate (not before, not after)**\n- terminationReason: Reason for termination (optional, e.g., \"Redundant\", \"Resignation\", \"Retirement\")\n- reasonType: Type/category of termination reason (optional, e.g., \"End of Contract\", \"Voluntary\", \"Involuntary\")\n\n**Permission Requirements:**\n- root.edit required\n- Service user must be in scope for the employee\n\n**Validation Rules:**\n- Employee must exist in the database\n- Employee must NOT already be terminated (lifecycle.status != 'terminated')\n- If employee is already terminated, returns 400 error: \"Person with ID {id} is already terminated\"\n- terminationDate must be in YYYY-MM-DD format\n- terminationDate must be greater than current date (cannot terminate in the past or today)\n- lastDayOfWork must be in YYYY-MM-DD format if provided\n- lastDayOfWork must be EQUAL to terminationDate (cannot be before or after)\n- noticePeriod.unit must be one of: \"days\", \"weeks\", \"months\" (returns 400 if invalid)\n- noticePeriod.length must be a positive integer greater than 0 (returns 400 if negative or zero)\n\n**Behavior:**\n- Sets lifecycle.status to 'terminated'\n- Stores terminationDate and terminatedAt timestamp\n- Stores notice period details if provided\n- Stores last day of work if provided\n- Stores termination reason and reason type if provided\n- Tracks who performed the action in lifecycle.terminatedBy\n- Updates metadata with termination information\n\n**Example Request (full):**\n```json\n{\n  \"identifier\": \"12345\",\n  \"terminationDate\": \"2025-12-31\",\n  \"noticePeriod\": {\n    \"unit\": \"days\",\n    \"length\": 30\n  },\n  \"lastDayOfWork\": \"2025-12-31\",\n  \"terminationReason\": \"Redundant\",\n  \"reasonType\": \"End of Contract\"\n}\n```\n\n**Example Request (minimal):**\n```json\n{\n  \"identifier\": \"12345\",\n  \"terminationDate\": \"2025-12-31\"\n}\n```\n\n**Example Response (Success):**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"lifecycle\": {\n      \"status\": \"terminated\",\n      \"terminationDate\": \"2025-12-31\",\n      \"terminatedAt\": \"2025-11-21T10:00:00.000Z\",\n      \"terminationReason\": \"Redundant\",\n      \"reasonType\": \"End of Contract\",\n      \"terminatedBy\": \"service_user:1\"\n    }\n  }]\n}\n```\n\n**Example Response (Already Terminated - 400 Error):**\n```json\n{\n  \"detail\": \"Person with ID 12345 is already terminated\"\n}\n```\n\n**Error Responses:**\n- 400: Employee already terminated, invalid identifier, invalid date format, invalid notice period unit, negative notice period length, or lastDayOfWork after terminationDate\n- 403: Missing permissions or not in scope\n- 404: Employee not found\n\n**Validation Error Examples:**\n\nInvalid notice period unit:\n```json\n{\n  \"detail\": [{\n    \"type\": \"value_error\",\n    \"loc\": [\"body\", \"noticePeriod\", \"unit\"],\n    \"msg\": \"noticePeriod.unit must be one of: days, weeks, months. Got: 'years'\"\n  }]\n}\n```\n\nNegative notice period length:\n```json\n{\n  \"detail\": [{\n    \"type\": \"greater_than\",\n    \"loc\": [\"body\", \"noticePeriod\", \"length\"],\n    \"msg\": \"Input should be greater than 0\"\n  }]\n}\n```\n\nlastDayOfWork not equal to terminationDate:\n```json\n{\n  \"detail\": [{\n    \"type\": \"value_error\",\n    \"loc\": [\"body\", \"lastDayOfWork\"],\n    \"msg\": \"lastDayOfWork must be equal to terminationDate\"\n  }]\n}\n```\n\n**Note:** The terminationDate in examples is set to a future date as required by validation.\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "identifier": {
          "type": "string",
          "description": "Employee identifier (numeric id) - path parameter"
        },
        "terminationDate": {
          "type": "string",
          "description": "Termination date in ISO 8601 format (YYYY-MM-DD). Required. MUST be greater than current date.",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "noticePeriod": {
          "type": "object",
          "description": "Notice period details (optional)",
          "properties": {
            "unit": {
              "type": "string",
              "description": "Time unit: 'days', 'weeks', or 'months'",
              "enum": [
                "days",
                "weeks",
                "months"
              ]
            },
            "length": {
              "type": "integer",
              "description": "Length of notice period"
            }
          },
          "required": [
            "unit",
            "length"
          ]
        },
        "lastDayOfWork": {
          "type": "string",
          "description": "Last day of work in ISO 8601 format (YYYY-MM-DD). Optional."
        },
        "terminationReason": {
          "type": "string",
          "description": "Reason for termination (e.g., 'Redundant', 'Resignation', 'Retirement', 'Termination')"
        },
        "reasonType": {
          "type": "string",
          "description": "Type/category of termination reason (e.g., 'End of Contract', 'Voluntary', 'Involuntary')"
        }
      },
      "required": [
        "identifier",
        "terminationDate"
      ]
    }
  },
  {
    "name": "set_start_date",
    "description": "Set or update an employee's start date.\n\n**Endpoint**: POST /v1/people/{employeeId}/start-date\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nUpdates an employee's start date in their work record. This affects tenure calculations and employment duration.\n\n**Path Parameter:**\n- employeeId: Employee ID (must be an integer)\n\n**Request Body (required):**\n- startDate: Start date in ISO 8601 format YYYY-MM-DD (required)\n  **IMPORTANT: startDate MUST be greater than or equal to current date (today or future date)**\n- reason: Optional reason for setting/updating the start date\n\n**Permission Requirements:**\n- work.edit required\n- Service user must be in scope for the employee\n\n**Validation Rules:**\n- startDate must be in YYYY-MM-DD format\n- startDate must be greater than or equal to current date (cannot be in the past)\n\n**Behavior:**\n- Updates work.startDate with the provided date\n- Sets work.originalStartDate if not already set\n- Updates work.activeEffectiveDate\n- Stores reason if provided\n- Recalculates tenure duration based on the new start date\n- Creates work record if it doesn't exist\n\n**Example Request:**\n```json\n{\n  \"employeeId\": 12345,\n  \"startDate\": \"2025-12-01\",\n  \"reason\": \"Setting future start date\"\n}\n```\n\n**Note:** The startDate in examples is set to today or a future date as required by validation.\n\n**Example Response:**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"work\": {\n      \"startDate\": \"2024-01-15\",\n      \"originalStartDate\": \"2024-01-15\",\n      \"tenureDuration\": {\n        \"years\": 1,\n        \"months\": 9,\n        \"humanize\": \"1 years, 9 months\"\n      }\n    }\n  }]\n}\n```\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employeeId": {
          "type": "integer",
          "description": "Employee ID (required path parameter - must be an integer)"
        },
        "startDate": {
          "type": "string",
          "description": "Employee start date in ISO 8601 format (YYYY-MM-DD). Required. MUST be greater than or equal to current date.",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "reason": {
          "type": "string",
          "description": "Optional reason for setting/updating the start date"
        }
      },
      "required": [
        "employeeId",
        "startDate"
      ]
    }
  },
  {
    "name": "get_avatar_by_email",
    "description": "Read avatar URL for an employee by their email address.\n\n**Endpoint**: GET /v1/people/avatars?email=employee@company.com\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\n**Query Parameter (validated by Pydantic):**\n- email: Employee email address (required, must be valid email format)\n\n**Validation Rules:**\n- email cannot be empty\n- email must contain @ symbol\n- email must match standard email format pattern\n- Invalid email returns 400 error with Pydantic validation message\n\n**Permission Requirements:**\n- about.view required (People's data > About > View selected employees' About sections)\n- Service user must be in scope for the employee\n\n**Returns:**\n- email: The employee's email address\n- avatarUrl: The URL of the employee's avatar image (null if not set)\n- employeeId: The employee's ID\n\n**Example Request:**\n```\nGET /v1/people/avatars?email=john.doe@company.com\n```\n\n**Example Response (Success):**\n```json\n{\n  \"email\": \"john.doe@company.com\",\n  \"avatarUrl\": \"https://cdn.company.com/avatars/john.jpg\",\n  \"employeeId\": \"12345\"\n}\n```\n\n**Example Response (Invalid Email - 400 Error):**\n```json\n{\n  \"detail\": [{\n    \"type\": \"value_error\",\n    \"loc\": [\"query\", \"email\"],\n    \"msg\": \"Invalid email format\",\n    \"input\": \"invalid-email\"\n  }]\n}\n```\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Employee email address (required query parameter)"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "get_avatar_by_id",
    "description": "Read avatar URL for an employee by their ID.\n\n**Endpoint**: GET /v1/people/avatars/{employeeId}\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nRetrieves the avatar image URL for an employee identified by their employee ID.\n\n**Path Parameter:**\n- employeeId: Employee ID (must be an integer)\n\n**Permission Requirements:**\n- about.view required (People's data > About > View selected employees' About sections)\n- Service user must be in scope for the employee\n\n**Important Notes:**\n- The employeeId parameter MUST be an integer, not a string\n- The visibility of avatars through the API is restricted based on the About category permission\n- To allow the service user to read the avatar, you need to enable the permission:\n  \"People's data > About > View selected employees' About sections\"\n\n**Returns:**\n- employeeId: The employee's ID\n- email: The employee's email address\n- avatarUrl: The URL of the employee's avatar image (null if not set)\n\n**Example Request:**\n```json\n{\n  \"employeeId\": 12345\n}\n```\n\n**Example Response:**\n```json\n{\n  \"employeeId\": \"12345\",\n  \"email\": \"john.doe@company.com\",\n  \"avatarUrl\": \"https://cdn.company.com/avatars/john.jpg\"\n}\n```\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employeeId": {
          "type": "integer",
          "description": "Employee ID (required path parameter - must be an integer)"
        }
      },
      "required": [
        "employeeId"
      ]
    }
  },
  {
    "name": "upload_avatar_by_url",
    "description": "Upload an employee's avatar by providing an image URL.\n\n**Endpoint**: PUT /v1/people/avatars/{employeeId}\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nUploads/updates an employee's avatar by specifying an image URL. The URL should point to a publicly accessible image.\n\n**Path Parameter:**\n- employeeId: Employee ID (must be an integer)\n\n**Request Body:**\n- url: URL of the avatar image (required, must start with http:// or https://)\n\n**Permission Requirements:**\n- about.edit required (People's data > About > Edit selected employees' About sections)\n- Service user must be in scope for the employee\n\n**Important Note:**\nAvatar editing is restricted based on the About category permission.\nTo allow the service user to upload/modify avatars, you need to enable the permission:\n\"People's data > About > Edit selected employees' About sections\"\n\n**Behavior:**\n- Updates the avatar URL in the employee's root/about record\n- Creates a root record if it doesn't exist\n- Validates the image URL format (must start with http:// or https://)\n\n**Returns:**\n- Complete updated employee information in HiBob format\n\n**Example Request:**\n```json\n{\n  \"employeeId\": 12345,\n  \"url\": \"https://cdn.example.com/avatars/employee123.jpg\"\n}\n```\n\n**Example Response:**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"john.doe@company.com\",\n    \"root\": {\n      \"displayName\": \"john.doe\",\n      \"avatarUrl\": \"https://cdn.example.com/avatars/employee123.jpg\"\n    }\n  }]\n}\n```\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employeeId": {
          "type": "integer",
          "description": "Employee ID (required path parameter - must be an integer)"
        },
        "url": {
          "type": "string",
          "description": "URL of the avatar image. Must start with http:// or https://. Required."
        }
      },
      "required": [
        "employeeId",
        "url"
      ]
    }
  },
  {
    "name": "update_employee_email",
    "description": "Update an employee's email address.\n\n**Endpoint**: PUT /v1/people/{id}/email\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nUpdates an employee's email address. The new email must be unique and not already in use by another employee.\n\n**Path Parameter:**\n- id: Employee ID (must be an integer)\n\n**Request Body:**\n- email: New email address (required)\n\n**Permission Requirements:**\n- root.edit required\n- Service user must be in scope for the employee\n\n**Behavior:**\n- Validates email format (must contain @ symbol)\n- Checks email uniqueness (no other employee can have the same email)\n- Updates the email in the person record\n- Returns updated employee information\n\n**Example Request:**\n```json\n{\n  \"id\": 12345,\n  \"email\": \"new.email@company.com\"\n}\n```\n\n**Example Response:**\n```json\n{\n  \"employees\": [{\n    \"id\": \"12345\",\n    \"firstName\": \"John\",\n    \"surname\": \"Doe\",\n    \"email\": \"new.email@company.com\",\n    \"displayName\": \"john.doe\"\n  }]\n}\n```\n\n**Error Responses:**\n- 400: Invalid email format\n- 403: Missing permissions or not in scope\n- 404: Employee not found\n- 409: Email already in use by another employee\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "Employee ID (required path parameter - must be an integer)"
        },
        "email": {
          "type": "string",
          "description": "New email address for the employee. Must be unique. Required."
        }
      },
      "required": [
        "id",
        "email"
      ]
    }
  },
  {
    "name": "get_all_positions_fields",
    "description": "Return a list of all fields of object type `position`.\n\nThis endpoint provides metadata describing the structure of Position objects, including field names, data types, relationships, and custom field definitions.\n\nResponse Structure:\n  - success: Boolean indicating operation success\n  - count: Total number of fields available for 'position' objects\n  - fields: Array of field metadata objects containing:\n      - id: Unique field identifier (e.g., 'position.id')\n      - name: Human-readable field name (e.g., 'Position ID')\n      - type: Data type (string, number, enum, date, boolean, json)\n      - required: Whether this field is mandatory\n      - description: Short explanation of the field purpose\n      - referenceTo: (Optional) Indicates if the field references another object (e.g., 'department', 'site', 'jobProfile')\n      - custom: Boolean indicating if the field is user-defined (custom)",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "description": "This endpoint does not require any parameters or request body."
    },
    "queryParams": []
  },
  {
    "name": "get_all_position_openings_fields",
    "description": "Return a list of all fields of object type `position opening`.\n\nThis endpoint provides metadata describing the structure of PositionOpening objects, including field names, data types, relationships, and custom field definitions.\n\nResponse Structure:\n  - success: Boolean indicating operation success (implicitly via HTTP status)\n  - fields: Array of field metadata objects containing:\n      - id: Unique field identifier (e.g., 'position_opening.id')\n      - name: Human-readable field name (e.g., 'Position Opening ID')\n      - type: Data type (string, number, enum, date, boolean, json)\n      - description: Short explanation of the field purpose\n      - jsonPath.root: The root object name (e.g., 'position_openings')\n      - jsonPath.rawData: The path to the value (e.g., 'position_openings.field_name')\n",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "description": "This endpoint does not require any parameters or request body."
    },
    "queryParams": []
  },
  {
    "name": "get_all_position_budget_fields",
    "description": "Return a list of all fields of object type `position budget`.\n\nThis endpoint provides metadata describing the structure of PositionBudget objects, including field names, data types, and descriptions.\n\nResponse Structure:\n  - success: Boolean indicating operation success (implicitly via HTTP status)\n  - fields: Array of field metadata objects containing:\n      - id: Unique field identifier (e.g., 'position_budget.id')\n      - name: Human-readable field name (e.g., 'Position Budget ID')\n      - type: Data type (string, number, enum, date, boolean, json)\n      - description: Short explanation of the field purpose\n      - jsonPath.root: The root object name (e.g., 'position_budget')\n      - jsonPath.rawData: The path to the value (e.g., 'position_budget.field_name')\n",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "description": "This endpoint does not require any parameters or request body."
    },
    "queryParams": []
  },
  {
    "name": "read_company_positions",
    "description": "Search Position records using dynamic filters and request only selected fields.\n\nThis endpoint allows consumers to:\n  - Select which fields should be returned\n  - Apply one or more filters using supported operators\n  - Optionally return human-readable string versions of field values\n\nResponse Structure:\n  - Each returned object contains the requested fields in '/position/{fieldName}' format\n  - Each field is returned as:\n         { \"value\": <raw database value>, \"humanReadable\": <optional readable string> }\n  - If includeHumanReadable=False, only `value` will be provided.\n\nSupported Operators:\n  - equals: Match values\n  - notEqual: Exclude values\nFilters Behavior:\n  filters is an array where each entry applies AND logic. For multi-value equals, IN logic is used.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "items": {
            "type": "string",
            "example": "/position/title"
          },
          "minItems": 1,
          "maxItems": 50,
          "description": "List of fields to include in the response. Must use the '/position/{fieldName}' format."
        },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "example": "/position/siteId",
                "description": "Field to filter on. Must start with '/position/'."
              },
              "operator": {
                "type": "string",
                "enum": [
                  "equals",
                  "notEqual"
                ],
                "description": "Comparison operator to apply."
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Values to compare against."
              }
            },
            "required": [
              "fieldId",
              "operator",
              "values"
            ]
          },
          "description": "Array of filter conditions. All filters are combined using AND logic."
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false,
          "description": "If true, also returns human-readable string versions of field values."
        }
      }
    },
    "queryParams": []
  },
  {
    "name": "read_position_openings",
    "description": "Search Position Opening records using dynamic filters and request only selected fields.\n\nThis endpoint allows consumers to:\n  - Select which fields should be returned using '/positionOpening/{fieldName}' format\n  - Apply one or more filters using supported operators ('equals', 'notEqual')\n  - Optionally include human-readable field values in the response\n  - Use cursor-based pagination for large result sets\n\nResponse Structure:\n  - Each returned object contains the requested fields keyed by '/positionOpening/{fieldName}'\n  - If includeHumanReadable=true, each field is returned as:\n         { \"value\": <raw_value>, \"humanReadable\": <converted_value> }\n  - If includeHumanReadable=False, fields return only the raw value.\n\nPagination Behavior:\n  - limit controls how many records to return per page (1-100, default 100)\n  - cursor is an opaque string representing where to continue the next page\n  - The response will include a next cursor when additional data is available",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "items": {
            "type": "string",
            "example": "/positionOpening/id"
          },
          "minItems": 1,
          "maxItems": 50,
          "description": "List of fields to include in the response. Must use the '/positionOpening/{fieldName}' format."
        },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "example": "/positionOpening/status",
                "description": "Field to filter on. Must start with '/positionOpening/'."
              },
              "operator": {
                "type": "string",
                "enum": [
                  "equals",
                  "notEqual"
                ],
                "description": "Comparison operator to apply."
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Values to compare against. Must contain at least 1 non-empty string."
              }
            },
            "required": [
              "fieldId",
              "operator",
              "values"
            ]
          },
          "description": "Filters are combined using AND logic. Multi-value equals maps to SQL IN()."
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false,
          "description": "If true, returns both raw and human-readable values for each field."
        },
        "pagination": {
          "type": "object",
          "properties": {
            "limit": {
              "type": "number",
              "default": 100,
              "minimum": 1,
              "maximum": 100,
              "description": "Max number of results per page."
            },
            "cursor": {
              "type": "string",
              "nullable": true,
              "description": "Opaque cursor string to continue paginated results. Omit or null for first page."
            }
          },
          "required": []
        }
      }
    },
    "queryParams": []
  },
  {
    "name": "read_position_budgets",
    "description": "Search Position Budget records using dynamic filters and return only selected fields.\n\nThis endpoint supports:\n  - Selecting a custom subset of fields using the '/positionBudget/{fieldName}' format\n  - Applying multiple AND-based filters using supported comparison operators\n  - Optionally including human-readable text values (useful for enums and lookups)\n  - Cursor-based pagination for large datasets\n\nResponse Format:\n  - Each returned row is represented as an object containing only the requested fields\n  - If includeHumanReadable=true:\n         { \"value\": <raw database value>, \"humanReadable\": <string version> }\n  - If includeHumanReadable=False:\n         { \"value\": <raw database value> }\n\nPagination:\n  - 'limit' sets max row count per request (1-100, default 100)\n  - 'cursor' indicates where to continue from in subsequent requests\n  - The response includes 'next_cursor' when more data is available",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "array",
          "items": {
            "type": "string",
            "example": "/positionBudget/budgetAmount"
          },
          "minItems": 1,
          "maxItems": 50,
          "description": "List of fields to include. Must start with '/positionBudget/'."
        },
        "filters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fieldId": {
                "type": "string",
                "example": "/positionBudget/fiscalYear",
                "description": "Field to filter on. Must start with '/positionBudget/'."
              },
              "operator": {
                "type": "string",
                "enum": [
                  "equals",
                  "notEqual",
                  "greaterThan",
                  "lessThan",
                  "in",
                  "notIn"
                ],
                "description": "Comparison operator."
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "minItems": 1,
                "description": "Values to compare with. Multi-value equals = SQL IN()."
              }
            },
            "required": [
              "fieldId",
              "operator",
              "values"
            ]
          },
          "description": "Filter conditions. All filters are combined using AND logic."
        },
        "includeHumanReadable": {
          "type": "boolean",
          "default": false,
          "description": "If true, returns both raw and human-readable value formats."
        },
        "pagination": {
          "type": "object",
          "properties": {
            "limit": {
              "type": "number",
              "default": 100,
              "minimum": 1,
              "maximum": 100,
              "description": "Maximum number of results to return."
            },
            "cursor": {
              "type": "string",
              "nullable": true,
              "description": "Opaque cursor token used to resume pagination."
            }
          }
        }
      },
      "required": [
        "fields"
      ]
    },
    "queryParams": []
  },
  {
    "name": "create_positions",
    "description": "Create one or more Position records including required Position Opening, and optional Position Budget. Mirrors HiBob Workforce Planning Create Positions API. Up to 10 positions per request.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "items": {
          "type": "array",
          "description": "A list of position creation entries (max 10).",
          "maxItems": 10,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "position"
                ],
                "default": "position",
                "description": "Must always be `position`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style field mapping. Keys must start with `/position/`. Nested values for Opening and Budget must use `.fields`.",
                "additionalProperties": {
                  "oneOf": [
                    {
                      "type": "object",
                      "description": "Simple field map",
                      "properties": {
                        "value": {}
                      },
                      "required": [
                        "value"
                      ]
                    },
                    {
                      "type": "object",
                      "description": "Nested Position Opening or Position Budget",
                      "properties": {
                        "fields": {
                          "type": "object",
                          "description": "Subfield mapping",
                          "additionalProperties": {
                            "type": "object",
                            "properties": {
                              "value": {}
                            },
                            "required": [
                              "value"
                            ]
                          }
                        }
                      },
                      "required": [
                        "fields"
                      ]
                    }
                  ]
                },
                "example": {
                  "/position/jobProfile": {
                    "value": 789
                  },
                  "/position/department": {
                    "value": "Engineering"
                  },
                  "/position/positionOpening": {
                    "fields": {
                      "/positionOpening/positionOpeningName": {
                        "value": "Software Engineer"
                      },
                      "/positionOpening/expectedStartDate": {
                        "value": "2025-04-30"
                      }
                    }
                  },
                  "/position/positionBudget": {
                    "fields": {
                      "/positionBudget/expectedBaseSalaryCurrencyValue": {
                        "value": 50000
                      },
                      "/positionBudget/salaryPayPeriod": {
                        "value": "Monthly"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "create_position_openings",
    "description": "Create one or more Position Opening records under an existing Position. Mirrors HiBob Workforce Planning Create Position Openings API. Up to 10 openings can be created per request.\n\nRequired:\n  - 'positionId' must reference an existing Position record\n  - Each item requires at least '/positionOpening/expectedStartDate'\n\nResponse Format:\n  - Returns list of created positionOpeningIds",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position under which these opening(s) will be created."
        },
        "items": {
          "type": "array",
          "description": "List of position openings to create (max 10).",
          "maxItems": 10,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "positionOpening"
                ],
                "default": "positionOpening",
                "description": "Must always be `positionOpening`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style field mapping. Keys must start with `/positionOpening/`.",
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "value": {}
                  },
                  "required": [
                    "value"
                  ]
                },
                "example": {
                  "/positionOpening/positionOpeningName": {
                    "value": "Backend Engineer Hire"
                  },
                  "/positionOpening/expectedStartDate": {
                    "value": "2025-02-01"
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "positionId",
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "update_position",
    "description": "Update an existing Position record in Workforce Planning. Mirrors HiBob PATCH Positions API.\n\nBehavior:\n  - Only fields included in the request will be updated (partial update / patch).\n  - Supports updating core position attributes such as name, department, site, jobProfile, managerPositionId, etc.\n\nRequired:\n  - 'positionId' must reference an existing Position record\n  - Each item must have objectType = 'position'\n\nResponse Format:\n  - Returns the updated positionId",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position under which these opening(s) will be created."
        },
        "items": {
          "type": "array",
          "description": "List of partial updates to apply (max 10).",
          "maxItems": 10,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "position"
                ],
                "default": "position",
                "description": "Must always be `position`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style fields. Keys must start with `/position/`.",
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "value": {}
                  },
                  "required": [
                    "value"
                  ]
                },
                "example": {
                  "/position/name": {
                    "value": "Senior Backend Lead"
                  },
                  "/position/managerPositionId": {
                    "value": 42
                  },
                  "/position/department": {
                    "value": "Engineering"
                  },
                  "/position/fte": {
                    "value": 1
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "positionId",
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "update_position_opening",
    "description": "Update an existing Position Opening record in Workforce Planning. Mirrors HiBob PATCH Position Openings API.\n\nBehavior:\n  - Only fields included in the request will be updated (patch / partial update).\n  - Supports updating opening name, expected start date, and recruitment status.\n\nRequired:\n  - 'positionId' must reference an existing Position.\n  - 'positionOpeningId' must reference an existing Position Opening under that Position.\n  - 'objectType' must be 'positionOpening'.\n  - '/positionOpening/expectedStartDate' is required when updating.\n\nResponse Format:\n  - Returns the updated positionOpeningId.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position under which these opening(s) will be created."
        },
        "positionOpeningId": {
          "type": "integer",
          "default": 0,
          "example": 987,
          "description": "The ID of the specific Position Opening to delete."
        },
        "items": {
          "type": "array",
          "description": "List of updates to apply. Only one is allowed.",
          "maxItems": 1,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "positionOpening"
                ],
                "default": "positionOpening",
                "description": "Must always be `positionOpening`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style fields. Keys must start with `/positionOpening/`.",
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "value": {}
                  },
                  "required": [
                    "value"
                  ]
                },
                "example": {
                  "/positionOpening/positionOpeningName": {
                    "value": "Frontend Developer - Q2"
                  },
                  "/positionOpening/expectedStartDate": {
                    "value": "2025-04-15"
                  },
                  "/positionOpening/recruitmentStatus": {
                    "value": "open"
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "positionId",
        "positionOpeningId",
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "delete_position_opening",
    "description": "Delete an existing Position Opening in Workforce Planning. Mirrors HiBob DELETE Position Opening API.\n\nBehavior:\n  - Permanently removes a position opening record under the specified Position.\n  - Operation will fail if the Position or Position Opening does not exist.\n\nRequired:\n  - 'positionId' must reference an existing Position.\n  - 'positionOpeningId' must reference an existing Position Opening under that Position.\n\nResponse Format:\n  - Returns the deleted positionOpeningId.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position under which these opening(s) will be created."
        },
        "positionOpeningId": {
          "type": "integer",
          "default": 0,
          "example": 987,
          "description": "The ID of the specific Position Opening to delete."
        }
      },
      "required": [
        "positionId",
        "positionOpeningId"
      ],
      "additionalProperties": false
    },
    "queryParams": []
  },
  {
    "name": "create_position_budget",
    "description": "Create a Position Budget entry for a given Position. Mirrors HiBob POST Position Budget API.\n\nBehavior:\n  - Creates a new Position Budget record.\n  - Supports setting salary pay period, currency, and cost values.\n  - Links the created budget to the specified Position.\n\nRequired:\n  - 'positionId' must reference an existing Position.\n  - 'objectType' must be 'positionBudget'.\n  - '/positionBudget/salaryPayPeriod' and '/positionBudget/currency' are required.\n\nResponse Format:\n  - Returns the created positionBudgetId.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position for which the Budget is being created."
        },
        "items": {
          "type": "array",
          "description": "List of budget objects to create. Only one is allowed.",
          "maxItems": 1,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "positionBudget"
                ],
                "default": "positionBudget",
                "description": "Must always be `positionBudget`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style budget fields. Keys must start with `/positionBudget/`.",
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "value": {}
                  },
                  "required": [
                    "value"
                  ]
                },
                "example": {
                  "/positionBudget/salaryPayPeriod": {
                    "value": "Monthly"
                  },
                  "/positionBudget/currency": {
                    "value": "USD"
                  },
                  "/positionBudget/expectedBaseSalaryCurrencyValue": {
                    "value": 50000
                  },
                  "/positionBudget/totalPositionCostCurrencyValue": {
                    "value": 60000
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "positionId",
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "update_position_budget",
    "description": "Update an existing Position Budget record in Workforce Planning. Mirrors HiBob PATCH Position Budget API.\n\nBehavior:\n  - Performs a partial update on the specified position budget.\n  - Only fields included in the request payload will be modified.\n  - Supports updating salary values, pay period, variable pay structure, and currency.\n\nRequired:\n  - 'positionId' must reference an existing Position.\n  - 'positionBudgetId' must reference an existing Position Budget tied to that Position.\n  - 'objectType' must be 'positionBudget'.\n  - Fields must be provided using HiBob path-mapped format (e.g. '/positionBudget/currency').\n\nResponse Format:\n  - Returns the updated positionBudgetId.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 1234,
          "description": "The Position that owns the budget being updated."
        },
        "positionBudgetId": {
          "type": "integer",
          "example": 4567,
          "description": "The ID of the specific Position Budget to update."
        },
        "items": {
          "type": "array",
          "description": "List of updates to apply. Only one item is allowed.",
          "maxItems": 1,
          "items": {
            "type": "object",
            "required": [
              "objectType",
              "fields"
            ],
            "properties": {
              "objectType": {
                "type": "string",
                "enum": [
                  "positionBudget"
                ],
                "default": "positionBudget",
                "description": "Must always be `positionBudget`."
              },
              "fields": {
                "type": "object",
                "description": "Dynamic HiBob-style budget fields. Keys must start with `/positionBudget/`.",
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "value": {}
                  },
                  "required": [
                    "value"
                  ]
                },
                "example": {
                  "/positionBudget/expectedBaseSalaryCurrencyValue": {
                    "value": 75000
                  },
                  "/positionBudget/currency": {
                    "value": "USD"
                  },
                  "/positionBudget/salaryPayPeriod": {
                    "value": "Annual"
                  },
                  "/positionBudget/expectedVariablePayCurrencyValue": {
                    "value": 5000
                  },
                  "/positionBudget/variablePayPeriod": {
                    "value": "Annual"
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "positionId",
        "positionBudgetId",
        "items"
      ]
    },
    "queryParams": []
  },
  {
    "name": "cancel_position",
    "description": "Cancel an existing Position in Workforce Planning. Mirrors HiBob PATCH Cancel Position API.\n\nBehavior:\n  - Updates the Position's status to 'cancelled'.\n  - Does NOT delete the Position record.\n  - Operation will fail if the Position does not exist.\n\nRequired:\n  - 'positionId' must reference an existing Position.\n\nResponse Format:\n  - Returns the cancelled positionId.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "positionId": {
          "type": "integer",
          "example": 4567,
          "description": "The Position to cancel."
        }
      },
      "additionalProperties": false
    },
    "queryParams": []
  },
  {
    "name": "get_onboarding_wizards",
    "description": "Get a summary of all onboarding wizards.\n\n**Endpoint**: GET /v1/onboarding/wizards\n**Headers required**: X-Hibob-User-Token, X-Database-Id\n\nRetrieves all configured onboarding/welcome wizards that can be assigned to new employees.\n\n**Query Parameters:**\n- active_only: If true, returns only active wizards (default: false)\n\n**Response:**\nReturns a list of wizard objects containing:\n- id: Wizard unique identifier\n- name: Wizard name\n- description: Wizard description\n- category: Wizard category (e.g., \"welcome\", \"manager\", \"it_setup\")\n- isActive: Whether the wizard is currently active\n- isDefault: Whether this is the default wizard\n- tasks: List of tasks included in the wizard\n- config: Additional configuration\n- usageCount: Number of times this wizard has been assigned\n- createdBy: Who created the wizard\n- createdAt: Creation timestamp\n- updatedAt: Last update timestamp\n\n**Example:**\n```json\n{\n  \"active_only\": true\n}\n```\n\n**Example Response:**\n```json\n{\n  \"wizards\": [\n    {\n      \"id\": 1,\n      \"name\": \"Standard Welcome Wizard\",\n      \"description\": \"Default onboarding wizard for new employees\",\n      \"category\": \"welcome\",\n      \"isActive\": true,\n      \"isDefault\": true,\n      \"tasks\": [\n        {\"id\": 1, \"title\": \"Complete profile\", \"type\": \"form\"},\n        {\"id\": 2, \"title\": \"Read employee handbook\", \"type\": \"document\"}\n      ],\n      \"config\": {},\n      \"usageCount\": 25,\n      \"createdBy\": \"admin\",\n      \"createdAt\": \"2024-01-15T10:00:00Z\",\n      \"updatedAt\": \"2024-01-15T10:00:00Z\"\n    }\n  ],\n  \"total\": 1\n}\n```\n",
    "inputSchema": {
      "type": "object",
      "properties": {
        "active_only": {
          "type": "boolean",
          "description": "If true, return only active wizards",
          "default": false
        }
      },
      "required": []
    }
  },
  {
    "name": "get_bulk_people_work",
    "description": "List work history for a list of employees. Returns historical work entries from the work table.\n        \n        Supports cursor-based pagination for handling large datasets. You can filter by specific employee IDs \n        (comma-separated, max 200). If not provided, returns entries for all employees.\n        \n        Response includes results array, response_metadata with cursor, and errors array for permission issues.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 200,
          "default": 50,
          "description": "Number of table entries to include on each page of results"
        },
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null,
          "description": "Marker for the first item on the next page"
        },
        "employeeIds": {
          "type": "string",
          "description": "Comma separated list of employee IDs (max 200)"
        }
      },
      "required": []
    }
  },
  {
    "name": "get_bulk_lifecycle_history",
    "description": "List lifecycle status history for a list of employees. Returns historical lifecycle entries from the lifecycle table.\n        \n        Lifecycle entries track employee status changes (hired, active, terminated, on leave, etc.).\n        Supports cursor-based pagination. You can filter by specific employee IDs (comma-separated, max 200).\n        \n        Response includes results array with nested values, response_metadata with cursor, and errors array.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 200,
          "default": 50,
          "description": "Number of table entries to include on each page of results"
        },
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null,
          "description": "Marker for the first item on the next page"
        },
        "employeeIds": {
          "type": "string",
          "description": "Comma separated list of employee IDs (max 200)"
        }
      },
      "required": []
    }
  },
  {
    "name": "get_bulk_employment_history",
    "description": "List employment history for a list of employees. Returns historical employment entries from the employment table.\n        \n        Each employment entry includes the working pattern assigned to the employee (hourly or fortnightly schedules).\n        Supports cursor-based pagination. You can filter by specific employee IDs (comma-separated, max 200).\n        \n        Response includes results array with nested values, response_metadata with cursor, and errors array.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 200,
          "default": 50,
          "description": "Number of table entries to include on each page of results"
        },
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null,
          "description": "Marker for the first item on the next page"
        },
        "employeeIds": {
          "type": "string",
          "description": "Comma separated list of employee IDs (max 200)"
        }
      },
      "required": []
    }
  },
  {
    "name": "get_bulk_payroll_history",
    "description": "List payroll/salary history for a list of employees. Returns historical salary entries from the salaries table.\n        \n        Each entry includes base salary with currency, pay frequency, pay period, effective dates, and change tracking.\n        Supports cursor-based pagination. You can filter by specific employee IDs (comma-separated, max 200).\n        \n        Response includes results array with nested values, response_metadata with cursor, and errors array.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 200,
          "default": 50,
          "description": "Number of table entries to include on each page of results"
        },
        "cursor": {
          "type": [
            "string",
            "null"
          ],
          "default": null,
          "description": "Marker for the first item on the next page"
        },
        "employeeIds": {
          "type": "string",
          "description": "Comma separated list of employee IDs (max 200)"
        }
      },
      "required": []
    }
  },
  {
    "name": "search_actual_payments",
    "description": "Search actual payment records with flexible filtering and pagination. Requires at least an employeeId filter in all requests.\n        \n        You can filter by employeeId (max 200 IDs with 'equals' operator) and optionally by payDate (using 'greaterThanOrEquals' or 'lessThanOrEquals' operators with YYYY-MM-DD format). Supports cursor-based pagination with configurable limits (1-200, default 50).\n        \n        Response includes results array, response_metadata with cursor for pagination.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "filters": {
          "type": "array",
          "description": "Array of filter objects (must include employeeId filter)",
          "items": {
            "type": "object",
            "properties": {
              "fieldPath": {
                "type": "string",
                "description": "Field to filter by",
                "enum": [
                  "employeeId",
                  "payDate"
                ]
              },
              "operator": {
                "type": "string",
                "description": "Comparison operator",
                "enum": [
                  "equals",
                  "greaterThanOrEquals",
                  "lessThanOrEquals"
                ]
              },
              "values": {
                "type": "array",
                "description": "Array of employee IDs (for employeeId filter, max 200)",
                "items": {
                  "type": "string"
                },
                "maxItems": 200
              },
              "value": {
                "type": "string",
                "description": "Date value for payDate filter (YYYY-MM-DD)",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
              }
            },
            "required": [
              "fieldPath",
              "operator"
            ]
          },
          "minItems": 1
        },
        "pagination": {
          "type": "object",
          "description": "Pagination parameters",
          "properties": {
            "limit": {
              "type": "integer",
              "description": "Number of results per page (1-200, default 50)",
              "minimum": 1,
              "maximum": 200,
              "default": 50
            },
            "cursor": {
              "type": "string",
              "description": "Cursor for next page from response_metadata"
            }
          }
        }
      },
      "required": [
        "filters"
      ]
    }
  },
  {
    "name": "get_employee_work_history",
    "description": "Get work history for a specific employee by ID.\n        \n        Returns a flat array of work history entries including department, title, reports-to information,\n        effective dates, and change tracking. Each entry represents a work change event (promotion, transfer, etc.).",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_work_entry",
    "description": "Create a new work entry for an employee. Requires effectiveDate (YYYY-MM-DD) and either site or siteId to avoid conflicts with existing entries on the same date and site.\n        \n        Optionally include title, department, reportsTo (manager details with id, firstName, surname, email, displayName), reason, and customColumns. Entry must not conflict with another on the same effective date and site.\n        \n        Returns the created work entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date this entry becomes effective (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "site": {
          "type": "string",
          "description": "Site name (must provide either site or siteId)"
        },
        "siteId": {
          "type": "integer",
          "description": "Site ID (must provide either site or siteId)"
        },
        "title": {
          "type": "string",
          "description": "Job title"
        },
        "department": {
          "type": "string",
          "description": "Department name"
        },
        "reason": {
          "type": "string",
          "description": "Reason for this change"
        },
        "reportsTo": {
          "type": "object",
          "description": "Manager details",
          "properties": {
            "id": {
              "type": "string",
              "description": "Manager's employee ID (REQUIRED if reportsTo is provided)"
            },
            "firstName": {
              "type": "string"
            },
            "surname": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "displayName": {
              "type": "string"
            }
          }
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "effectiveDate"
      ]
    }
  },
  {
    "name": "update_employee_work_entry",
    "description": "Update a work entry in the employee's work history. Performs full replacement by default, overwriting the entire entry with provided data - any omitted columns will be cleared.\n        \n        Best practice: Read the complete work entry first, modify needed fields, then submit the full entry. Requires effectiveDate (YYYY-MM-DD). Optionally include title, department, site, siteId, reportsTo, workChangeType, reason, and customColumns. Legacy patchUpdate flag available but not recommended.\n        \n        Returns the updated work entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The work entry ID to update as a string (obtain from GET /people/{id}/work endpoint)"
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date this entry becomes effective (YYYY-MM-DD format) - MANDATORY",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "title": {
          "type": "string",
          "description": "Job title"
        },
        "department": {
          "type": "string",
          "description": "Department name"
        },
        "site": {
          "type": "string",
          "description": "Site name"
        },
        "siteId": {
          "type": "integer",
          "description": "Site ID"
        },
        "workChangeType": {
          "type": "string",
          "description": "Type of change from Change Type list"
        },
        "reason": {
          "type": "string",
          "description": "Reason for this change"
        },
        "reportsTo": {
          "type": "object",
          "description": "Manager details",
          "properties": {
            "id": {
              "type": "string",
              "description": "Manager's employee ID"
            },
            "firstName": {
              "type": "string"
            },
            "surname": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "displayName": {
              "type": "string"
            }
          }
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        },
        "patchUpdate": {
          "type": "boolean",
          "default": false,
          "description": "Legacy flag for partial updates (not recommended)"
        }
      },
      "required": [
        "id",
        "entry_id",
        "effectiveDate"
      ]
    }
  },
  {
    "name": "delete_employee_work_entry",
    "description": "Delete a work entry from an employee's work history using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist with can_be_deleted=true, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The work entry ID to delete as a string (obtain from GET /people/{id}/work endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_employee_employment_history",
    "description": "Get employment history for a specific employee by ID.\n        \n        Returns a flat array of employment history entries including employment type, contract type, \n        employment status, working patterns, effective dates, and change tracking.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_employment_entry",
    "description": "Create a new employment entry for an employee. Requires effectiveDate (YYYY-MM-DD) and must not conflict with another entry on the same date.\n        \n        Optionally include reason, personalWorkingPatternType, actualWorkingPattern, contract (Full-Time/Part-Time/Shifts), type (Permanent/Temporary/Apprentice/Contractor), salaryPayType (Salaries/Hourly), flsaCode (Exempt/Non-Exempt), weeklyHours, fte, calendar details, and customColumns.\n        \n        Returns the created employment entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date this entry becomes effective (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "reason": {
          "type": "string",
          "description": "Reason for this change"
        },
        "personalWorkingPatternType": {
          "type": "string",
          "description": "Working pattern type",
          "enum": [
            "none",
            "custom",
            "library",
            "flexible"
          ]
        },
        "contract": {
          "type": "string",
          "description": "Contract type",
          "enum": [
            "Full-Time",
            "Part-Time",
            "Shifts"
          ]
        },
        "type": {
          "type": "string",
          "description": "Employment type",
          "enum": [
            "Permanent",
            "Temporary",
            "Apprentice",
            "Contractor",
            "custom value"
          ]
        },
        "salaryPayType": {
          "type": "string",
          "description": "Salary pay type",
          "enum": [
            "Salaries",
            "Hourly"
          ]
        },
        "flsaCode": {
          "type": "string",
          "description": "FLSA code",
          "enum": [
            "Exempt",
            "Non-Exempt"
          ]
        },
        "weeklyHours": {
          "type": "number",
          "description": "Weekly hours based on working pattern"
        },
        "fte": {
          "type": "number",
          "description": "FTE percentage for this entry"
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "effectiveDate"
      ]
    }
  },
  {
    "name": "update_employee_employment_entry",
    "description": "Update an employment entry in the employee's employment history using PUT semantics with FULL REPLACEMENT.\n        \n        CRITICAL WARNING: This endpoint overwrites the ENTIRE employment entry. Any fields NOT included in your request will be CLEARED (set to null/empty values).\n        \n        BEST PRACTICE: Always read the complete entry first with get_employee_employment_history, modify the needed fields, then submit the COMPLETE entry back with all fields populated.\n        \n        Requires effectiveDate (YYYY-MM-DD). Include all fields you want to preserve: reason, personalWorkingPatternType, actualWorkingPattern, contract, type, salaryPayType, flsaCode, weeklyHours, fte, calendar details, and customColumns.\n        \n        Returns the updated employment entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The employment entry ID to update as a string (obtain from GET /people/{id}/employment endpoint)"
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date this entry becomes effective (YYYY-MM-DD format) - MANDATORY",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "reason": {
          "type": "string",
          "description": "Reason for this change"
        },
        "personalWorkingPatternType": {
          "type": "string",
          "description": "Working pattern type",
          "enum": [
            "none",
            "custom",
            "library",
            "flexible"
          ]
        },
        "actualWorkingPattern": {
          "type": "object",
          "description": "Active working pattern (hourly/biweekly/flexible)"
        },
        "contract": {
          "type": "string",
          "description": "Contract type",
          "enum": [
            "Full-Time",
            "Part-Time",
            "Shifts"
          ]
        },
        "type": {
          "type": "string",
          "description": "Employment type",
          "enum": [
            "Permanent",
            "Temporary",
            "Apprentice",
            "Contractor",
            "custom value"
          ]
        },
        "salaryPayType": {
          "type": "string",
          "description": "Salary pay type",
          "enum": [
            "Salaries",
            "Hourly"
          ]
        },
        "flsaCode": {
          "type": "string",
          "description": "FLSA code",
          "enum": [
            "Exempt",
            "Non-Exempt"
          ]
        },
        "weeklyHours": {
          "type": "number",
          "description": "Weekly hours based on working pattern"
        },
        "fte": {
          "type": "number",
          "description": "FTE percentage for this entry"
        },
        "calendarName": {
          "type": "string",
          "description": "Selected Holiday calendar"
        },
        "calendarId": {
          "type": "integer",
          "description": "Selected Holiday calendar ID"
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "entry_id",
        "effectiveDate"
      ]
    }
  },
  {
    "name": "delete_employee_employment_entry",
    "description": "Delete an employment entry from an employee's employment history using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist with can_be_deleted=true, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The employment entry ID to delete as a string (obtain from GET /people/{id}/employment endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_employee_lifecycle_history",
    "description": "Get lifecycle status history for a specific employee by ID.\n        \n        Returns a flat array of lifecycle history entries tracking employee status changes over time.\n        Includes status, employee status, work change type, reason, effective dates, and change tracking.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "get_employee_payroll_history",
    "description": "Get salary/payroll history for a specific employee by ID.\n        \n        Returns a flat array of salary history entries including base salary (value and currency), \n        pay frequency, pay period, work change type, effective dates, and change tracking.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_salary_entry",
    "description": "Create a new salary entry for an employee. Requires base amount object (currency and value) and payPeriod (Annual/Hourly/Daily/Weekly/Monthly). Must not conflict with another entry on the same effective date.\n        \n        Optionally include effectiveDate (YYYY-MM-DD), payFrequency (Monthly/Semi Monthly/Weekly/Bi-Weekly), workChangeType, change details (reason, changedBy, changedById), and customColumns.\n        \n        Returns the created salary entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "base": {
          "type": "object",
          "description": "Salary amount object (REQUIRED)",
          "properties": {
            "currency": {
              "type": "string",
              "description": "Three-letter currency code (e.g., USD, EUR)"
            },
            "value": {
              "type": "number",
              "description": "Salary value"
            }
          },
          "required": [
            "currency",
            "value"
          ]
        },
        "payPeriod": {
          "type": "string",
          "description": "Period for salary entry (REQUIRED)",
          "enum": [
            "Annual",
            "Hourly",
            "Daily",
            "Weekly",
            "Monthly"
          ]
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date this entry becomes effective (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "payFrequency": {
          "type": "string",
          "description": "How often paid",
          "enum": [
            "Monthly",
            "Semi Monthly",
            "Weekly",
            "Bi-Weekly"
          ]
        },
        "workChangeType": {
          "type": "string",
          "description": "Type of change from Change Type list"
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "base",
        "payPeriod"
      ]
    }
  },
  {
    "name": "delete_employee_salary_entry",
    "description": "Delete a salary entry from the employee's salary history using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist with can_be_deleted=true, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The salary entry ID to delete as a string (obtain from GET /people/{id}/salaries endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_payroll_history",
    "description": "Read payroll tables history combining employee and work tables. Legacy endpoint maintained for backward compatibility but planned for deprecation - use alternative employee table endpoints where possible.\n        \n        Supports filtering by department and optionally including inactive employees via showInactive flag.\n        \n        Returns employees with combined work information.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "department": {
          "type": "string",
          "description": "Filter payroll for specific department"
        },
        "showInactive": {
          "type": "boolean",
          "default": false,
          "description": "Whether to include inactive employees in the response"
        }
      },
      "required": []
    }
  },
  {
    "name": "get_employee_equity_grants",
    "description": "Get equity grants for a specific employee by ID.\n        \n        Returns equity grant entries including stock options, RSUs, and other equity compensation.\n        Each entry includes equity type, quantity (supports fractional shares), grant type, grant number,\n        grant date, grant status, exercise price (for options), vesting details (commencement date, term, schedule),\n        vested quantity, option expiration, and reason for grant.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_equity_grant",
    "description": "Create a new equity grant for an employee. Requires effectiveDate (YYYY-MM-DD), quantity (supports fractional shares), and equityType (e.g., \"Stock Options\", \"RSU\").\n        \n        exercisePrice is optional, but if provided, both currency (exactly 3 uppercase letters like USD, EUR, GBP) and value (positive number) are required.\n        \n        Optionally include grantType (Initial Grant/Merit Grant), grantNumber, grantDate, grantStatus (Granted/Pending Approval), vesting details (commencementDate, term, schedule in months), optionExpiration, reason, consentNumber, and customColumns.\n        \n        Returns the created equity grant in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date when grant becomes effective (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "quantity": {
          "type": "number",
          "description": "Number of shares granted (supports fractional shares)"
        },
        "equityType": {
          "type": "string",
          "description": "Type of equity (e.g., Stock Options, RSU)"
        },
        "grantType": {
          "type": "string",
          "description": "Grant type",
          "enum": [
            "Initial Grant",
            "Merit Grant"
          ]
        },
        "grantNumber": {
          "type": "string",
          "description": "Unique grant identifier"
        },
        "grantDate": {
          "type": "string",
          "description": "When grant was made (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "grantStatus": {
          "type": "string",
          "description": "Grant status",
          "enum": [
            "Granted",
            "Pending Approval"
          ]
        },
        "exercisePrice": {
          "type": "object",
          "description": "Exercise price for options (REQUIRED)",
          "properties": {
            "currency": {
              "type": "string",
              "description": "Three-letter currency code (e.g., USD, EUR, GBP) - REQUIRED",
              "minLength": 3,
              "maxLength": 3,
              "pattern": "^[A-Z]{3}$"
            },
            "value": {
              "type": "number",
              "description": "Exercise price value - REQUIRED",
              "exclusiveMinimum": 0
            }
          },
          "required": [
            "currency",
            "value"
          ]
        },
        "vestingCommencementDate": {
          "type": "string",
          "description": "Vesting start date (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "vestingTerm": {
          "type": "string",
          "description": "Vesting terms description"
        },
        "vestingSchedule": {
          "type": "integer",
          "description": "Number of months for vesting"
        },
        "optionExpiration": {
          "type": "string",
          "description": "When options expire (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "reason": {
          "type": "string",
          "description": "Reason for the grant"
        },
        "consentNumber": {
          "type": "string",
          "description": "Consent/agreement number"
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "effectiveDate",
        "quantity",
        "equityType"
      ]
    }
  },
  {
    "name": "update_employee_equity_grant",
    "description": "Update an equity grant in the employee's equity grants table using PUT semantics with FULL REPLACEMENT, matching HiBob's `PUT /people/{id}/equities/{entry_id}` endpoint.\n\n        CRITICAL WARNING: This endpoint overwrites the ENTIRE equity grant entry. Any fields NOT included in your request will be CLEARED (set to null/empty values), as documented in HiBob's API reference for updating an equity grant [`PUT /people/{id}/equities/{entry_id}`](https://apidocs.hibob.com/reference/put_people-id-equities-entry-id).\n\n        BEST PRACTICE: Always read the complete equity grant entry first (via get_employee_equity_grants), modify only the needed fields in your client, and then submit the COMPLETE entry back with ALL fields you want to preserve.\n\n        Per HiBob documentation, the following body fields are REQUIRED for updates: effectiveDate, quantity, equityType. All other fields are optional, but any omitted fields will be cleared by the PUT operation. For option-type grants, exercisePrice should follow the same behavior as the create equity grant endpoint (optional object, but if provided both currency and value are required).\n\n        Returns the updated equity grant in values array format ({\"values\": [...]}) consistent with the GET equities grants endpoint.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The equity grant entry ID to update as a string (obtain from GET /people/{id}/equities endpoint)"
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date when grant becomes effective (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "equityType": {
          "type": "string",
          "description": "Type of equity (e.g., Stock Options, RSU)"
        },
        "quantity": {
          "type": "number",
          "description": "Quantity of shares (supports fractional, must be positive)"
        },
        "grantType": {
          "type": "string",
          "description": "Grant type",
          "enum": [
            "Initial Grant",
            "Merit Grant"
          ]
        },
        "grantNumber": {
          "type": "number",
          "description": "Grant identifier (must be positive)"
        },
        "grantDate": {
          "type": "string",
          "description": "When grant was made (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "grantStatus": {
          "type": "string",
          "description": "Grant status",
          "enum": [
            "Granted",
            "Pending Approval"
          ]
        },
        "exercisePrice": {
          "type": "object",
          "description": "Exercise price for options",
          "properties": {
            "currency": {
              "type": "string",
              "description": "Three-letter currency code (e.g., USD, EUR, GBP)"
            },
            "value": {
              "type": "number",
              "description": "Price value (must be positive)"
            }
          }
        },
        "vestingCommencementDate": {
          "type": "string",
          "description": "Vesting start date (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "vestingTerm": {
          "type": "string",
          "description": "Vesting terms description"
        },
        "vestingSchedule": {
          "type": "integer",
          "description": "Number of months for vesting"
        },
        "vestedQuantity": {
          "type": "number",
          "description": "Vested shares (supports fractional)"
        },
        "optionExpiration": {
          "type": "string",
          "description": "When options expire (YYYY-MM-DD)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "reason": {
          "type": "string",
          "description": "Reason for grant"
        },
        "consentNumber": {
          "type": "string",
          "description": "Consent number"
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id",
        "entry_id",
        "effectiveDate",
        "quantity",
        "equityType"
      ]
    }
  },
  {
    "name": "delete_employee_equity_grant",
    "description": "Delete an equity grant for an employee using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist with can_be_deleted=true, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The equity grant entry ID to delete as a string (obtain from GET /people/{id}/equities endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_employee_variable_payments",
    "description": "Get variable payment history for a specific employee by ID.\n        \n        Returns variable compensation entries including bonuses, commissions, and other variable pay.\n        Each entry includes amount (value and currency), percentage breakdowns (company, department, individual),\n        payout type, payment period, effective dates, and change tracking.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_variable_payment",
    "description": "Create a new variable payment for an employee. Requires effectiveDate (YYYY-MM-DD), amount (value and currency), variableType (only \"amount\" supported), and paymentPeriod (Annual/Half-Yearly/Quarterly/Monthly).\n        \n        Optionally include companyPercent, departmentPercent, individualPercent, and reason. Currency must be 3-letter uppercase code (USD, EUR, GBP).\n        \n        Returns the created variable payment in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "effectiveDate": {
          "type": "string",
          "description": "Date when payment becomes effective (YYYY-MM-DD format) - REQUIRED",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "amount": {
          "type": "object",
          "description": "Payment amount with value and currency - REQUIRED",
          "properties": {
            "value": {
              "type": "number",
              "description": "Payment amount value"
            },
            "currency": {
              "type": "string",
              "description": "Three-letter currency code (e.g., USD, EUR, GBP)",
              "pattern": "^[A-Z]{3}$"
            }
          },
          "required": [
            "value",
            "currency"
          ]
        },
        "variableType": {
          "type": "string",
          "description": "Type of variable payment (only 'amount' is supported) - REQUIRED",
          "enum": [
            "amount"
          ]
        },
        "paymentPeriod": {
          "type": "string",
          "description": "Payment period - REQUIRED",
          "enum": [
            "Annual",
            "Half-Yearly",
            "Quarterly",
            "Monthly"
          ]
        },
        "companyPercent": {
          "type": "number",
          "description": "Company performance percentage"
        },
        "departmentPercent": {
          "type": "number",
          "description": "Department performance percentage"
        },
        "individualPercent": {
          "type": "number",
          "description": "Individual performance percentage"
        },
        "reason": {
          "type": "string",
          "description": "Reason for the variable payment"
        }
      },
      "required": [
        "id",
        "effectiveDate",
        "amount",
        "variableType",
        "paymentPeriod"
      ]
    }
  },
  {
    "name": "delete_employee_variable_payment",
    "description": "Delete a variable payment record for an employee using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist with can_be_deleted=true, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The variable payment entry ID to delete as a string (obtain from GET /people/{id}/variable endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_employee_training_records",
    "description": "Get training records for a specific employee by ID.\n        \n        Returns a flat array of training record entries including training name, description, cost (value and currency),\n        status (Completed, In Progress, Planned), frequency, start/end dates, and document IDs for certificates.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_training_record",
    "description": "Create a new training record for an employee. All fields are optional including name, description, cost (value and currency), status (Completed/In Progress/Planned), frequency (Once/Weekly/Monthly/Yearly), startDate and endDate (YYYY-MM-DD format, date only, not datetime), documentId (must be non-negative if provided), and customColumns.\n        \n        Currency must be exactly 3 uppercase letters (USD, EUR, GBP). Dates must be in YYYY-MM-DD format (date only, not datetime). documentId must be a non-negative integer (>= 0) if provided.\n        \n        Returns the created training record in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "name": {
          "type": "string",
          "description": "Training name from Training Name list"
        },
        "description": {
          "type": "string",
          "description": "Further description about the training entry"
        },
        "cost": {
          "type": "object",
          "description": "Cost object with value and currency",
          "properties": {
            "value": {
              "type": "number",
              "description": "Cost value (double precision)"
            },
            "currency": {
              "type": "string",
              "description": "Three-letter currency code (e.g., USD, EUR, GBP)",
              "pattern": "^[A-Z]{3}$"
            }
          },
          "required": [
            "value",
            "currency"
          ]
        },
        "status": {
          "type": "string",
          "description": "Status of training entry (Completed, In Progress, Planned, etc.)"
        },
        "frequency": {
          "type": "string",
          "description": "Training frequency - MUST be one of: Once, Weekly, Monthly, Yearly",
          "enum": [
            "Once",
            "Weekly",
            "Monthly",
            "Yearly"
          ]
        },
        "startDate": {
          "type": "string",
          "description": "Training start date (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "endDate": {
          "type": "string",
          "description": "Training end date (YYYY-MM-DD format)",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "documentId": {
          "type": "integer",
          "description": "ID of document attached to this training entry (must be non-negative, >= 0)",
          "minimum": 0
        },
        "customColumns": {
          "type": "object",
          "description": "Custom org-specific columns"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "delete_employee_training_record",
    "description": "Delete a training record for an employee using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The training record entry ID to delete as a string (obtain from GET /people/{id}/training endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_employee_bank_accounts",
    "description": "Get bank account information for a specific employee by ID.\n        \n        Returns bank account entries for payroll processing including account type, routing number, \n        account number (masked), bank name, branch address, BIC/SWIFT, IBAN, allocation method,\n        amount/percentage for split payments, and bonus payment flag.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "create_employee_bank_account",
    "description": "Create a new bank account entry for an employee. Requires bankAccountType (Checking/Savings), accountNumber (min 4 characters), bankName, and branchAddress.\n        \n        Optionally include routingNumber (exactly 9 digits for US/Canada), accountNickname, bicOrSwift (8 or 11 alphanumeric), iban (15-34 characters), allocation (percent/amount/remaining), amount (required for percent or amount allocation), and useForBonus flag. Validates format for routing numbers, IBAN, and BIC/SWIFT codes.\n        \n        Returns the created bank account in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "bankAccountType": {
          "type": "string",
          "description": "Account type - REQUIRED",
          "enum": [
            "Checking",
            "Savings"
          ]
        },
        "accountNumber": {
          "type": "string",
          "description": "Account number (minimum 4 characters) - REQUIRED",
          "minLength": 4
        },
        "routingNumber": {
          "type": "string",
          "description": "Routing number (exactly 9 digits for US/Canada)",
          "pattern": "^\\d{9}$"
        },
        "accountNickname": {
          "type": "string",
          "description": "Account nickname"
        },
        "bankName": {
          "type": "string",
          "description": "Bank name"
        },
        "branchAddress": {
          "type": "string",
          "description": "Bank branch address"
        },
        "bicOrSwift": {
          "type": "string",
          "description": "BIC/SWIFT code (8 or 11 alphanumeric characters)",
          "pattern": "^[A-Z0-9]{8}$|^[A-Z0-9]{11}$"
        },
        "iban": {
          "type": "string",
          "description": "IBAN (15-34 characters, starts with country code + 2 digits)",
          "pattern": "^[A-Z]{2}\\d{2}[A-Z0-9]{11,30}$"
        },
        "allocation": {
          "type": "string",
          "description": "Salary portion allocation method",
          "enum": [
            "percent",
            "amount",
            "remaining"
          ]
        },
        "amount": {
          "type": "number",
          "description": "Amount or percentage value for allocation (must be positive, required if allocation is 'percent' or 'amount')",
          "exclusiveMinimum": 0
        },
        "useForBonus": {
          "type": "boolean",
          "description": "Whether account is used for bonuses"
        }
      },
      "required": [
        "id",
        "bankAccountType",
        "accountNumber",
        "bankName",
        "branchAddress"
      ]
    }
  },
  {
    "name": "update_employee_bank_account",
    "description": "Update a bank account entry in the employee's bank accounts table. Performs a PARTIAL update - only fields provided in the input will be updated; omitted fields will retain their existing values.\n        \n        All fields optional except id and entry_id. Optionally include bankAccountType, routingNumber (9 digits), accountNickname, accountNumber (min 4 chars), bankName, branchAddress, bicOrSwift (8 or 11 chars), iban (15-34 chars), allocation, amount, and useForBonus.\n        \n        Returns the updated bank account entry in values array format.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The bank account entry ID to update as a string (obtain from GET /people/{id}/bank-accounts endpoint)"
        },
        "bankAccountType": {
          "type": "string",
          "description": "Account type",
          "enum": [
            "Checking",
            "Savings"
          ]
        },
        "routingNumber": {
          "type": "string",
          "description": "Routing number (exactly 9 digits for US/Canada)",
          "pattern": "^\\d{9}$"
        },
        "accountNickname": {
          "type": "string",
          "description": "Account nickname"
        },
        "accountNumber": {
          "type": "string",
          "description": "Account number (minimum 4 characters)",
          "minLength": 4
        },
        "bankName": {
          "type": "string",
          "description": "Bank name"
        },
        "branchAddress": {
          "type": "string",
          "description": "Bank branch address"
        },
        "bicOrSwift": {
          "type": "string",
          "description": "BIC/SWIFT code (8 or 11 alphanumeric characters)",
          "pattern": "^[A-Z0-9]{8}$|^[A-Z0-9]{11}$"
        },
        "iban": {
          "type": "string",
          "description": "IBAN (15-34 characters, starts with country code + 2 digits)",
          "pattern": "^[A-Z]{2}\\d{2}[A-Z0-9]{11,30}$"
        },
        "allocation": {
          "type": "string",
          "description": "Salary portion allocation method",
          "enum": [
            "percent",
            "amount",
            "remaining"
          ]
        },
        "amount": {
          "type": "number",
          "description": "Amount or percentage value for allocation (must be positive)",
          "exclusiveMinimum": 0
        },
        "useForBonus": {
          "type": "boolean",
          "description": "Whether account is used for bonuses"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "delete_employee_bank_account",
    "description": "Delete a bank account entry from an employee's bank accounts table using soft delete. Marks the entry as deleted while preserving data for audit purposes.\n        \n        Entry must exist, not already be deleted, and belong to the specified employee. Soft-deleted entries won't appear in queries but remain in the database. Returns 404 \"Requested entry not found. Nothing was changed\" if entry doesn't exist.\n        \n        Returns success message with entry and employee IDs.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID (unique identifier)",
          "minLength": 1
        },
        "entry_id": {
          "type": "integer",
          "description": "The bank account entry ID to delete as a string (obtain from GET /people/{id}/bank-accounts endpoint)"
        }
      },
      "required": [
        "id",
        "entry_id"
      ]
    }
  },
  {
    "name": "get_docs_folders_metadata",
    "description": "Return a list of all document folders with metadata.\n\nThis endpoint retrieves the list of folders available for storing documents, including each folder’s ID, display name, and folder type.\n\nResponse Structure:\n  - Array of folder metadata objects containing:\n      - id: { value: Numeric folder ID }\n      - name: { value: Human-readable folder name }\n      - folderType: { value: One of 'shared', 'confidential', 'custom' }\n\nThis is a HiBob-compatible format used for determining target folder IDs when uploading documents.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "description": "This endpoint does not accept any input parameters or body."
    },
    "queryParams": [],
    "pathParams": []
  },
  {
    "name": "get_docs_for_employee",
    "description": "Return a list of documents for a specific person that the authenticated user's permission groups are allowed to VIEW.\n\nThis endpoint follows HiBob's Documents API behavior by filtering documents based on folder-level permissions.\n\nResponse Structure:\n  - documents: Array of document objects:\n        - documentName: { value: File name of the document }\n        - downloadLink: { value: URL to download the stored document }\n\nPermission Rules:\n  - User must have 'documents' module-level view permission.\n  - User must belong to at least one permission group assigned to the folder with canView = true.\n\nThis tool retrieves only the documents stored in folders that the user's permission groups can access.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Person ID whose documents should be fetched."
        }
      },
      "required": [
        "id"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "string",
        "description": "Person ID from the path parameter."
      }
    ]
  },
  {
    "name": "upload_shared_document",
    "description": "Upload a file to a specific employee's Shared folder via URL.\n\nThis endpoint follows HiBob's Documents API behavior for Shared folders.\nIt validates file size (max 5 MB), ensures the shared folder exists, and inserts a document record linked to the employee and the uploader.\n\nResponse Structure:\n  - documentName: { value: File name of the uploaded document }\n  - downloadLink: { value: URL to download the stored document }\n\nPermission Rules:\n  - User must have 'documents' module-level upload/edit permission.\n  - User must belong to at least one permission group with upload access to the shared folder.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "documentName": {
          "type": "string",
          "description": "The name of the documentName to be stored in HiBob."
        },
        "documentUrl": {
          "type": "string",
          "format": "uri",
          "description": "A direct file URL from your server (public or temporary signed). HiBob will call this URL to retrieve and store the document."
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Optional list of tags to assign to the document."
        }
      },
      "required": [
        "documentName",
        "documentUrl"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "number",
        "description": "Employee ID from the path parameter."
      }
    ]
  },
  {
    "name": "upload_confidential_document",
    "description": "Upload a file to a specific employee's Confidential folder via URL.\n\nThis endpoint follows HiBob's Documents API behavior for Confidential folders.\nIt validates file size (max 5 MB), ensures the confidential folder exists, and inserts a document record linked to the employee and the uploader.\n\nResponse Structure:\n  - id: Document ID\n  - employeeId: Employee ID as string\n  - uploadedById: ID of the user who uploaded the document\n  - name: File name of the uploaded document\n  - creationDate: ISO 8601 timestamp of creation\n  - status: Document status (e.g., 'active')\n  - tags: Array of tags assigned to the document\n  - folderId: UUID of the confidential folder\n  - mimeType: MIME type of the document\n  - fileId: File ID (matches document ID)\n  - documentName: Display name of the document\n  - owner: Object with owner ID\n  - actionRequestDate: ISO 8601 timestamp when upload was requested\n  - actionCompleteDate: ISO 8601 timestamp when upload completed\n\nPermission Rules:\n  - User must have 'documents' module-level upload/edit permission.\n  - User must belong to at least one permission group with upload access to the confidential folder.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "documentName": {
          "type": "string",
          "description": "The name of the documentName to be stored in HiBob."
        },
        "documentUrl": {
          "type": "string",
          "format": "uri",
          "description": "A direct file URL from your server (public or temporary signed). HiBob will call this URL to retrieve and store the document."
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Optional list of tags to assign to the document."
        }
      },
      "required": [
        "documentName",
        "documentUrl"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "number",
        "description": "Employee ID from the path parameter."
      }
    ]
  },
  {
    "name": "upload_custom_document",
    "description": "Upload a file to a specific custom folder via URL.\n\nThis endpoint follows HiBob's Documents API behavior for Custom folders.\nIt validates file size (max 5 MB), ensures the custom folder exists, and inserts a document record linked to the employee, folder, and uploader.\n\nResponse Structure:\n  - id: Document ID\n  - employeeId: Employee ID as string\n  - uploadedById: ID of the user who uploaded the document\n  - name: File name of the uploaded document\n  - creationDate: ISO 8601 timestamp of creation\n  - status: Document status (e.g., 'active')\n  - tags: Array of tags assigned to the document\n  - folderId: UUID of the custom folder\n  - mimeType: MIME type of the document\n  - fileId: File ID (matches document ID)\n  - documentName: Display name of the document\n  - owner: Object with owner ID\n  - actionRequestDate: ISO 8601 timestamp when upload was requested\n  - actionCompleteDate: ISO 8601 timestamp when upload completed\n\nPermission Rules:\n  - User must have 'documents' module-level upload/edit permission.\n  - The custom folder must exist and have folderType='custom'.\n  - User must belong to at least one permission group with upload access to the custom folder.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "folderId": {
          "type": "string",
          "description": "The UUID of the custom folder to upload to."
        },
        "documentName": {
          "type": "string",
          "description": "The name of the documentName to be stored in HiBob."
        },
        "documentUrl": {
          "type": "string",
          "format": "uri",
          "description": "A direct file URL from your server (public or temporary signed). HiBob will call this URL to retrieve and store the document."
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Optional list of tags to assign to the document."
        }
      },
      "required": [
        "documentName",
        "documentUrl",
        "folderId"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "number",
        "description": "Employee ID from the path parameter."
      },
      {
        "name": "folderId",
        "type": "string",
        "description": "The UUID of the custom folder."
      }
    ]
  },
  {
    "name": "delete_shared_document",
    "description": "Delete a specific document from an employee's Shared folder.\n\nThis endpoint removes a document from the shared folder and deletes the associated file from storage.\n\nResponse:\n  - 200 OK: Document deleted successfully with confirmation message\n  - 404 Not Found: Document not found or user lacks permission\n\nPermission Rules:\n  - User must have 'documents' module-level edit permission.\n  - User must belong to at least one permission group with delete access to the shared folder.\n  - The document must exist in the specified employee's shared folder.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "docId": {
          "type": "string",
          "description": "Document ID to delete."
        }
      },
      "required": [
        "id",
        "docId"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "string",
        "description": "Employee ID from the path parameter."
      },
      {
        "name": "docId",
        "type": "string",
        "description": "Document ID to delete."
      }
    ]
  },
  {
    "name": "delete_confidential_document",
    "description": "Delete a specific document from an employee's Confidential folder.\n\nThis endpoint removes a document from the confidential folder and deletes the associated file from storage.\n\nResponse:\n  - 200 OK: Document deleted successfully with confirmation message\n  - 404 Not Found: Document not found or user lacks permission\n\nPermission Rules:\n  - User must have 'documents' module-level edit permission.\n  - User must belong to at least one permission group with delete access to the confidential folder.\n  - The document must exist in the specified employee's confidential folder.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "docId": {
          "type": "string",
          "description": "Document ID to delete."
        }
      },
      "required": [
        "id",
        "docId"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "string",
        "description": "Employee ID from the path parameter."
      },
      {
        "name": "docId",
        "type": "string",
        "description": "Document ID to delete."
      }
    ]
  },
  {
    "name": "delete_custom_document",
    "description": "Delete a specific document from a custom folder.\n\nThis endpoint removes a document from the specified custom folder and deletes the associated file from storage.\n\nResponse:\n  - 200 OK: Document deleted successfully with confirmation message\n  - 404 Not Found: Document not found or user lacks permission\n\nPermission Rules:\n  - User must have 'documents' module-level edit permission.\n  - User must belong to at least one permission group with delete access to the custom folder.\n  - The document must exist in the specified custom folder for the employee.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Employee ID from the path parameter."
        },
        "folderId": {
          "type": "string",
          "description": "Custom folder UUID from the path parameter."
        },
        "docId": {
          "type": "string",
          "description": "Document ID to delete."
        }
      },
      "required": [
        "id",
        "folderId",
        "docId"
      ]
    },
    "queryParams": [],
    "pathParams": [
      {
        "name": "id",
        "type": "string",
        "description": "Employee ID from the path parameter."
      },
      {
        "name": "folderId",
        "type": "string",
        "description": "Custom folder UUID from the path parameter."
      },
      {
        "name": "docId",
        "type": "string",
        "description": "Document ID to delete."
      }
    ]
  },
  {
    "name": "get_all_company_fields",
    "description": "Get all company fields metadata.\n        \n        **Endpoint**: GET /v1/company/people/fields\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        Returns metadata for all fields including:\n        - Field ID and name\n        - Category information (root, work, about, etc.)\n        - Field type and type-specific data\n        - Historical flag\n        - JSON path\n        \n        **Rate Limit**: 50 requests per minute\n        \n        **No special permissions required** - All authenticated service users can access field metadata.\n        \n        **Use Cases:**\n        - Discover available fields for employee data\n        - Understand field structure and types\n        - Plan data migration or integration\n        - Validate field paths before querying\n        \n        **Example Response**:\n        ```json\n        [\n          {\n            \"id\": \"work.department\",\n            \"category\": \"work\",\n            \"categoryId\": \"work\",\n            \"categoryDisplayName\": \"Work\",\n            \"name\": \"Department\",\n            \"description\": \"Employee department\",\n            \"jsonPath\": \"work.department\",\n            \"type\": \"list\",\n            \"typeData\": {\"listId\": \"departments\"},\n            \"historical\": true\n          },\n          {\n            \"id\": \"root.firstName\",\n            \"category\": \"root\",\n            \"categoryId\": \"root\",\n            \"categoryDisplayName\": \"Root\",\n            \"name\": \"First Name\",\n            \"description\": \"Employee first name\",\n            \"jsonPath\": \"root.firstName\",\n            \"type\": \"text\",\n            \"typeData\": null,\n            \"historical\": false\n          }\n        ]\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "create_new_field",
    "description": "Create a new field.\n        \n        **Endpoint**: POST /v1/company/people/fields\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > Settings > Employee fields > Manage Employee Field Settings**\n        \n        **Request Body** (required fields):\n        - name: The name of the field - REQUIRED\n        - category: The category of the field - REQUIRED\n        - type: The type of field - REQUIRED\n          Supported field types: text, text-area, number, date, list, multi-list, hierarchy-list, currency, employee-reference, document\n        - description: The description of the field - OPTIONAL\n        - historical: When true, this field keeps the history of its values. Default is false - OPTIONAL\n        \n        **Restrictions**:\n        - Cannot create fields with category \"root\"\n        - Historical flag may not be allowed for certain categories\n        - Field type must be one of the supported types\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Use Cases:**\n        - Add custom employee attributes\n        - Create company-specific fields\n        - Extend standard employee data model\n        - Support custom business requirements\n        \n        **Example Request**:\n        ```json\n        {\n          \"category\": \"extra-information\",\n          \"name\": \"Skill Level\",\n          \"type\": \"text\",\n          \"description\": \"Employee's technical skill level\",\n          \"historical\": false\n        }\n        ```\n        \n        **Example Response**:\n        ```json\n        {\n          \"id\": \"extra-information.skillLevel\"\n        }\n        ```\n        \n        **Note**:\n        - The field ID is auto-generated based on category and name (category.fieldNameInCamelCase)\n        - The ID is returned in the response after successful creation\n        - Use this ID to reference the field in other API calls\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the field"
        },
        "category": {
          "type": "string",
          "description": "The category of the field (cannot be 'root')"
        },
        "type": {
          "type": "string",
          "description": "The type of field. Supported: text, text-area, number, date, list, multi-list, hierarchy-list, currency, employee-reference, document",
          "enum": [
            "text",
            "text-area",
            "number",
            "date",
            "list",
            "multi-list",
            "hierarchy-list",
            "currency",
            "employee-reference",
            "document"
          ]
        },
        "description": {
          "type": "string",
          "description": "The description of the field (optional)"
        },
        "historical": {
          "type": "boolean",
          "description": "When true, this field keeps the history of its values. Default is false",
          "default": false
        }
      },
      "required": [
        "name",
        "category",
        "type"
      ]
    }
  },
  {
    "name": "update_existing_field",
    "description": "Update an existing field.\n        \n        **Endpoint**: PUT /v1/company/people/fields/{fieldId}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > Settings > Employee fields > Manage Employee Field Settings**\n        \n        **Path Parameter**:\n        - fieldId: The ID of the field\n        \n        **Request Body** (all fields optional):\n        - name: The name of the field\n        - description: The description of the field\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Note**: You cannot change the field's ID, category, or type after creation.\n        Only name and description can be updated.\n        \n        **Use Cases:**\n        - Update field display names\n        - Modify field descriptions\n        - Correct field metadata\n        \n        **Example Request**:\n        ```json\n        {\n          \"fieldId\": \"extra-information.skillLevel\",\n          \"name\": \"Technical Skill Level\",\n          \"description\": \"Employee's current technical skill level\"\n        }\n        ```\n        \n        **Response**: Empty content with HTTP 200 on success\n        ```json\n        {}\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fieldId": {
          "type": "string",
          "description": "The ID of the field (path parameter)"
        },
        "name": {
          "type": "string",
          "description": "The name of the field (optional)",
          "minLength": 1,
          "maxLength": 100
        },
        "description": {
          "type": "string",
          "description": "The description of the field (optional)",
          "maxLength": 500
        }
      },
      "required": [
        "fieldId"
      ]
    }
  },
  {
    "name": "delete_existing_field",
    "description": "Delete an existing field.\n        \n        **Endpoint**: DELETE /v1/company/people/fields/{fieldId}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > Settings > Employee fields > Manage Employee Field Settings**\n        \n        **Path Parameter**:\n        - fieldId: The ID of the field.\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Error Responses**:\n        - 200: The field was deleted successfully\n        - 400: If the field is a Bob default field (cannot delete fields in 'root' category or system fields)\n        - 404: If the field doesn't exist\n        \n        **Warning**:\n        - Deleting a field will also delete all associated data for that field across all employees.\n        - This action cannot be undone.\n        - Bob default fields (in 'root' category or system fields) cannot be deleted.\n        - Use with caution in production environments.\n        \n        **Use Cases:**\n        - Remove deprecated custom fields\n        - Clean up unused fields\n        - Archive old metadata structures\n        \n        **Example Request**:\n        ```json\n        {\n          \"fieldId\": \"extra-information.oldField\"\n        }\n        ```\n        \n        **Example Response (Success)**:\n        ```json\n        {}\n        ```\n        \n        **Example Error (Bob default field)**:\n        ```json\n        {\n          \"error\": \"Cannot delete Bob default field in 'root' category\"\n        }\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "fieldId": {
          "type": "string",
          "description": "The ID of the field. (path parameter)"
        }
      },
      "required": [
        "fieldId"
      ]
    }
  },
  {
    "name": "get_all_company_lists",
    "description": "Get all company lists with their items.\n        \n        **Endpoint**: GET /v1/company/named-lists\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Query Parameters**:\n        - includeArchived: Whether to include archived items in the response (default: false)\n        \n        Returns all named lists including:\n        - List name\n        - List items with their integer IDs, values, names, and archived status\n        - Support for nested lists (children array)\n        \n        **Rate Limit**: 50 requests per minute\n        \n        **No special permissions required** - All authenticated service users can access list metadata.\n        \n        **Common Lists**:\n        - Departments: Company departments\n        - Sites: Office locations\n        - Employment Types: Types of employment (full-time, part-time, etc.)\n        - Titles: Job titles\n        \n        **Use Cases:**\n        - Discover available dropdown options\n        - Validate list values before creating employees\n        - Plan data migrations\n        - Build user interfaces with correct options\n        - Get archived items for historical data analysis\n        \n        **Example Response**:\n        ```json\n        [\n          {\n            \"name\": \"Departments\",\n            \"items\": [\n              {\"id\": 1, \"value\": \"Engineering\", \"name\": \"Engineering\", \"archived\": false, \"children\": []},\n              {\"id\": 2, \"value\": \"Sales\", \"name\": \"Sales\", \"archived\": false, \"children\": []},\n              {\"id\": 3, \"value\": \"Marketing\", \"name\": \"Marketing\", \"archived\": false, \"children\": []}\n            ]\n          },\n          {\n            \"name\": \"Sites\",\n            \"items\": [\n              {\"id\": 4, \"value\": \"Headquarters\", \"name\": \"Headquarters\", \"archived\": false, \"children\": []},\n              {\"id\": 5, \"value\": \"Remote\", \"name\": \"Remote\", \"archived\": false, \"children\": []}\n            ]\n          }\n        ]\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "includeArchived": {
          "type": "boolean",
          "description": "Whether to include archived items in the response (default: false)",
          "default": false
        }
      },
      "required": []
    }
  },
  {
    "name": "get_company_list_by_name",
    "description": "Get a specific company list by its name/ID.\n        \n        **Endpoint**: GET /v1/company/named-lists/{listName}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Path Parameter**:\n        - listName: The internal name of the list (e.g., 'departments', 'sites', 'employmentTypes')\n        \n        **Query Parameters**:\n        - includeArchived: Whether to include archived items in the response (default: false)\n        \n        **Rate Limit**: 50 requests per minute\n        \n        **No special permissions required** - All authenticated service users can access list metadata.\n        \n        **Use Cases:**\n        - Get options for a specific dropdown\n        - Validate a specific list value\n        - Check if a list item exists\n        - Build dynamic forms\n        - Get archived items for historical data\n        \n        **Example Request**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"includeArchived\": false\n        }\n        ```\n        \n        **Example Response**:\n        ```json\n        {\n          \"name\": \"Departments\",\n          \"items\": [\n            {\n              \"id\": 1,\n              \"value\": \"Engineering\",\n              \"name\": \"Engineering\",\n              \"archived\": false,\n              \"children\": [\n                {\n                  \"id\": 2,\n                  \"value\": \"Backend Engineering\",\n                  \"name\": \"Backend Engineering\",\n                  \"archived\": false\n                }\n              ]\n            },\n            {\n              \"id\": 5,\n              \"value\": \"Sales\",\n              \"name\": \"Sales\",\n              \"archived\": false,\n              \"children\": [\n                {\n                  \"id\": 6,\n                  \"value\": \"Enterprise Sales\",\n                  \"name\": \"Enterprise Sales\",\n                  \"archived\": false\n                }\n              ]\n            }\n          ]\n        }\n        ```\n        \n        **Note**: Item IDs are integers. The `children` field only appears when items have nested children.\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "listName": {
          "type": "string",
          "description": "The internal name of the list (path parameter, e.g., 'departments', 'sites')"
        },
        "includeArchived": {
          "type": "boolean",
          "description": "Whether to include archived items in the response (default: false)",
          "default": false
        }
      },
      "required": [
        "listName"
      ]
    }
  },
  {
    "name": "add_item_to_list",
    "description": "Add a new item to an existing list.\n        \n        **Endpoint**: POST /v1/company/named-lists/{listName}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > People > Edit all lists (sites, job titles, etc.)**\n        \n        **Path Parameter**:\n        - listName: The internal name of the list (e.g., 'departments')\n        \n        **Request Body**:\n        - name: Name of the item - REQUIRED\n        - parentId: ID of the new hierarchy parent node - OPTIONAL (only for hierarchy lists)\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Notes**:\n        - The `parentId` attribute is optional and only applies to hierarchy lists\n        - When `parentId` is specified, the newly created list item will be placed under the specific hierarchy parent node\n        - The ID returned can be textual or numeric depending on the list type\n        \n        **Use Cases:**\n        - Add new department\n        - Add new office location\n        - Extend employment types\n        - Add nested job title to a hierarchy\n        \n        **Example Request (flat list)**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"name\": \"Product Management\"\n        }\n        ```\n        \n        **Example Request (hierarchy list)**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"name\": \"Backend Team\",\n          \"parentId\": 1\n        }\n        ```\n        \n        **Example Response**:\n        ```json\n        {\n          \"id\": \"61\"\n        }\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "listName": {
          "type": "string",
          "description": "The internal name of the list (path parameter)"
        },
        "name": {
          "type": "string",
          "description": "Name of the item"
        },
        "parentId": {
          "type": "integer",
          "description": "ID of the new hierarchy parent node (optional, for nested lists only)"
        }
      },
      "required": [
        "listName",
        "name"
      ]
    }
  },
  {
    "name": "update_list_item",
    "description": "Update an existing item in a list.\n        \n        **Endpoint**: PUT /v1/company/named-lists/{listName}/{itemId}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > People > Edit all lists (sites, job titles, etc.)**\n        \n        **Path Parameters**:\n        - listName: The internal name of the list\n        - itemId: The ID of the list item\n        \n        **Request Body** (at least one required):\n        - name: Name of the item (optional) - Renames the list item value\n        - parentId: ID of the new hierarchy parent node (optional) - Moves the hierarchy list item (together with its children) under the indicated parent node\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Notes**:\n        - You need to provide at least one of: `name` or `parentId`\n        - Providing a name will rename the list item value\n        - Providing the parent ID will move the hierarchy list item (together with its children) under the indicated parent node\n        \n        **Use Cases:**\n        - Rename department or location\n        - Move team within organization hierarchy\n        - Reorganize nested structures\n        - Update job title names\n        \n        **Example Request (rename)**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"itemId\": \"5\",\n          \"name\": \"Product & Engineering\"\n        }\n        ```\n        \n        **Example Request (move in hierarchy)**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"itemId\": \"10\",\n          \"parentId\": 1\n        }\n        ```\n        \n        **Example Request (rename and move)**:\n        ```json\n        {\n          \"listName\": \"sites\",\n          \"itemId\": \"25\",\n          \"name\": \"Austin Tech Hub\",\n          \"parentId\": 24\n        }\n        ```\n        \n        **Example Response**:\n        ```json\n        {}\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "listName": {
          "type": "string",
          "description": "The internal name of the list (path parameter)"
        },
        "itemId": {
          "type": "string",
          "description": "The ID of the list item (path parameter)"
        },
        "name": {
          "type": "string",
          "description": "Name of the item (optional, renames the item)"
        },
        "parentId": {
          "type": "integer",
          "description": "ID of the new hierarchy parent node (optional, moves item in hierarchy)"
        }
      },
      "required": [
        "listName",
        "itemId"
      ]
    }
  },
  {
    "name": "delete_list_item",
    "description": "Delete an item from an existing list.\n        \n        **Endpoint**: DELETE /v1/company/named-lists/{listName}/{itemId}\n        **Headers required**: X-Hibob-User-Token, X-Database-Id\n        \n        **Permission Required**:\n        - **Features > People > Edit all lists (sites, job titles, etc.)**\n        \n        **Path Parameters**:\n        - listName: The internal name of the list\n        - itemId: The ID of the list item\n        \n        **Rate Limit**: 10 requests per minute\n        \n        **Warning**:\n        - Deleting a list item may affect employees who have this value selected\n        - Deleting an item will also delete all its children in hierarchical lists\n        - This action cannot be undone\n        \n        **Use Cases:**\n        - Remove incorrect list entries\n        - Clean up test data\n        - Delete truly unused items from hierarchy\n        \n        **Example Request**:\n        ```json\n        {\n          \"listName\": \"departments\",\n          \"itemId\": \"25\"\n        }\n        ```\n        \n        **Example Response**:\n        ```json\n        {}\n        ```\n        ",
    "inputSchema": {
      "type": "object",
      "properties": {
        "listName": {
          "type": "string",
          "description": "The internal name of the list (path parameter)"
        },
        "itemId": {
          "type": "string",
          "description": "The ID of the list item (path parameter)"
        }
      },
      "required": [
        "listName",
        "itemId"
      ]
    }
  },
  {
    "name": "read_all_open_tasks",
    "description": "List all open tasks in the system. Returns all tasks with status='open' for the organization.\n\n        Returns tasks array with id, employeeId, title, description, status, dueDate, createdAt, and updatedAt fields.",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "read_tasks_for_employee",
    "description": "List tasks for a specific employee with optional status filter. Returns tasks assigned to a particular employee.\n\n        Optionally filter by task_status (\"open\" or \"closed\"). Requires employee id parameter.\n\n        Returns tasks array with id, employeeId, title, description, status, dueDate, createdAt, and updatedAt fields.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The employee ID (e.g.,\"101\", \"102\")",
          "minimum": 1
        },
        "task_status": {
          "type": "string",
          "description": "Optional filter by task status",
          "enum": [
            "open",
            "closed"
          ]
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "complete_task",
    "description": "Mark a task as complete. Changes the status of a task from 'open' to 'closed' by task ID.\n\n        Requires taskId parameter. Returns toDosUpdated count (1 if successful, 0 if not found or already completed).",
    "inputSchema": {
      "type": "object",
      "properties": {
        "taskId": {
          "type": "string",
          "description": "The task ID to mark as complete (e.g., \"1\", \"2\", \"3\")",
          "minimum": 1
        }
      },
      "required": [
        "taskId"
      ]
    }
  },
  {
    "name": "get_custom_tables_metadata",
    "description": "Get metadata for all custom tables in the organization. Returns table definitions including columns, types, and constraints.\n\n        No special permissions required - metadata is available to all authenticated users.\n\n        Returns tables array with id, category, name, description, and columns array (with id, name, description, mandatory, type, typeData).",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  {
    "name": "get_custom_table_metadata",
    "description": "Get metadata for a specific custom table by ID. Returns table definition including columns, types, and constraints.\n\n        Requires custom_table_id parameter. No special permissions required.\n\n        Returns table object with id, category, name, description, and columns array.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "custom_table_id": {
          "type": "string",
          "description": "The custom table ID (e.g., '1', '2', '3', '4')"
        }
      },
      "required": [
        "custom_table_id"
      ]
    }
  },
  {
    "name": "get_employee_custom_table_entries",
    "description": "Read all entries of a custom table for a specific employee. Returns all entries for an employee in a specific custom table.\n\n        Requires employee_id and custom_table_id parameters. Optionally include includeHumanReadable flag for formatted values. Values are returned in flat column_<id> format.\n\n        Returns values array with id, changedBy, column_<id> fields, and optional humanReadable object.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employee_id": {
          "type": "string",
          "description": "The employee ID (e.g., '101', '102')"
        },
        "custom_table_id": {
          "type": "string",
          "description": "The custom table ID (e.g., '1', '2', '3', '4')"
        },
        "includeHumanReadable": {
          "type": "boolean",
          "description": "Include human-readable format of values",
          "default": false
        }
      },
      "required": [
        "employee_id",
        "custom_table_id"
      ]
    }
  },
  {
    "name": "create_custom_table_entry",
    "description": "Create new custom table entry for an employee. Creates a new entry in a custom table with all mandatory columns provided.\n\n        Requires employee_id, custom_table_id, and column_data object with column_<id> fields. All mandatory columns must be provided (varies by table).\n\n        Returns new entry with id, changedBy, and all column_<id> values.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employee_id": {
          "type": "string",
          "description": "The employee ID (e.g., '101')"
        },
        "custom_table_id": {
          "type": "string",
          "description": "The custom table ID (e.g., '1' for Expense Allowances)"
        },
        "column_data": {
          "type": "object",
          "description": "Column values in column_<id> format (e.g., {\"column_1\": \"Travel\", \"column_2\": 500, \"column_3\": \"USD\", \"column_4\": \"2024-12-01\"})",
          "additionalProperties": true
        }
      },
      "required": [
        "employee_id",
        "custom_table_id",
        "column_data"
      ]
    }
  },
  {
    "name": "update_custom_table_entry",
    "description": "Update existing custom table entry (PATCH behavior). Updates an existing entry in a custom table with partial updates supported.\n\n        Requires employee_id, custom_table_id, entry_id, and column_data object with column_<id> fields to update. Only provided fields are updated, others remain unchanged.\n\n        Returns updated entry with id, changedBy, and all column_<id> values (updated + unchanged).",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employee_id": {
          "type": "string",
          "description": "The employee ID (e.g., '101')"
        },
        "custom_table_id": {
          "type": "string",
          "description": "The custom table ID (e.g., '1')"
        },
        "entry_id": {
          "type": "string",
          "description": "The entry ID to update (e.g., '1', '2')"
        },
        "column_data": {
          "type": "object",
          "description": "Column values to update in column_<id> format (e.g., {\"column_2\": 850})",
          "additionalProperties": true
        }
      },
      "required": [
        "employee_id",
        "custom_table_id",
        "entry_id",
        "column_data"
      ]
    }
  },
  {
    "name": "delete_custom_table_entry",
    "description": "Delete custom table entry using soft delete. Marks entry as deleted while preserving data for audit purposes.\n\n        Requires employee_id, custom_table_id, and entry_id parameters. Entry is preserved in database but won't appear in GET requests.\n\n        Returns success message confirming deletion.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "employee_id": {
          "type": "string",
          "description": "The employee ID (e.g., '101')"
        },
        "custom_table_id": {
          "type": "string",
          "description": "The custom table ID (e.g., '1')"
        },
        "entry_id": {
          "type": "string",
          "description": "The entry ID to delete (e.g., '1', '2')"
        }
      },
      "required": [
        "employee_id",
        "custom_table_id",
        "entry_id"
      ]
    }
  }
]
```

2. Show thinking traces/thinking scratch pad that the model outputs on every step of the way
3. Migrate to using Qwen3 for the model outputs (using openrouter)
4. Make the cycle go: User -> [Thinking -> Action (ToolCall/ToolOutput) -> Observation]LOOP -> Assistant Response
5. Open the testing server


And after finishing every step, make a git commit.
