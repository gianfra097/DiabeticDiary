from android import autoclass
from jnius import PythonJavaClass, java_method
from kivy.app import App

AuthorizationServiceConfiguration = autoclass(
    "net.openid.appauth.AuthorizationServiceConfiguration"
)
AuthorizationRequestBuilder = autoclass(
    "net.openid.appauth.AuthorizationRequest$Builder"
)
AuthorizationResponse = autoclass("net.openid.appauth.AuthorizationResponse")
AuthorizationService = autoclass("net.openid.appauth.AuthorizationService")
Uri = autoclass("android.net.Uri")
PythonActivity = autoclass("org.kivy.android.PythonActivity")


class AuthorizationServiceTokenResponseCallback(PythonJavaClass):
    __javainterfaces__ = [
        "net/openid/appauth/AuthorizationService$TokenResponseCallback"
    ]
    __javacontext__ = "app"

    @java_method(
        "(Lnet/openid/appauth/TokenResponse;Lnet/openid/appauth/AuthorizationException;)V"
    )  # Ritorna void
    def onTokenRequestCompleted(self, resp, ex):
        print(resp)
        print(ex)
        if resp:
            pass


class AndroidOAuth:
    def __init__(self, authendpoint, tokenendpoint, client_id, redirect_uri):
        self.authendpoint = authendpoint
        self.tokenendpoint = tokenendpoint
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._app = App.get_running_app()

    def _on_token_res(self, intent):
        resp = AuthorizationResponse.fromIntent(intent)
        if resp:
            print("Ok, request di autorizzazoine valida")
            self.authService.performTokenRequest(
                resp.createTokenExchangeRequest(), self.support_authorization_callback
            )
        else:
            print("Request non valida")

    def configure(self):
        self.service_config = AuthorizationServiceConfiguration(
            Uri.parse(self.authendpoint), Uri.parse(self.tokenendpoint)
        )
        self.support_authorization_callback = (
            AuthorizationServiceTokenResponseCallback()
        )

    def build_request(self):
        authRequestBuilder = AuthorizationRequestBuilder(
            self.service_config, self.client_id, "code", Uri.parse(self.redirect_uri)
        )
        authRequest = authRequestBuilder.setScope("offline_access").build()
        self._app.result_callbacks.append({"code": 200, "callback": self._on_token_res})

        self.authService = AuthorizationService(
            PythonActivity.mActivity.getApplicationContext()
        )
        authIntent = self.authService.getAuthorizationRequestIntent(authRequest)
        PythonActivity.mActivity.startActivityForResult(
            authIntent, 200
        )  # Lanciamo l'attivita'
