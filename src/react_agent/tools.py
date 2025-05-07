"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from datetime import datetime

from typing import Any, Callable, Dict, List, Optional, Tuple, cast

from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration


# async def search(query: str) -> Optional[dict[str, Any]]:
#     """Search for general web results.

#     This function performs a search using the Tavily search engine, which is designed
#     to provide comprehensive, accurate, and trusted results. It's particularly useful
#     for answering questions about current events.
#     """
#     configuration = Configuration.from_context()
#     wrapped = TavilySearch(max_results=configuration.max_search_results)
#     return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))

invoices_data_store = invoices = [
    {
        "invoice_id": "5d4259c4-cbe5-4766-972a-1a5e0311f20e",
        "invoice_date": "2023-01-01",
        "invoice_amount": 2434,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-01-31",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Globex Inc",
        "invoice_PO_number": "58254a76-b86a-464f-91a0-06cb409dfb9f",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 1",
                "item_description": "Description for service 1",
                "item_quantity": 2,
                "item_price": 1217,
                "item_total": 2434
            }
        ]
    },
    {
        "invoice_id": "f0e65297-bb94-47ab-9f85-2e2412e49dd6",
        "invoice_date": "2023-07-17",
        "invoice_amount": 1988,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-08-16",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Gringotts Bank",
        "invoice_PO_number": "b8784e0c-1cfc-4cae-9b13-545d8d625e93",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 2",
                "item_description": "Description for service 2",
                "item_quantity": 5,
                "item_price": 397,
                "item_total": 1988
            }
        ]
    },
    {
        "invoice_id": "47695aff-c1f6-45b5-a793-b2f2aeb3993d",
        "invoice_date": "2023-08-07",
        "invoice_amount": 947,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-09-06",
        "invoice_currency": "EUR",
        "invoice_customer_name": "Tyrell Corporation",
        "invoice_PO_number": "b86971dd-3f58-4870-b342-35e16a6d6be4",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 3",
                "item_description": "Description for service 3",
                "item_quantity": 7,
                "item_price": 135,
                "item_total": 947
            }
        ]
    },
    {
        "invoice_id": "5cee0d10-3cfe-4e58-ba3b-e6faa7897c3b",
        "invoice_date": "2023-05-24",
        "invoice_amount": 6178,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-06-08",
        "invoice_currency": "EUR",
        "invoice_customer_name": "Pied Piper",
        "invoice_PO_number": "f858c7a4-72c9-48ae-a5c3-1c0c3499cd4d",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 4",
                "item_description": "Description for service 4",
                "item_quantity": 1,
                "item_price": 6178,
                "item_total": 6178
            }
        ]
    },
    {
        "invoice_id": "e0de2a9b-b0dc-4979-b3ba-2615ecd27b20",
        "invoice_date": "2023-06-22",
        "invoice_amount": 3146,
        "invoice_status": "paid",
        "invoice_due_date": "2023-07-22",
        "invoice_currency": "USD",
        "invoice_customer_name": "Wayne Enterprises",
        "invoice_PO_number": "b1581e35-d341-4108-a26d-20127beabad9",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 5",
                "item_description": "Description for service 5",
                "item_quantity": 3,
                "item_price": 1048,
                "item_total": 3146
            }
        ]
    },
    {
        "invoice_id": "fc71daff-1bd5-4f8a-b9b8-8808a01895e3",
        "invoice_date": "2023-06-24",
        "invoice_amount": 8242,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-07-24",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Cyberdyne Systems",
        "invoice_PO_number": "dd975e82-b124-47fc-8bde-523d282260c5",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 6",
                "item_description": "Description for service 6",
                "item_quantity": 7,
                "item_price": 1177,
                "item_total": 8242
            }
        ]
    },
    {
        "invoice_id": "1a4aae73-375f-423e-9a01-e4ab1c2ec8ee",
        "invoice_date": "2023-06-19",
        "invoice_amount": 3477,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-06-19",
        "invoice_currency": "GBP",
        "invoice_customer_name": "John Doe",
        "invoice_PO_number": "c42e0b34-dc61-4c05-b4ef-5655504d6bd0",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 7",
                "item_description": "Description for service 7",
                "item_quantity": 2,
                "item_price": 1738,
                "item_total": 3477
            }
        ]
    },
    {
        "invoice_id": "7a521519-d923-43ee-b642-95429ad4fb0b",
        "invoice_date": "2023-04-07",
        "invoice_amount": 7238,
        "invoice_status": "paid",
        "invoice_due_date": "2023-04-22",
        "invoice_currency": "EUR",
        "invoice_customer_name": "John Doe",
        "invoice_PO_number": "114b0092-1f83-4b45-ad79-c2baa454f58c",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 8",
                "item_description": "Description for service 8",
                "item_quantity": 6,
                "item_price": 1206,
                "item_total": 7238
            }
        ]
    },
    {
        "invoice_id": "f3bd7f3d-3362-47fb-aeb4-233167331830",
        "invoice_date": "2023-04-29",
        "invoice_amount": 1155,
        "invoice_status": "paid",
        "invoice_due_date": "2023-05-29",
        "invoice_currency": "USD",
        "invoice_customer_name": "Umbrella LLC",
        "invoice_PO_number": "e3f53c76-7a8d-41ce-97aa-dca92a2e8e09",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 9",
                "item_description": "Description for service 9",
                "item_quantity": 3,
                "item_price": 385,
                "item_total": 1155
            }
        ]
    },
    {
        "invoice_id": "19856e41-28b5-4c6c-834b-a611c3b4f5cd",
        "invoice_date": "2023-06-22",
        "invoice_amount": 404,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-07-22",
        "invoice_currency": "USD",
        "invoice_customer_name": "Acme Corp",
        "invoice_PO_number": "d5d85f89-3a70-47e8-91f2-303c31e0e62f",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 10",
                "item_description": "Description for service 10",
                "item_quantity": 5,
                "item_price": 80,
                "item_total": 404
            }
        ]
    },
    {
        "invoice_id": "4f80bef8-a011-4c1d-8be2-53c23f021258",
        "invoice_date": "2023-07-13",
        "invoice_amount": 1851,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-07-13",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Jane Smith",
        "invoice_PO_number": "49c6b53b-497d-41b3-8b05-34d953c31172",
        "invoice_terms": "Net 15",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 11",
                "item_description": "Description for service 11",
                "item_quantity": 3,
                "item_price": 617,
                "item_total": 1851
            }
        ]
    },
    {
        "invoice_id": "b826cb23-4574-4404-aceb-c89ef5f5dc30",
        "invoice_date": "2023-06-08",
        "invoice_amount": 9674,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-06-08",
        "invoice_currency": "USD",
        "invoice_customer_name": "Cyberdyne Systems",
        "invoice_PO_number": "7f4339fa-5af3-4551-ab6d-5cef03142518",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 12",
                "item_description": "Description for service 12",
                "item_quantity": 7,
                "item_price": 1382,
                "item_total": 9674
            }
        ]
    },
    {
        "invoice_id": "924dc6db-1afa-41ea-bb6a-7f5ec36e8423",
        "invoice_date": "2023-03-24",
        "invoice_amount": 6736,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-03-24",
        "invoice_currency": "EUR",
        "invoice_customer_name": "John Doe",
        "invoice_PO_number": "f5491731-cba6-4363-9c95-3451dc06f5d9",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 13",
                "item_description": "Description for service 13",
                "item_quantity": 9,
                "item_price": 748,
                "item_total": 6736
            }
        ]
    },
    {
        "invoice_id": "4b276ff7-0c1b-4cf8-8a11-72d8d6f84fe4",
        "invoice_date": "2023-03-04",
        "invoice_amount": 2679,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-03-04",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Wonka Industries",
        "invoice_PO_number": "52c86421-103d-4403-8c39-51a8b935e51b",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 14",
                "item_description": "Description for service 14",
                "item_quantity": 10,
                "item_price": 267,
                "item_total": 2679
            }
        ]
    },
    {
        "invoice_id": "699947c6-7ea9-4652-a3cd-44a7ec6024e7",
        "invoice_date": "2023-08-26",
        "invoice_amount": 5997,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-08-26",
        "invoice_currency": "USD",
        "invoice_customer_name": "Duff Beer",
        "invoice_PO_number": "1eb45552-653e-41f8-9e98-6575eb63f721",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 15",
                "item_description": "Description for service 15",
                "item_quantity": 2,
                "item_price": 2998,
                "item_total": 5997
            }
        ]
    },
    {
        "invoice_id": "813c16d0-bde7-4c35-8bab-3b8dab5d0e9f",
        "invoice_date": "2023-07-20",
        "invoice_amount": 8028,
        "invoice_status": "overdue",
        "invoice_due_date": "2023-07-20",
        "invoice_currency": "USD",
        "invoice_customer_name": "Globex Inc",
        "invoice_PO_number": "b7c902d2-6ef9-4a0c-8b64-4b21a4e9d8f5",
        "invoice_terms": "Net 15",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 16",
                "item_description": "Description for service 16",
                "item_quantity": 5,
                "item_price": 1605,
                "item_total": 8028
            }
        ]
    },
    {
        "invoice_id": "d852c021-f872-4ae7-a07f-239fa4819d91",
        "invoice_date": "2023-01-29",
        "invoice_amount": 1776,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-01-29",
        "invoice_currency": "GBP",
        "invoice_customer_name": "Tyrell Corporation",
        "invoice_PO_number": "b7c902d2-6ef9-4a0c-8b64-4b21a4e9d8f5",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 17",
                "item_description": "Description for service 17",
                "item_quantity": 4,
                "item_price": 444,
                "item_total": 1776
            }
        ]
    },
    {
        "invoice_id": "d218c42d-f8dc-4c4c-a796-e4af2af3dcc2",
        "invoice_date": "2023-02-23",
        "invoice_amount": 1444,
        "invoice_status": "paid",
        "invoice_due_date": "2023-02-23",
        "invoice_currency": "EUR",
        "invoice_customer_name": "Cyberdyne Systems",
        "invoice_PO_number": "695e7e5b-149f-4505-a139-30dd33e5a76f",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 18",
                "item_description": "Description for service 18",
                "item_quantity": 7,
                "item_price": 206,
                "item_total": 1444
            }
        ]
    },
    {
        "invoice_id": "bf234da4-5e89-45ad-8cee-6f45a8f1a459",
        "invoice_date": "2023-08-24",
        "invoice_amount": 3732,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-09-23",
        "invoice_currency": "USD",
        "invoice_customer_name": "Stark Industries",
        "invoice_PO_number": "695e7e5b-149f-4505-a139-30dd33e5a76f",
        "invoice_terms": "Net 30",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 19",
                "item_description": "Description for service 19",
                "item_quantity": 7,
                "item_price": 533,
                "item_total": 3732
            }
        ]
    },
    {
        "invoice_id": "f75a87ab-2a55-4bbb-9e46-74b0838441a0",
        "invoice_date": "2023-06-28",
        "invoice_amount": 710,
        "invoice_status": "unpaid",
        "invoice_due_date": "2023-07-28",
        "invoice_currency": "USD",
        "invoice_customer_name": "Jane Smith",
        "invoice_PO_number": "695e7e5b-149f-4505-a139-30dd33e5a76f",
        "invoice_terms": "Due on receipt",
        "invoice_notes": "Automatically generated invoice.",
        "invoice_items": [
            {
                "item_name": "Service 20",
                "item_description": "Description for service 20",
                "item_quantity": 1,
                "item_price": 710,
                "item_total": 710
            }
        ]
    }
]

