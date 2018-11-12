from eve import Eve
from eve_swagger import swagger, add_documentation
from eve.io.mongo import Validator

import settings
# from oauth2 import BearerAuth
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth


class MyValidator(Validator):
    def _validate_description(self, description, field, value):
        """ {'type': 'string'} """
        # Accept description attribute, used for swagger doc generation
        pass


# app = Eve(auth=BearerAuth)
app = Eve(validator=MyValidator)
app.config["MONGO_URI"] = "mongodb://" + settings.MONGO_HOST + ":" + str(settings.MONGO_PORT)
app.config["TRANSPARENT_SCHEMA_RULES"] = True
app.register_blueprint(swagger)
# ResourceOwnerPasswordCredentials(app)

app.config['SWAGGER_INFO'] = {
    'title': 'EventIT Backend API',
    'version': '0.1',
    'description': 'The EventIT backend provides the ability to book locations and events.',
    'termsOfService': 'my terms of service',
    'contact': {
        'name': 'cthit',
        'url': 'http://chalmers.it'
    },
    'license': {
        'name': 'BSD',
        'url': 'https://github.com/cthit/EventIT/blob/master/LICENSE',
    },
    'schemes': ['http', 'https'],
}


@app.route('/about')
def about_info():
    return "This is the backend of EventIT"


@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"


if __name__ == '__main__':
    # app.run(ssl_context='adhoc')
    app.run()
