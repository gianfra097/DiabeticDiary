from android import autoclass
from jnius import PythonJavaClass, java_method
import datetime
from kivy.app import App

AuthorizationServiceConfiguration = autoclass(
    "net.openid.appauth.AuthorizationServiceConfiguration"
)
AuthorizationRequestBuilder = autoclass(
    "net.openid.appauth.AuthorizationRequest$Builder"
)
AuthorizationResponse = autoclass("net.openid.appauth.AuthorizationResponse")
AuthorizationService = autoclass("net.openid.appauth.AuthorizationService")
ClientSecretPost = autoclass("net.openid.appauth.ClientSecretPost")
Uri = autoclass("android.net.Uri")
PythonActivity = autoclass("org.kivy.android.PythonActivity")


class AuthorizationServiceTokenResponseCallback(PythonJavaClass):
    __javainterfaces__ = [
        "net/openid/appauth/AuthorizationService$TokenResponseCallback"
    ]
    __javacontext__ = "app"

    on_token_request_completed = None

    @java_method(
        "(Lnet/openid/appauth/TokenResponse;Lnet/openid/appauth/AuthorizationException;)V"
    )  # Ritorna void
    def onTokenRequestCompleted(self, resp, ex):
        print(resp)
        print(ex)
        if resp:
            if self.on_token_request_completed is not None:
                self.on_token_request_completed(resp, ex)


class AndroidOAuth:
    def __init__(self, authendpoint, tokenendpoint, client_id, redirect_uri):
        self.authendpoint = authendpoint
        self.tokenendpoint = tokenendpoint
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._app = App.get_running_app()

    def _on_token_request_completed(self, tokenresp, ex):

        try:
            exception_json_string = tokenresp.toJsonString()
        except:
            exception_json_string = None

        try:
            token_storage = dict(
                access_token=tokenresp.accessToken,
                refresh_token=tokenresp.refreshToken,
                expiration_datetime=datetime.datetime.fromtimestamp(
                    tokenresp.accessTokenExpirationTime / 1000
                ),
            )
        except:
            token_storage = None

        print(token_storage, exception_json_string)

    def _on_token_res(self, intent):
        resp = AuthorizationResponse.fromIntent(intent)
        print(resp)
        if resp:
            print("Ok, request di autorizzazoine valida")
            clientAuth = ClientSecretPost("")
            self.authService.performTokenRequest(
                resp.createTokenExchangeRequest(),
                clientAuth,
                self.support_authorization_callback,
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
        self.support_authorization_callback.on_token_request_completed = (
            self._on_token_request_completed
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