departments = [
    {"department_id": "695e7e5b-149f-4505-a139-30dd33e5a76f", "department_name": "Marketing"},
    {"department_id": "b7c902d2-6ef9-4a0c-8b64-4b21a4e9d8f5", "department_name": "Operations"},
    {"department_id": "c9f45e36-bdc4-4375-8cf5-91ad61e43f58", "department_name": "Creative"},
    {"department_id": "d92d45f9-90a3-426b-b4d5-cf82f4189d11", "department_name": "People Operations"},
    {"department_id": "e3f53c76-7a8d-41ce-97aa-dca92a2e8e09", "department_name": "Executive"}
]



peoples_directory = [
    {"firstName": "Nadia", "lastName": "Kassem", "title": "Chief Executive Officer", "email": "nadia.kassem@duo-marketing.com"},
    {"firstName": "Youssef", "lastName": "Gad", "title": "Chief Marketing Officer", "email": "youssef.gad@duo-marketing.com"},
    {"firstName": "Dalia", "lastName": "Farouk", "title": "Marketing Manager", "email": "dalia.farouk@duo-marketing.com"},
    {"firstName": "Karim", "lastName": "Hassan", "title": "Marketing Analyst", "email": "karim.hassan@duo-marketing.com"},
    {"firstName": "Salma", "lastName": "Khalil", "title": "Brand Strategist", "email": "salma.khalil@duo-marketing.com"},
    {"firstName": "Amit", "lastName": "Patel", "title": "Chief Operating Officer", "email": "amit.patel@duo-marketing.com"},
    {"firstName": "Tanya", "lastName": "Desai", "title": "Operations Manager", "email": "tanya.desai@duo-marketing.com"},
    {"firstName": "Nour", "lastName": "El Din", "title": "Project Coordinator", "email": "nour.eldin@duo-marketing.com"},
    {"firstName": "Luis", "lastName": "Martinez", "title": "Administrative Assistant", "email": "luis.martinez@duo-marketing.com"},
    {"firstName": "Omar", "lastName": "Zaki", "title": "Chief Creative Officer", "email": "omar.zaki@duo-marketing.com"},
    {"firstName": "Martha", "lastName": "Nguyen", "title": "Content Manager", "email": "martha.nguyen@duo-marketing.com"},
    {"firstName": "Elena", "lastName": "Santiago", "title": "Junior Content Creator", "email": "elena.santiago@duo-marketing.com"},
    {"firstName": "Dave", "lastName": "Henderson", "title": "Senior Video Editor", "email": "dave.henderson@duo-marketing.com"},
    {"firstName": "Riya", "lastName": "Verma", "title": "Photographer", "email": "riya.verma@duo-marketing.com"},
    {"firstName": "Carlos", "lastName": "Ramirez", "title": "Junior Video Editor", "email": "carlos.ramirez@duo-marketing.com"},
    {"firstName": "Martha", "lastName": "Reynolds", "title": "People Operations Lead", "email": "martha.reynolds@duo-marketing.com"}
]


