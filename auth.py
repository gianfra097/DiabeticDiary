from android import autoclass  #Dal modulo android viene buildato nella classica configurazione di python_for_android, (quindi funzionalita' offerta da kivy) l'helper autoclass che ci permette di rendere disponibile una classe java su python utilizzando la java native interface (jni)
from jnius import PythonJavaClass, java_method  #Da pyjnius importiamo pythonjavaclass e java_method per gestire successivamente delle callbacks che ci arriveranno da net.openid.appauth
import datetime
import os
import json
from kivy.app import App  #Importiamo from kivy.app app per ottenere accesso all'app correntemente in fase di run

#Qui attraverso l'helper autoclass importato precedentemente andiamo ad ottenere accesso attraverso python alle classi java necessarie offerte da net.openid.appauth
AuthorizationServiceConfiguration = autoclass(
    "net.openid.appauth.AuthorizationServiceConfiguration"
)
AuthorizationRequestBuilder = autoclass(
    "net.openid.appauth.AuthorizationRequest$Builder"
)
TokenRequestBuilder = autoclass("net.openid.appauth.TokenRequest$Builder")
AuthorizationResponse = autoclass("net.openid.appauth.AuthorizationResponse")
AuthorizationService = autoclass("net.openid.appauth.AuthorizationService")
ClientSecretPost = autoclass("net.openid.appauth.ClientSecretPost")

Uri = autoclass("android.net.Uri") #Attraverso autoclass, otteniamo accesso alla classe Uri di android che servira' in fase di configurazione di OAuth2
PythonActivity = autoclass("org.kivy.android.PythonActivity") #Attraverso autoclass, otteniamo accesso alla classe dell'attivita' di questa applicazione

#PythonJavaclass: base per la creazione di una classe Java da una classe Python. Ci permette di implementare interfacce java completamente in Python.
class AuthorizationServiceTokenResponseCallback(PythonJavaClass): #Questa e' la nostra interfaccia java completamente in python per AuthorizationService.TokenResponseCallback
    __javainterfaces__ = [  #Qui andiamo a definire quali sono le interfacce gestite da questa classe
        "net/openid/appauth/AuthorizationService$TokenResponseCallback"
    ]
    __javacontext__ = "app"  #Indicate which class loader to use, ‘system’ or ‘app’. The default is ‘system’. So if you wish to implement a class from an interface you’ve done in your app, use ‘app’.

    on_token_request_completed = None

    @java_method(  #Deve corrispondere alla firma desiderata dell'interfaccia.
        "(Lnet/openid/appauth/TokenResponse;Lnet/openid/appauth/AuthorizationException;)V"
    )  # Ritorna void
    def onTokenRequestCompleted(self, resp, ex):  #Nome della callback di TokenResponseCallback. 
        print(resp)
        print(ex)
        if resp:  #Se c'e' una risposta 
            if self.on_token_request_completed is not None:  #Se e' stata settata una callback lato python per on_token_request_completed
                self.on_token_request_completed(resp, ex)  #Allora andiamo a chiamare la callback passandogli sia la risposta che l'eventuale eccezione

