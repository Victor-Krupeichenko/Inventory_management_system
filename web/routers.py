from fastapi import APIRouter, Request, responses, status
from fastapi.templating import Jinja2Templates
from api.company.schemes import CompanyCreateScheme
from web.forms import form_for_models
from web.web_utils import check_error, form_valid_data, object_instance, templates_error, form_processing
from api.company.models import Company
from api.company.repository import CompanyRepositoryRedis
from api.users.schemes import RegisterUserScheme, AuthUserScheme
from api.users.models import User
from api.users.token_and_current_user import create_access_token
from api.users.settings_for_token import name_cookies
from api.stock.schemes import StockProductScheme
from api.stock.models import Stock
from api.ordering.repository import MIN_QUANTITY as min_quantity, OrderRepositoryRedis

web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="web/templates")


@web_router.get("/")
def web_home_page(request: Request):
    """Main page render"""
    return templates.TemplateResponse("index.html", context={"request": request}, status_code=status.HTTP_200_OK)


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
        redirect_url = web_router.url_path_for("web_home_page")
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)


@web_router.get("/search")
async def web_company_specified_product(request: Request):
    """Company search by product (material)"""
    search = request.query_params.get("search")
    results = CompanyRepositoryRedis.product(search)
    return templates.TemplateResponse(
        name="index.html",
        status_code=status.HTTP_200_OK,
        context={"request": request, "results": results, "search": search, "count": len(results.get("company"))}
    )


@web_router.api_route("/register-user", methods=["GET", "POST"])
async def web_register_user(request: Request):
    """Register user"""
    form_fields = form_for_models(RegisterUserScheme)
    name_template = "register_or_login_user.html"
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template, status_code=status.HTTP_200_OK, context={
                "request": request, "form_fields": form_fields
            }
        )
    elif request.method == "POST":
        form_data, errors_list = await form_processing(request, RegisterUserScheme)
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        new_user = User(
            username=form_data.get("username"), password=form_data.get("password1"), email=form_data.get("email")
        )
        new_user.create_user()
        redirect_url = web_router.url_path_for("web_home_page")
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)


@web_router.api_route("/login-user", methods=["GET", "POST"])
async def web_login_user(request: Request):
    """Login user"""
    form_fields = form_for_models(AuthUserScheme)
    name_template = "register_or_login_user.html"
    login_user = True
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template,
            context={
                "request": request, "form_fields": form_fields, "login_user": login_user
            }
        )
    elif request.method == "POST":
        form_data, errors_list = await form_processing(request, AuthUserScheme)
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        redirect_url = web_router.url_path_for("web_home_page")
        response = responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        jwt_token = create_access_token(data={"username": form_data.get("username")})
        response.set_cookie(key=name_cookies, value=f"Bearer {jwt_token}", httponly=True)
        return response


@web_router.api_route("/create-stock", methods=["GET", "POST"])
async def web_create_stock(request: Request):
    """Create stock"""
    form_fields = form_for_models(StockProductScheme)
    name_template = "create_stock.html"
    redirect_url = web_router.url_path_for("web_home_page")
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template, status_code=status.HTTP_200_OK,
            context={
                "request": request, "form_fields": form_fields,
            }
        )
    elif request.method == "POST":
        form_data, errors_list = await form_processing(request, StockProductScheme)
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        new_product = object_instance(form_data, Stock)
        new_product.add_product()
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)


@web_router.api_route("/stock-consumption", methods=["GET", "POST"])
async def web_stock_consumption(request: Request):
    """Consumption product"""
    form_fields = form_for_models(StockProductScheme)
    name_template = "create_stock.html"
    redirect_url = web_router.url_path_for("web_home_page")
    consumption = True
    if request.method == "GET":
        return templates.TemplateResponse(
            name=name_template, status_code=status.HTTP_200_OK,
            context={
                "request": request, "form_fields": form_fields, "consumption": consumption
            }
        )
    elif request.method == "POST":
        form_data, errors_list = await form_processing(request, StockProductScheme)
        if errors_list:
            return templates_error(
                request, templates=templates, name_template=name_template, status_code=status.HTTP_400_BAD_REQUEST,
                errors_list=errors_list, form_fields=form_fields
            )
        consumption_product = object_instance(form_data, Stock)
        answer = consumption_product.consumption()
        remainder = answer.get("remainder")
        data = dict(form_data)
        if answer.get("remainder") <= min_quantity:
            await OrderRepositoryRedis.balance_for_order(remainder, data.get("product"))
        return responses.RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