def parse_invoice_data(invoice_data: str) -> List[Dict[str, Any]]:
    """Parse an invoice data and return a list of dictionaries containing the invoice data.

    Args:
        invoice_data (str): The invoice data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the invoice data.
    """
    # TODO: Add more data to this that could be used for validation


    results = []
    for invoice in invoices_data_store:
        if invoice_data in invoice["invoice_id"]:
            results.append(invoice)
    return results


def validate_invoice_data(invoice: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate the invoice data.

    Args:
        invoice (Dict[str, Any]): The invoice ids and their validation status.

    Returns:
        Tuple[bool, List[str]]: A tuple containing a boolean and a list of strings.
    """
    result = []
    for invoice in invoice:
        if invoice["invoice_id"] in invoices_data_store:
            for field in invoice:
                if field not in invoices_data_store[invoice["invoice_id"]]:
                    result.append(f"Invoice {invoice['invoice_id']} has an invalid field: {field}")
    return result


def detect_duplicate_invoice(invoice: Dict[str, Any]) -> bool:
    """Detect if an invoice is a duplicate.

    Args:
        invoice (Dict[str, Any]): The invoice data.

    Returns:
        bool: True if the invoice is a duplicate, False otherwise.

    """
    result = []
    for invoice in invoice:
        if invoice["invoice_id"] in invoices_data_store:
            return True
    return False


def cross_reference_po(po_number: str) -> str:
    """Cross-reference a PO number with the invoice data.

    Args:
        po_number (str): The PO number.

    Returns:
        bool: True if the PO number is valid, False otherwise.
    """
    # Match the PO number with the department
    for department in departments:
        if po_number in department["department_id"]:
            return department["department_name"]
    return None

def compute_invoice_totals(invoice: Dict[str, Any]) -> Dict[str, float]:
    """Compute the total of an invoice.

    Args:
        invoice (Dict[str, Any]): The invoice data.

    Returns:
        Dict[str, float]: A dictionary containing the total of the invoice.
    """
    total = 0
    for item in invoice["invoice_items"]:
        total += item["item_total"]
    return total

def get_people_directory(department: str) -> Dict[str, Any]:
    """Get the people directory for a department.

    Args:
        department (str): The department of the invoice.
    """
    return peoples_directory


def update_invoice_payment_status(invoice_id: str, status: str, payment_date: Optional[str]) -> bool:
    """Update the payment status of an invoice.

    Args:
        invoice_id (str): The invoice id.
        status (str): The status of the invoice.
        payment_date (Optional[str]): The payment date of the invoice.
    """
    if status not in ["paid", "unpaid", "overdue"]:
        return False
    if payment_date is None:
        return False
    if payment_date < invoices_data_store[invoice_id]["invoice_due_date"]:
        invoices_data_store[invoice_id]["invoice_status"] = "overdue"
        invoices_data_store[invoice_id]["invoice_payment_date"] = payment_date
    else:
        invoices_data_store[invoice_id]["invoice_status"] = status
        invoices_data_store[invoice_id]["invoice_payment_date"] = payment_date
    return True


def get_invoice_payment_status(invoice_id: str) -> str:
    """Get the payment status of an invoice.

    Args:
        invoice_id (str): The invoice id.
    """
    return invoices_data_store[invoice_id]["invoice_status"]

def query_unpaid_invoices(department: str, as_of_date: str) -> List[Dict[str, Any]]:
    """Query the unpaid invoices for a department.

    Args:
        department (str): The department of the invoice.
        as_of_date (str): The date of the invoice.
    """
    # handle that dates are strings
    results = []
    as_of_date = datetime.strptime(as_of_date, "%Y-%m-%d")
    for invoice in invoices_data_store:
        if invoice["invoice_status"] == "unpaid" and datetime.strptime(invoice["invoice_due_date"], "%Y-%m-%d") < as_of_date:
            results.append(invoice)
    return results

def send_notification_email(to: str, subject: str, body: str) -> None:
    """Send a notification email.

    Args:
        to (str): The email of the recipient.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    for person in peoples_directory:
        if to == person["email"]:
            return True
    return False

def calculator(expression: str) -> float:
    """Calculate the result of an expression.

    Args:
        expression (str): The expression to calculate.
    """
    return eval(expression)

TOOLS: List[Callable[..., Any]] = [parse_invoice_data, validate_invoice_data, detect_duplicate_invoice, cross_reference_po, compute_invoice_totals, get_people_directory, 
                                   calculator, query_unpaid_invoices, send_notification_email, update_invoice_payment_status, get_invoice_payment_status]