#Definiamo la classe androidauth che ci servira per gestire tutta la parte di autenticazione oauth2 lato python
class AndroidOAuth:
    def __init__(self, authendpoint, tokenendpoint, client_id, redirect_uri):
        self.authendpoint = authendpoint
        self.tokenendpoint = tokenendpoint
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.token_storage = dict(
            access_token=None, refresh_token=None, access_token_expiration_time=None
        )#Definiamo un dizionario "token_storage" che sara' il nostro database temporaneo durante l'esecuzione dell'applicazione
        self._app = App.get_running_app()#Andiamo a rendere disponibile all'interno dell'oggetto quella che e' l'applicazione kivy in fase di esecuzione

    def _on_token_request_completed(self, tokenresp, ex):
        #Utilizziamo un try except per evitare di mandare in crash l'applicazione per errori o eccezioni che non stiamo gestendo
        '''
        try:
            exception_json_string = ex.toJsonString()
        except:
            exception_json_string = None
        print(exception_json_string)
        '''
        try:
            self.token_storage = dict(
                access_token=tokenresp.accessToken,
                refresh_token=tokenresp.refreshToken,
                access_token_expiration_time=tokenresp.accessTokenExpirationTime,
            )#Creo un nuovo dizionario ed assegno il nuovo dizionario con i valori ottenuti da tokenresp(era resp) a quello di self.token_storage(vedi load_authentication_data_from_storage, cioe' rimane nel device nonostante abbia chiuso l'applicazione)
            self.save_authentication_data_to_storage()#Salvo i dati di autenticazione nello storage
        except:
            pass

        print(self.token_storage)

    #Callback che viene chiamata per ricevere i dati dal fine esecuzione dell'intent e poi noi andremo a processarli
    def _on_token_res(self, intent):
        resp = AuthorizationResponse.fromIntent(intent) #Andiamo ad ottenere la risposta di autenticazione dall'intent che l'ha generata
        print(resp)
        if resp:#Se la risposta e' valida, andiamo ad effettuare la tokenrequest vera e propria (eravamo autenticati ma non avevamo un token)
            print("Ok, request di autorizzazoine valida")
            self.authService.performTokenRequest(
                resp.createTokenExchangeRequest(),
                self.clientAuth,
                self.support_authorization_callback,
            ) #Attraverso self.authService, andiamo ad effettuare una richiesta di token passandogli quella che e' la risposta autorizzata (resp), clientAuth (che e' stato generato precedentemente passandogli la secret) e l'oggetto di callback sul quale riceveremo i token (o eventualmente un errore)
        else:
            print("Request non valida")

    def configure(self):
        self.clientAuth = ClientSecretPost("Ad8Cgk4tG1HgA4v7")#Il servizio di OAuth2 di dexcom, prevede l'utilizzo di una chiave secret, che inseriamo su ClientAuth, da passare in fase di richiesta token
        self.service_config = AuthorizationServiceConfiguration(
            Uri.parse(self.authendpoint), Uri.parse(self.tokenendpoint)
        )#Configuriamo il servizio oauth2 passando l'endpoint di autenticazione e l'endpoint per la richiesta di token
        self.support_authorization_callback = (
            AuthorizationServiceTokenResponseCallback()
        )#Andiamo ad istanziare un oggetto di tipo AuthorizationServiceTokenResponseCallback che passeremo poi in fase di richiesta token per ottenere le risposte del servizio
        self.support_authorization_callback.on_token_request_completed = (
            self._on_token_request_completed
        )#Andiamo a settare una callback dell'oggetto AuthorizationServiceTokenResponseCallback che ci permetta di ottenere i dati all'interno dell'oggetto AndroidOAuth

    def first_login(self):
        authRequestBuilder = AuthorizationRequestBuilder(
            self.service_config, self.client_id, "code", Uri.parse(self.redirect_uri)
        )#Andiamo a comporre la richiesta di autorizzazione passando la configurazione precedentemente generata in .configure(), il clientid, definiamo che vogliamo una risposta di tipo code e passiamo quello che e' l'uri di redirect necessario ad OAuth2. 
        #Redirect Uri e' l'indirizzo che OAuth2 chiamera' per passare i dati di autorizzazione, in questo caso e' un uri direttamente gestito dall'applicazione
        authRequest = authRequestBuilder.setScope("offline_access").build()#Effettuiamo effettivamente la costruzione della richiesta per OAuth2 settando come scope offline_access(vedi documentazione dexcom)
        self._app.result_callbacks.append({"code": 200, "callback": self._on_token_res})#L'applicazione gestisce una serie di callback in risposta alle chiamate sulla Uri dell'applicazione, in questo caso andiamo ad aggiungere un nuovo codice univoco che identifichi questa richiesta e gli passiamo quella che sara' la callback da chiamare

        self.authService = AuthorizationService(
            PythonActivity.mActivity.getApplicationContext()
        )#Istanziamo un AuthorizationService passandogli come argomento il context attuale dell'attivita' dell'applicazione
        authIntent = self.authService.getAuthorizationRequestIntent(authRequest)#Andiamo ad ottenere l'intent che ci permettera' poi di ottenere una risposta dal servizio di autenticazione
        PythonActivity.mActivity.startActivityForResult(
            authIntent, 200
        )  #Lanciamo l'attivita' passando l'intent precedentemente generato e il codice (200) per identificare la callback.

    #Decoratore property
    @property
    def auth_data_path(self):
        #Dato che andremo spesso ad utilizzare quello che e' un percorso che ci indica dove il nostro file "auth_data.json" e' salvato, andiamo ad esporlo attraverso una proprieta' 
        return os.path.join(
            self._app.user_data_dir, "auth_data.json"
        )

    #Questa funzoine si occupa di caricare i dati di autenticazione dal nostro storage persistente (file .json auth_data.json)
    #Se il file esiste andiamo ad aprirlo in modalita' di lettura e carichiamo nel dizionario self.token_storage, il contenuto del file json.
    def load_authentication_data_from_storage(self): 
        if os.path.exists(
            self.auth_data_path
        ):
            with open(self.auth_data_path, "r") as f:
                self.token_storage = json.load(f)

    #Salviamo i dati per l'autenticazione attraverso un dump del dizionario (rappresentazione a stringa) dopo aver aperto il file in modalita' di scrittura
    def save_authentication_data_to_storage(self):
        with open(self.auth_data_path, "w") as f:
            json.dump(self.token_storage, f)

    #Verifichiamo se l'access token e' scaduto, confrontando la data e l'ora attuale con il timestamp che ci e' stato fornito in fase di scambio token
    def is_access_token_expired(self):
        return datetime.datetime.now() > datetime.datetime.fromtimestamp(
            self.token_storage["access_token_expiration_time"] / 1000
        )

    #Verifichiamo se esiste l'access token e non è scaduto
    def is_access_token_valid(self):
        if self.token_storage["access_token"] and not self.is_access_token_expired():
            return True
        else:
            return False

    #Questa funzione va a verificare se access token e refresh token sono settati a None. Se lo sono, significa che non abbiamo mai effettuato il login
    def is_first_login(self):
        return (
            self.token_storage["access_token"] is None
            and self.token_storage["refresh_token"] is None
        )

    #Come da ciclo di vita OAuth2, l'access token scade, questo metodo ci permette di andare a chiedere un nuovo access token, un nuovo refresh token 
    #ed una nuova data di scadenza per l'access_token, tramite il refresh token precedentemente ottenuto.
    def refresh_token(self):
        token_request = (
            TokenRequestBuilder(self.service_config, self.client_id)
            .setGrantType("refresh_token")
            .setScope("offline_access")
            .setRefreshToken(self.token_storage["refresh_token"])
            .setRedirectUri(Uri.parse(self.redirect_uri))
            .build()
        ) #Andiamo a costruire quella che e' una richiesta di token, passando i dati richiesti
        print(self.token_storage)

        #Come fatto precedentemente, andiamo ad istanziare un servizio authorizaitionService, passandogli il context dell'attivita' 
        self.authService = AuthorizationService(
            PythonActivity.mActivity.getApplicationContext()
        )
        self.authService.performTokenRequest(
            token_request,
            self.clientAuth,
            self.support_authorization_callback,
        ) #Andiamo ad effettuare la tokenrequest, passando la richiesta token buildata, l'oggetto clientAuth che contiene la secret e l'oggetto di callback