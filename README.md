I apologize for the confusion. If you want to obtain a client credentials token using cURL with Keycloak, you can use the following command:

```bash
curl -X POST 'https://your-keycloak-domain/auth/realms/your-realm/protocol/openid-connect/token' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=your-client-id' \
  -d 'client_secret=your-client-secret'
```

Make sure to replace `your-keycloak-domain`, `your-realm`, `your-client-id`, and `your-client-secret` with the appropriate values for your Keycloak setup.

This request will use the client credentials grant type to obtain an access token for the specified client. Keep in mind that client credentials should be treated securely and should not be exposed in a public client or client-side application.