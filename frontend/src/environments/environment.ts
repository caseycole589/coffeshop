export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "dev-filffmow.us", // the auth0 domain prefix
    audience: "https://myapp/", // the audience set for the auth0 app
    clientId: "JSE1VcVE9Orxtw5BISkC9RfnOia88niC", // the client id generated for the auth0 app
    callbackURL: "http://localhost:8100", // the base url of the running ionic application.
  },
};
// https://dev-filffmow.us.auth0.com/authorize?audience=https://myapp/&response_type=token&client_id=JSE1VcVE9Orxtw5BISkC9RfnOia88niC&redirect_uri=https://127.0.0.1:8080/login-results
