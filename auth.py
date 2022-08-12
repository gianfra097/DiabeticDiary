from android import autoclass

AuthorizationServiceConfiguration = autoclass('net.openid.appauth.AuthorizationServiceConfiguration')
AuthorizationRequestBuilder = autoclass('net.openid.appauth.AuthorizationRequest$Builder')
AuthorizationResponse = autoclass('net.openid.appauth.AuthorizationResponse')
AuthorizationService = autoclass('net.openid.appauth.AuthorizationService')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class AndroidOAuth:
    def __init__(self,authendpoint,tokenendpoint,client_id,redirect_uri):
        self.authendpoint = authendpoint
        self.tokenendpoint = tokenendpoint
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def configure(self):
        self.service_config = AuthorizationServiceConfiguration(Uri.parse(self.authendpoint), Uri.parse(self.tokenendpoint))

    def build_request(self):
        authRequestBuilder = AuthorizationRequestBuilder(self.service_config, self.client_id, "code", Uri.parse(self.redirect_uri))
        authRequest = authRequestBuilder.setScope("offline_access").build()      
        
        authService = AuthorizationService(PythonActivity.mActivity.getApplicationContext())
        authIntent = authService.getAuthorizationRequestIntent(authRequest)
        PythonActivity.mActivity.startActivityForResult(authIntent, 200)
