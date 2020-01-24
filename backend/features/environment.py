from behave import fixture, use_fixture
from app import create_app, db


@fixture
def budgie_client(context, *args, **kwargs):
    context.app = create_app("testing")
    context.app_context = context.app.app_context()
    context.app_context.push()
    db.create_all()


def before_feature(context, feature):
    use_fixture(budgie_client, context)
