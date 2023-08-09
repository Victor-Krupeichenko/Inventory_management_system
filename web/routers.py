from fastapi import APIRouter, Request, responses, status
from fastapi.templating import Jinja2Templates
from api.company.schemes import CompanyCreateScheme
from web.forms import form_company
from web.utils import check_error, form_valid_data, object_instance
from api.company.models import Company

web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="web/templates")


@web_router.get("/")
def home_page(request: Request):
    """Main page render"""
    return templates.TemplateResponse("index.html", context={"request": request})


@web_router.get("/add-company")
def web_add_company(request: Request):
    """Form Page Render"""
    form_fields = form_company()
    return templates.TemplateResponse("create_company.html", context={"request": request, "form_fields": form_fields})


@web_router.post("/add-company")
async def web_add_company(request: Request):
    """Sending data from a form"""
    form_data = await request.form()
    form = form_valid_data(form_data, "product", CompanyCreateScheme)
    error_list = check_error(form, "error")
    if error_list:
        form_fields = form_company()
        return templates.TemplateResponse(
            name="create_company.html", status_code=status.HTTP_400_BAD_REQUEST,
            context={"request": request, "form_fields": form_fields, "errors_list": error_list}
        )
    company = object_instance(form, Company)
    company.add_company()
    return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
