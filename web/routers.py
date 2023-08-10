from fastapi import APIRouter, Request, responses, status
from fastapi.templating import Jinja2Templates
from api.company.schemes import CompanyCreateScheme
from web.forms import form_for_models
from web.web_utils import check_error, form_valid_data, object_instance, templates_error
from api.company.models import Company
from api.company.repository import CompanyRepositoryRedis
from api.users.schemes import RegisterUserScheme
from api.users.models import User

web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="web/templates")


@web_router.get("/")
def home_page(request: Request):
    """Main page render"""
    return templates.TemplateResponse("index.html", context={"request": request})


@web_router.api_route("/add-company", methods=["GET", "POST"])
async def web_add_company(request: Request):
    """Add company page render"""
    form_fields = form_for_models(CompanyCreateScheme)
    name_template = "create_company.html"
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template, status_code=status.HTTP_200_OK,
            context={
                "request": request,
                "form_fields": form_fields
            }
        )
    elif request.method == "POST":
        form_data = await request.form()
        form_valid = form_valid_data(form_data, CompanyCreateScheme, key="product")
        errors_list = check_error(form_valid, "error")
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        company = object_instance(form_valid, Company)
        company.add_company()
        redirect_url = web_router.url_path_for("home_page")
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)


@web_router.get("/search")
async def company_specified_product(request: Request):
    """Company search by product (material)"""
    search = request.query_params.get("search")
    results = CompanyRepositoryRedis.product(search)
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "results": results, "search": search, "count": len(results.get("company"))}
    )


@web_router.api_route("/register-user", methods=["GET", "POST"])
async def web_register_user(request: Request):
    """Register user"""
    form_fields = form_for_models(RegisterUserScheme)
    name_template = "register_user.html"
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template, context={
                "request": request, "form_fields": form_fields
            }
        )
    elif request.method == "POST":
        form_data = await request.form()
        form_valid = form_valid_data(form_data, RegisterUserScheme)
        errors_list = check_error(form_valid, "error")
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        new_user = User(
            username=form_data.get("username"), password=form_data.get("password1"), email=form_data.get("email")
        )
        new_user.create_user()
        redirect_url = web_router.url_path_for("home_page")
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
