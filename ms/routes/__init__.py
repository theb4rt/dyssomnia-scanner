from ms import app
import ms.api_nmap.route as api_nmap_route
import ms.api_users.route as api_users_route

api_prefix = app.config.get('URL_PREFIX')

app.register_blueprint(api_nmap_route.api_bp, url_prefix="{}{}".format(api_prefix, "nmap"))
app.register_blueprint(api_users_route.api_bp, url_prefix="{}{}".format(api_prefix, "user"))
