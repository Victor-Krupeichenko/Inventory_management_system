from fastapi import APIRouter, Request, responses, status
from fastapi.templating import Jinja2Templates
from api.company.schemes import CompanyCreateScheme
from web.forms import form_company
from web.web_utils import check_error, form_valid_data, object_instance
from api.company.models import Company

web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="web/templates")


@web_router.get("/")
def home_page(request: Request):
    """Main page render"""
    return templates.TemplateResponse("index.html", context={"request": request})


@web_router.api_route("/add-company", methods=["GET", "POST"])
async def web_add_company(request: Request):
    """Add company page render"""
    form_fields = form_company()
    if request.method == "GET":
        return templates.TemplateResponse(
            name="create_company.html", status_code=status.HTTP_200_OK,
            context={
                "request": request,
                "form_fields": form_fields
            }
        )
    elif request.method == "POST":
        form_data = await request.form()
        form_valid = form_valid_data(form_data, "product", CompanyCreateScheme)
        errors_list = check_error(form_valid, "error")
        if errors_list:
            return templates.TemplateResponse(
                name="create_company.html", status_code=status.HTTP_400_BAD_REQUEST,
                context={
                    "request": request,
                    "form_fields": form_fields,
                    "errors_list": errors_list
                }
            )
        company = object_instance(form_valid, Company)
        company.add_company()
        redirect_url = web_router.url_path_for("home_page")
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
